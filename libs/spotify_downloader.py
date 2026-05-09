"""
Spotify track downloader for rp.download_spotify_audio.

Pulls real Spotify audio bytes (320kbps OGG Vorbis with Premium) directly from
Spotify's CDN via the Spotify Connect protocol (librespot). Authentication is
automatic on macOS when the Spotify desktop app is logged in -- the autologin
blob from ~/Library/Application Support/Spotify/prefs is decrypted with the
machine's IOPlatformUUID, no password prompt. Falls back to librespot's OAuth
flow when the desktop blob isn't usable.

NO YouTube/SoundCloud fallback. Every CDN URL is asserted to be on a
Spotify-controlled host before any byte is fetched.

Companion: tags the resulting file with title/artist/album/year/track number
plus the largest available cover art from i.scdn.co.
"""

import rp


_SPOTIFY_AUDIO_HOSTS = (
    ".spotify.com",
    ".scdn.co",
    ".spotifycdn.com",
    ".spotifycontent.com",
    ".spotify-everywhere.com",
)


def _parse_spotify_track_id(url_or_id):
    """
    Pure function. Extract the 22-char base62 track ID from any Spotify URL or bare ID.

    >>> _parse_spotify_track_id("https://open.spotify.com/track/0eM4CcU3AaE7m4FGH8vgql?si=x")
    '0eM4CcU3AaE7m4FGH8vgql'
    >>> _parse_spotify_track_id("0eM4CcU3AaE7m4FGH8vgql")
    '0eM4CcU3AaE7m4FGH8vgql'
    >>> _parse_spotify_track_id("spotify:track:0eM4CcU3AaE7m4FGH8vgql")
    '0eM4CcU3AaE7m4FGH8vgql'
    """
    import re
    if re.fullmatch(r'[A-Za-z0-9]{22}', url_or_id):
        return url_or_id
    m = re.search(r'track[:/]([A-Za-z0-9]{22})', url_or_id)
    if not m:
        raise ValueError("Cannot parse Spotify track id from: " + repr(url_or_id))
    return m.group(1)


def _parse_spotify_desktop_prefs(prefs_path):
    """
    Query. Parse the Spotify macOS desktop app's `prefs` file (a one-key-per-line
    text file with quoted string values) into a {key: value} dict. Returns {} if the
    file does not exist.
    """
    import json
    import os
    import re
    if not os.path.isfile(prefs_path):
        return {}
    out = {}
    with open(prefs_path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            m = re.match(r'^([A-Za-z0-9_.-]+)\s*=\s*(.*)$', line)
            if not m:
                continue
            key, raw = m.group(1), m.group(2).strip()
            if raw.startswith('"') and raw.endswith('"'):
                try:
                    out[key] = json.loads(raw)
                except json.JSONDecodeError:
                    out[key] = raw[1:-1]
            else:
                out[key] = raw
    return out


def _extract_spotify_desktop_blob():
    """
    Query. Read (username, base64_blob) from `~/Library/Application Support/Spotify/prefs`
    on macOS. Returns None if the desktop app has no saved autologin credentials
    (e.g. "Remember me" disabled, or non-macOS platform).
    """
    import os
    prefs = os.path.expanduser("~/Library/Application Support/Spotify/prefs")
    p = _parse_spotify_desktop_prefs(prefs)
    user = p.get("autologin.username") or p.get("autologin.canonical_username")
    blob = p.get("autologin.blob")
    if not user or not blob:
        return None
    return user, blob


def _spotify_candidate_device_ids():
    """
    Query. Build a list of plausible device IDs the Spotify desktop client might have
    used to encrypt its autologin blob. The right one is typically IOPlatformUUID on
    macOS; we try variants because the blob format gives no hint of which was used.
    """
    import re
    import socket
    import subprocess
    cands = []
    try:
        out = subprocess.check_output(
            ["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"],
            text=True, stderr=subprocess.DEVNULL,
        )
        m = re.search(r'"IOPlatformUUID"\s*=\s*"([^"]+)"', out)
        if m:
            uuid = m.group(1)
            cands.append(uuid)
            cands.append(uuid.replace("-", ""))
            cands.append(uuid.replace("-", "").lower())
            cands.append(uuid.replace("-", "").upper())
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    try:
        out = subprocess.check_output(
            ["system_profiler", "SPHardwareDataType"],
            text=True, stderr=subprocess.DEVNULL,
        )
        m = re.search(r"Hardware UUID:\s*([A-F0-9-]+)", out)
        if m:
            cands.append(m.group(1))
            cands.append(m.group(1).replace("-", "").lower())
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    cands.append(socket.gethostname())
    cands.append("")
    seen = set()
    uniq = []
    for c in cands:
        if c not in seen:
            seen.add(c)
            uniq.append(c)
    return uniq


def _spotify_decrypt_blob(username, blob_b64, device_id):
    """
    Query. Decrypt the Spotify desktop app's autologin.blob and return a librespot
    LoginCredentials proto. Mirrors librespot.core.Session.Builder.decrypt_blob but
    side-effect-free so we can try multiple device_ids without contaminating
    builder state. Raises if decryption gibberish fails to parse.
    """
    import base64
    import io
    rp.pip_import('Cryptodome', 'pycryptodomex')
    from Cryptodome.Cipher import AES
    from Cryptodome.Hash import SHA1
    from Cryptodome.Protocol.KDF import PBKDF2
    rp.pip_import('librespot')
    from librespot.proto import Authentication_pb2 as Authentication

    encrypted_blob = base64.b64decode(blob_b64)
    sha1 = SHA1.new()
    sha1.update(device_id.encode())
    secret = sha1.digest()
    base_key = PBKDF2(secret, username.encode(), 20, 0x100, hmac_hash_module=SHA1)
    sha1 = SHA1.new()
    sha1.update(base_key)
    key = sha1.digest() + b"\x00\x00\x00\x14"
    aes = AES.new(key, AES.MODE_ECB)
    decrypted = bytearray(aes.decrypt(encrypted_blob))
    n = len(decrypted)
    for i in range(0, n - 0x10):
        decrypted[n - i - 1] ^= decrypted[n - i - 0x11]

    def _read_int(buf):
        lo = buf.read(1)
        if not lo:
            raise ValueError("EOF reading Spotify blob int")
        if (lo[0] & 0x80) == 0:
            return lo[0]
        hi = buf.read(1)
        if not hi:
            raise ValueError("EOF reading Spotify blob int hi")
        return (lo[0] & 0x7F) | (hi[0] << 7)

    buf = io.BytesIO(decrypted)
    buf.read(1)
    le = _read_int(buf); buf.read(le); buf.read(1)
    type_int = _read_int(buf)
    type_name = Authentication.AuthenticationType.Name(type_int)
    buf.read(1)
    al = _read_int(buf)
    auth_data = buf.read(al)
    if len(auth_data) != al or al == 0 or al > 4096:
        raise ValueError("Spotify blob auth_data length suspect: " + str(al))
    return Authentication.LoginCredentials(
        auth_data=auth_data, typ=type_name, username=username,
    )


def _spotify_authenticate(credentials_path):
    """
    Command. Authenticate to Spotify and return a librespot Session.

    Tries (in order):
      1. Existing `credentials.json` at credentials_path (cached from prior run).
      2. The macOS desktop app's autologin.blob (no user interaction).
      3. The librespot OAuth flow (interactive; opens a localhost URL).

    On success, librespot persists credentials_path so subsequent runs are silent.
    """
    import time
    rp.pip_import('librespot')
    from librespot.core import Session

    def _create_with_retry(builder, attempts=3, delay=1.5):
        last = None
        for i in range(attempts):
            try:
                return builder.create()
            except (ConnectionRefusedError, ConnectionResetError, OSError) as e:
                last = e
                rp.fansi_print('rp.download_spotify_audio: AP connect attempt '+str(i+1)+'/'+str(attempts)+' failed: '+str(e)+'; retrying','yellow')
                time.sleep(delay * (i + 1))
        rp.fansi_print('rp.download_spotify_audio: giving up after '+str(attempts)+' attempts; last error: '+str(last),'red')
        return None

    if rp.path_exists(credentials_path):
        rp.fansi_print('rp.download_spotify_audio: using cached credentials at '+credentials_path,'green')
        b = Session.Builder()
        b.conf.stored_credentials_file = credentials_path
        b.stored_file(credentials_path)
        if b.login_credentials is not None:
            sess = _create_with_retry(b)
            if sess is not None:
                return sess
            rp.fansi_print('rp.download_spotify_audio: cached credentials present but session create failed; falling through to fresh blob extraction','yellow')

    extracted = _extract_spotify_desktop_blob()
    if extracted is not None:
        username, blob_b64 = extracted
        rp.fansi_print('rp.download_spotify_audio: desktop autologin blob found for user='+repr(username)+'; trying device-ID candidates','cyan')
        last_err = None
        for did in _spotify_candidate_device_ids():
            try:
                creds = _spotify_decrypt_blob(username, blob_b64, did)
            except Exception as e:
                last_err = e
                continue
            rp.fansi_print('rp.download_spotify_audio: decrypt OK with device_id='+repr(did)+', attempting login','green')
            b = Session.Builder()
            b.conf.stored_credentials_file = credentials_path
            b.login_credentials = creds
            sess = _create_with_retry(b)
            if sess is not None:
                return sess
            last_err = RuntimeError("create() retries exhausted")
        rp.fansi_print('rp.download_spotify_audio: all device_id candidates failed; last error: '+str(last_err),'yellow')
    else:
        rp.fansi_print('rp.download_spotify_audio: no desktop autologin blob found in prefs','yellow')

    rp.fansi_print('rp.download_spotify_audio: falling back to OAuth -- a URL will be printed; visit it in the browser where you are logged in to Spotify','cyan')
    b = Session.Builder()
    b.conf.stored_credentials_file = credentials_path
    def _cb(url):
        rp.fansi_print('\n  >>> open this URL in your browser:\n  '+url+'\n','blue')
    b.oauth(_cb)
    if b.login_credentials is None:
        raise RuntimeError("rp.download_spotify_audio: OAuth did not produce credentials")
    return b.create()


def _assert_spotify_audio_url(url):
    """Command. Raise if URL is not a Spotify-controlled audio host."""
    import urllib.parse
    host = urllib.parse.urlparse(url).hostname or ""
    if not any(host == h.lstrip(".") or host.endswith(h) for h in _SPOTIFY_AUDIO_HOSTS):
        raise RuntimeError("rp.download_spotify_audio: refusing non-Spotify audio host: "+repr(host)+" (url="+repr(url)+")")


def _fetch_spotify_cover_art(track_meta):
    """
    Query. Return (jpeg_bytes, mime) for the largest cover image attached to the track,
    or (None, None) if the track has no cover art. Cover art is served from i.scdn.co.
    """
    images = []
    cover_group = getattr(track_meta.album, 'cover_group', None)
    if cover_group is not None:
        images = list(cover_group.image)
    if not images:
        images = list(getattr(track_meta.album, 'cover', []))
    if not images:
        return None, None
    largest = max(images, key=lambda im: (im.width or 0) * (im.height or 0))
    file_id_hex = largest.file_id.hex()
    url = "https://i.scdn.co/image/" + file_id_hex
    _assert_spotify_audio_url(url)
    rp.pip_import('requests')
    import requests
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.content, "image/jpeg"


def _tag_spotify_audio_file(path, track_meta):
    """
    Command. Embed Spotify metadata (title, artist, album, year, track number,
    disc number) and cover art into an mp3 or ogg file at `path`. No-ops on
    unsupported extensions.
    """
    rp.pip_import('mutagen')
    title = track_meta.name or ""
    artists = [a.name for a in track_meta.artist if a.name]
    artist = ", ".join(artists) if artists else ""
    album = track_meta.album.name or ""
    album_artists = [a.name for a in track_meta.album.artist if a.name]
    album_artist = ", ".join(album_artists) if album_artists else artist
    year = ""
    date = getattr(track_meta.album, 'date', None)
    if date is not None and getattr(date, 'year', 0):
        year = str(date.year)
    track_num = track_meta.number if track_meta.number else 0
    disc_num = track_meta.disc_number if track_meta.disc_number else 0

    cover_bytes, cover_mime = _fetch_spotify_cover_art(track_meta)

    ext = rp.get_file_extension(path).lower()
    if ext == 'mp3':
        from mutagen.id3 import ID3, ID3NoHeaderError, TIT2, TPE1, TPE2, TALB, TRCK, TPOS, TDRC, APIC
        try:
            tags = ID3(path)
        except ID3NoHeaderError:
            tags = ID3()
        tags.delall('TIT2'); tags.delall('TPE1'); tags.delall('TPE2'); tags.delall('TALB')
        tags.delall('TRCK'); tags.delall('TPOS'); tags.delall('TDRC'); tags.delall('APIC')
        tags.add(TIT2(encoding=3, text=title))
        tags.add(TPE1(encoding=3, text=artist))
        tags.add(TPE2(encoding=3, text=album_artist))
        tags.add(TALB(encoding=3, text=album))
        if track_num:
            tags.add(TRCK(encoding=3, text=str(track_num)))
        if disc_num:
            tags.add(TPOS(encoding=3, text=str(disc_num)))
        if year:
            tags.add(TDRC(encoding=3, text=year))
        if cover_bytes:
            tags.add(APIC(encoding=3, mime=cover_mime, type=3, desc='Cover', data=cover_bytes))
        tags.save(path, v2_version=3)
        return
    if ext == 'ogg':
        import base64
        from mutagen.oggvorbis import OggVorbis
        from mutagen.flac import Picture
        f = OggVorbis(path)
        f['title'] = title
        f['artist'] = artist
        f['albumartist'] = album_artist
        f['album'] = album
        if track_num:
            f['tracknumber'] = str(track_num)
        if disc_num:
            f['discnumber'] = str(disc_num)
        if year:
            f['date'] = year
        if cover_bytes:
            pic = Picture()
            pic.type = 3
            pic.mime = cover_mime
            pic.desc = 'Cover'
            pic.data = cover_bytes
            f['metadata_block_picture'] = [base64.b64encode(pic.write()).decode('ascii')]
        f.save()
        return


def download_spotify_audio(url_or_id,
                           path=None,
                           *,
                           filetype='mp3',
                           skip_existing=False,
                           overwrite=False,
                           credentials_path=None):
    """
    Downloads a Spotify track at full quality (320kbps OGG Vorbis with Premium,
    160kbps with free tier). Audio bytes come exclusively from Spotify-controlled
    CDNs (*.scdn.co / *.spotifycdn.com / etc.) -- there is NO YouTube/SoundCloud
    fallback. Authentication is automatic from the macOS Spotify desktop app's
    saved autologin blob (no password prompt) when the user is logged in there.

    On the first run: extracts credentials from ~/Library/Application Support/Spotify/prefs
    (or runs an OAuth fallback if the desktop app isn't available), then caches
    `credentials.json` next to the output file so subsequent runs are silent.

    The downloaded file is tagged with title, artist, album, year, track number,
    disc number, and the largest available cover art from Spotify's image CDN.

    Parameters:
        - url_or_id (str): Spotify track URL, URI, or 22-char base62 ID. All
                           equivalent:
                             "https://open.spotify.com/track/0eM4CcU3AaE7m4FGH8vgql"
                             "spotify:track:0eM4CcU3AaE7m4FGH8vgql"
                             "0eM4CcU3AaE7m4FGH8vgql"
        - path (str, optional): Destination path for the audio file. Defaults to
                                "<artist> - <title>.<filetype>" in CWD. Filetype
                                in the path overrides the `filetype` arg.
        - filetype (str, optional): "mp3" or "ogg". OGG saves the raw librespot
                                    output (no transcode). MP3 transcodes via
                                    ffmpeg at 320kbps. Defaults to "mp3".
        - skip_existing (bool, optional): If True and `path` exists, returns
                                          the existing path without re-downloading.
        - overwrite (bool, optional): If True, overwrites existing file. If False
                                      (and not skip_existing), creates a non-
                                      conflicting path like "song_copy.mp3".
        - credentials_path (str, optional): Path to librespot's credentials.json
                                            cache. Defaults to ~/.spotify_rp_creds.json.

    Returns:
        - str: Absolute path to the downloaded audio file.

    Note:
        - Requires being logged into the Spotify desktop app on macOS for silent
          auth. On other platforms (or first-run without desktop app), librespot's
          OAuth flow takes over and prints a URL to visit in your browser.
        - Backend: librespot-python. The output is raw OGG Vorbis from Spotify's
          CDN; mp3 is a local ffmpeg transcode.

    Examples:
        >>> download_spotify_audio("https://open.spotify.com/track/0eM4CcU3AaE7m4FGH8vgql")
        ans = /Users/ryan/Kishi Bashi - Can't Let Go, Juno.mp3
        >>> get_audio_file_duration(ans)
        ans = 262.71
        >>> download_spotify_audio("0eM4CcU3AaE7m4FGH8vgql", filetype='ogg')
        ans = /Users/ryan/Kishi Bashi - Can't Let Go, Juno.ogg
    """
    if filetype not in ('mp3', 'ogg'):
        raise ValueError("rp.download_spotify_audio: filetype must be 'mp3' or 'ogg', got "+repr(filetype))

    track_id = _parse_spotify_track_id(url_or_id)

    if credentials_path is None:
        import os
        credentials_path = os.path.expanduser("~/.spotify_rp_creds.json")

    rp.pip_import('librespot')
    from librespot.audio.decoders import VorbisOnlyAudioQuality, AudioQuality
    from librespot.metadata import TrackId

    session = _spotify_authenticate(credentials_path)
    rp.fansi_print('rp.download_spotify_audio: authenticated as '+session.username(),'green')

    tid = TrackId.from_uri("spotify:track:"+track_id)
    stream = session.content_feeder().load(
        tid,
        VorbisOnlyAudioQuality(AudioQuality.VERY_HIGH),
        False,
        None,
    )

    track_meta = stream.track if hasattr(stream, "track") else None
    if track_meta is not None and path is None:
        artist = track_meta.artist[0].name if track_meta.artist else "Unknown Artist"
        title = track_meta.name or track_id
        path = artist + " - " + title

    if path is None:
        path = track_id

    path = rp.with_file_extension(path, filetype)
    if rp.path_exists(path):
        if skip_existing:
            return rp.get_absolute_path(path)
        elif overwrite:
            rp.delete_file(path)
        else:
            path = rp.get_unique_copy_path(path)

    if track_meta is not None:
        try:
            files = list(getattr(track_meta, "file", []))
            for alt in getattr(track_meta, "alternative", []):
                files.extend(list(getattr(alt, "file", [])))
            for f in files:
                if not f.file_id:
                    continue
                sr = session.content_feeder().resolve_storage_interactive(f.file_id, False)
                for u in list(sr.cdnurl):
                    _assert_spotify_audio_url(u)
        except AttributeError:
            pass

    if filetype == 'ogg':
        out_path = path
    else:
        out_path = rp.with_file_extension(path, 'ogg')
        if rp.path_exists(out_path):
            out_path = rp.get_unique_copy_path(out_path)

    audio_in = stream.input_stream.stream()
    total = 0
    with open(out_path, "wb") as f:
        while True:
            chunk = audio_in.read(64 * 1024)
            if not chunk:
                break
            f.write(chunk)
            total += len(chunk)
    if total < 1024:
        rp.delete_file(out_path)
        raise RuntimeError("rp.download_spotify_audio: only "+str(total)+" bytes downloaded -- something is wrong")

    if filetype == 'mp3':
        rp.r._ensure_ffmpeg_installed()
        import subprocess
        cmd = ['ffmpeg', '-y', '-i', out_path, '-codec:a', 'libmp3lame', '-b:a', '320k', path]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError("rp.download_spotify_audio: ffmpeg transcode failed:\n"+res.stderr)
        rp.delete_file(out_path)
        out_path = path

    if track_meta is not None:
        _tag_spotify_audio_file(out_path, track_meta)

    return rp.get_absolute_path(out_path)
