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


import functools as _functools
import threading as _threading


# Serializes librespot-protocol calls. The librespot-python SyncCallback class
# uses class-level (shared) queue/condition objects (audio/__init__.py:294-295),
# so concurrent get_audio_key() calls race and crash with _queue.Empty. We hold
# this lock around stream-load (which fetches the audio key + sets up the CDN
# request) so only one track is in that critical section at a time. The actual
# CDN bytes are still streamed in parallel because each thread's stream object
# pulls from its own HTTP connection once load() returns.
_SPOTIFY_SESSION_LOCK = _threading.Lock()


# Spotify's keymaster has a per-session burst limit. We track an adaptive
# baseline wait across tracks: after a track succeeds, halve it (decays toward
# zero); when a track is rate-limited and we have to back off, lift this
# baseline so the NEXT track preemptively sleeps before its first attempt.
# Self-modulating throttle: a few rate-limited tracks raise the floor, a run
# of successes lowers it again. State is module-global so all downloads in
# this Python process feed the same throttle.
_SPOTIFY_BACKOFF_LOCK = _threading.Lock()
_SPOTIFY_BACKOFF_FLOOR = 0.0  # seconds, current preemptive-sleep baseline


def _spotify_backoff_take():
    """Query. Return current baseline preemptive sleep (seconds)."""
    with _SPOTIFY_BACKOFF_LOCK:
        return _SPOTIFY_BACKOFF_FLOOR


def _spotify_backoff_record_success():
    """Command. Halve the baseline -- decays toward zero on consecutive successes."""
    global _SPOTIFY_BACKOFF_FLOOR
    with _SPOTIFY_BACKOFF_LOCK:
        _SPOTIFY_BACKOFF_FLOOR /= 2.0


def _spotify_backoff_record_rate_limit(last_wait_seconds):
    """Command. Lift baseline to at least the wait that just succeeded."""
    global _SPOTIFY_BACKOFF_FLOOR
    with _SPOTIFY_BACKOFF_LOCK:
        if last_wait_seconds > _SPOTIFY_BACKOFF_FLOOR:
            _SPOTIFY_BACKOFF_FLOOR = last_wait_seconds


@_functools.lru_cache(maxsize=None)
def _spotify_authenticate(credentials_path):
    """
    Command. Authenticate to Spotify and return a librespot Session.

    Memoized for the lifetime of the Python process: the first call per
    credentials_path opens a real session; all subsequent calls return the same
    Session object, avoiding the AP-handshake cost per track when downloading
    playlists/albums. (functools.lru_cache rather than rp.memoized because this
    module is imported during rp's own initialization, before rp.memoized is
    bound on the namespace.)

    Tries (in order):
      1. Existing `credentials.json` at credentials_path (cached from prior run).
      2. The macOS desktop app's autologin.blob (no user interaction).
      3. The librespot OAuth flow (interactive; opens a localhost URL).

    On success, librespot persists credentials_path so subsequent runs are silent.
    """
    import time
    rp.pip_import('librespot')
    from librespot.core import Session

    def _announce(sess):
        rp.fansi_print('rp.download_spotify_audio: authenticated as '+sess.username(),'green')
        return sess

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
                return _announce(sess)
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
                return _announce(sess)
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
    return _announce(b.create())


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


def _parse_spotify_collection(url_or_id):
    """
    Pure function. Extract (kind, base62_id) from a Spotify URL/URI/ID for a
    track collection. Treats both playlists and albums as collections, since
    "download every track in this thing" makes equal sense for either.

    Returns:
        (kind, id) where kind is "playlist" or "album".

    Raises ValueError if no collection ID is found.

    >>> _parse_spotify_collection("https://open.spotify.com/playlist/37i9dQZF1F5p3rmiWPIYgZ?si=x")
    ('playlist', '37i9dQZF1F5p3rmiWPIYgZ')
    >>> _parse_spotify_collection("https://open.spotify.com/album/4XgGOMRY7H4hl6OQi5wb2Z?si=x")
    ('album', '4XgGOMRY7H4hl6OQi5wb2Z')
    >>> _parse_spotify_collection("spotify:album:4XgGOMRY7H4hl6OQi5wb2Z")
    ('album', '4XgGOMRY7H4hl6OQi5wb2Z')
    """
    import re
    m = re.search(r'(playlist|album)[:/]([A-Za-z0-9]{22})', url_or_id)
    if not m:
        raise ValueError("Cannot parse Spotify playlist/album id from: " + repr(url_or_id))
    return m.group(1), m.group(2)


def _track_id_to_url(track_id):
    """Pure function. Wrap a 22-char base62 track ID in a public Spotify URL.

    >>> _track_id_to_url("53DCgVviFW9hgCM9dKZmcQ")
    'https://open.spotify.com/track/53DCgVviFW9hgCM9dKZmcQ'
    """
    return "https://open.spotify.com/track/" + track_id


def _list_playlist_track_ids(session, base62_id):
    """Query. Return a list of base62 track IDs in playlist order."""
    from librespot.metadata import PlaylistId
    pid = PlaylistId.from_uri("spotify:playlist:" + base62_id)
    result = session.api().get_playlist(pid)
    out = []
    for item in result.contents.items:
        if item.uri.startswith("spotify:track:"):
            out.append(item.uri.split(":")[-1])
    return out


def _list_album_track_ids(session, base62_id):
    """Query. Return a list of base62 track IDs in album order (across all discs)."""
    from librespot.metadata import AlbumId, TrackId
    aid = AlbumId.from_base62(base62_id)
    album = session.api().get_metadata_4_album(aid)
    out = []
    for disc in album.disc:
        for track in disc.track:
            uri = TrackId.from_hex(track.gid.hex()).to_spotify_uri()
            out.append(uri.split(":")[-1])
    return out


_SPOTIFY_COLLECTION_LISTERS = {
    'playlist': _list_playlist_track_ids,
    'album':    _list_album_track_ids,
}


def get_spotify_playlist_song_urls(url_or_id, *, credentials_path=None):
    """
    Returns the list of `https://open.spotify.com/track/<id>` URLs for every
    track in a Spotify playlist OR album. Albums are accepted as well as
    playlists -- in this library they are treated identically. Authenticates
    silently using the same credentials as `download_spotify_audio`.

    Parameters:
        - url_or_id (str): Playlist or album URL/URI. Bare 22-char IDs are
                           ambiguous and not accepted.
        - credentials_path (str, optional): Path to the cached librespot credentials.json
                                            (defaults to ~/.spotify_rp_creds.json).

    Returns:
        - list[str]: One open.spotify.com/track/... URL per track, in collection order.

    Examples:
        >>> urls = get_spotify_playlist_song_urls("https://open.spotify.com/playlist/37i9dQZF1F5p3rmiWPIYgZ")
        >>> len(urls)
        573
        >>> urls[0]
        'https://open.spotify.com/track/53DCgVviFW9hgCM9dKZmcQ'
        >>> urls = get_spotify_playlist_song_urls("https://open.spotify.com/album/4XgGOMRY7H4hl6OQi5wb2Z")
        >>> len(urls)
        26
    """
    import os
    if credentials_path is None:
        credentials_path = os.path.expanduser("~/.spotify_rp_creds.json")
    rp.pip_import('librespot')

    kind, base62_id = _parse_spotify_collection(url_or_id)
    session = _spotify_authenticate(credentials_path)
    track_ids = _SPOTIFY_COLLECTION_LISTERS[kind](session, base62_id)
    return [_track_id_to_url(tid) for tid in track_ids]


def download_spotify_playlist(url_or_id,
                              out_dir=None,
                              *,
                              filetype='mp3',
                              skip_existing=True,
                              credentials_path=None,
                              show_progress='eta:Downloading Spotify Audio',
                              num_threads=0,
                              strict=False,
                              timeout=None):
    """
    Downloads every track in a Spotify playlist (including "Liked Songs") at the
    same 320kbps quality as `download_spotify_audio`. Files are saved as
    `<artist> - <title>.<filetype>` inside `out_dir`. Skips tracks whose output
    file already exists by default (so the call is resumable).

    Uses rp.load_files under the hood for parallelism and progress reporting.

    Parameters:
        - url_or_id (str): Playlist URL, URI, or 22-char base62 ID.
        - out_dir (str, optional): Output directory. Defaults to CWD.
        - filetype (str, optional): "mp3" or "ogg". Defaults to "mp3".
        - skip_existing (bool, optional): If True (default), already-downloaded
                                          files are skipped. Set False to
                                          re-download everything.
        - credentials_path (str, optional): Path to the cached librespot creds.
        - show_progress: Forwarded to rp.load_files. True / False / 'eta' / 'tqdm'.
                         Defaults to 'eta'.
        - num_threads (int, optional): Concurrent downloads. Defaults to 0
                                       (serial, main-thread). Spotify's keymaster
                                       throttles per-session bursts and returns
                                       "Audio key error code 2" once tripped, so
                                       parallelism mostly hurts. Bump to 2-4 for
                                       small playlists where you accept retries.
        - strict (bool or None, optional): Forwarded to rp.load_files. True
                                           raises on any failure; False (default)
                                           skips failed tracks; None substitutes
                                           None for failed tracks.

    Returns:
        - list[str]: Absolute paths to the downloaded files (one per track,
                     in playlist order; failed tracks are absent or None
                     depending on `strict`).

    Examples:
        >>> paths = download_spotify_playlist("https://open.spotify.com/playlist/37i9dQZF1F5p3rmiWPIYgZ", out_dir="liked_songs")
        >>> len(paths)
        573
    """
    if out_dir is None:
        out_dir = "."
    rp.make_directory(out_dir)
    out_dir = rp.get_absolute_path(out_dir)

    import functools
    if credentials_path is None:
        credentials_path = rp.r._spotify_credentials_path
    urls = get_spotify_playlist_song_urls(url_or_id, credentials_path=credentials_path)
    _spotify_authenticate(credentials_path)  # warm the lru_cache before threads fan out

    return rp.load_files(
        functools.partial(
            download_spotify_audio,
            filetype=filetype,
            skip_existing=skip_existing,
            out_dir=out_dir,
            credentials_path=credentials_path,
            timeout=timeout,
        ),
        urls,
        num_threads=num_threads,
        show_progress=show_progress,
        strict=strict,
    )


def download_spotify_audio(url_or_id,
                           path=None,
                           *,
                           filetype='mp3',
                           skip_existing=False,
                           overwrite=False,
                           out_dir=None,
                           credentials_path=None,
                           timeout=None):
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
        credentials_path = rp.r._spotify_credentials_path

    # Earliest possible skip_existing short-circuit: when the user passed an
    # explicit `path`, we know the final output location WITHOUT any network
    # call, so we can bail out before authenticating or hitting any Spotify
    # endpoint. This avoids both the AP handshake and the keymaster rate limit.
    def _resolve_path(p):
        if out_dir is not None:
            import os
            rp.make_directory(out_dir)
            p = os.path.join(out_dir, os.path.basename(p))
        return rp.with_file_extension(p, filetype, replace=True)

    if path is not None:
        path = _resolve_path(path)
        if skip_existing and rp.path_exists(path):
            return rp.get_absolute_path(path)

    rp.pip_import('librespot')
    from librespot.audio.decoders import VorbisOnlyAudioQuality, AudioQuality
    from librespot.metadata import TrackId

    session = _spotify_authenticate(credentials_path)

    # librespot-python's SyncCallback uses class-level shared state
    # (audio/__init__.py:294-295), so concurrent stream loads race each other
    # and crash with _queue.Empty. Hold a process-wide lock around the
    # stream-load call. CDN byte streaming below is still parallel because
    # each thread reads from its own HTTP connection.
    #
    # Spotify's keymaster also rate-limits audio-key requests per session: a
    # rapid burst returns AudioKey error code 2 (KEY_NOT_AVAILABLE/PERMISSION_DENIED).
    # Retry-with-backoff handles that.
    import time
    tid = TrackId.from_uri("spotify:track:"+track_id)
    # Cheap metadata pre-fetch (one mercury call, NOT keymaster-rate-limited)
    # so failure messages can name the song AND so we can resolve the default
    # "<artist> - <title>" path BEFORE the expensive content_feeder().load().
    with _SPOTIFY_SESSION_LOCK:
        meta_for_label = session.api().get_metadata_4_track(tid)
    label_artist = meta_for_label.artist[0].name if meta_for_label.artist else "?"
    label_title = meta_for_label.name or track_id
    label = label_artist+" - "+label_title

    # Second skip_existing short-circuit: when `path` was None we now have
    # enough metadata to derive the default name. Bail out before the
    # rate-limited audio-key fetch if the file already exists.
    if path is None:
        derived_artist = meta_for_label.artist[0].name if meta_for_label.artist else "Unknown Artist"
        derived_title = meta_for_label.name or track_id
        path = _resolve_path(derived_artist + " - " + derived_title)
        if skip_existing and rp.path_exists(path):
            return rp.get_absolute_path(path)

    # Preemptive sleep using the cross-track adaptive baseline. If the previous
    # track had to wait N seconds to get past the keymaster rate limit, this
    # track sleeps N/2 BEFORE its first attempt -- more likely to succeed first
    # try. After a clean success, the baseline halves; over many failures it
    # rises. Self-modulates instead of every track resetting to zero.
    preemptive = _spotify_backoff_take()
    if preemptive >= 1:
        rp.fansi_print('rp.download_spotify_audio: preemptively waiting '+str(int(preemptive))+'s before '+repr(label)+' (adaptive throttle)','cyan')
        time.sleep(preemptive)

    last_err = None
    elapsed = preemptive
    last_wait = preemptive
    attempt = 0
    stream = None
    while timeout is None or elapsed < timeout:
        with _SPOTIFY_SESSION_LOCK:
            try:
                stream = session.content_feeder().load(
                    tid,
                    VorbisOnlyAudioQuality(AudioQuality.VERY_HIGH),
                    False,
                    None,
                )
                break
            except RuntimeError as e:
                if "Failed fetching audio key" not in str(e):
                    raise
                last_err = e
        wait = 16 * (2 ** attempt)
        if timeout is not None:
            wait = min(wait, timeout - elapsed)
        budget_str = 'unlimited' if timeout is None else str(int(timeout))+'s'
        rp.fansi_print('rp.download_spotify_audio: keymaster rate-limited for '+repr(label)+' (attempt '+str(attempt+1)+', cumulative '+str(int(elapsed))+'s/'+budget_str+'); waiting '+str(int(wait))+'s','yellow')
        time.sleep(wait)
        elapsed += wait
        last_wait = wait
        attempt += 1
    if stream is None:
        raise RuntimeError("rp.download_spotify_audio: keymaster refused audio key for "+repr(label)+" after "+str(int(elapsed))+"s timeout: "+str(last_err))

    if attempt == 0:
        _spotify_backoff_record_success()
    else:
        _spotify_backoff_record_rate_limit(last_wait)

    track_meta = stream.track if hasattr(stream, "track") else None

    if rp.path_exists(path):
        if skip_existing:
            return rp.get_absolute_path(path)
        elif overwrite:
            rp.delete_file(path)
        else:
            path = rp.get_unique_copy_path(path)

    # Atomic download: stream OGG bytes to a /tmp partial file, transcode (if
    # mp3) and tag in /tmp too, only mv to the final path on success. Crashes
    # mid-download leave nothing in `out_dir`, so skip_existing stays accurate.
    import os
    import shutil
    import tempfile
    tmp_dir = tempfile.mkdtemp(prefix='rp_spotify_')
    try:
        tmp_ogg = os.path.join(tmp_dir, 'track.ogg')
        audio_in = stream.input_stream.stream()
        total = 0
        with open(tmp_ogg, "wb") as f:
            while True:
                chunk = audio_in.read(64 * 1024)
                if not chunk:
                    break
                f.write(chunk)
                total += len(chunk)
        if total < 1024:
            raise RuntimeError("rp.download_spotify_audio: only "+str(total)+" bytes downloaded -- something is wrong")

        if filetype == 'mp3':
            rp.r._ensure_ffmpeg_installed()
            import subprocess
            tmp_final = os.path.join(tmp_dir, 'track.mp3')
            cmd = ['ffmpeg', '-y', '-i', tmp_ogg, '-codec:a', 'libmp3lame', '-b:a', '320k', tmp_final]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0:
                raise RuntimeError("rp.download_spotify_audio: ffmpeg transcode failed:\n"+res.stderr)
        else:
            tmp_final = tmp_ogg

        if track_meta is not None:
            _tag_spotify_audio_file(tmp_final, track_meta)

        shutil.move(tmp_final, path)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    return rp.get_absolute_path(path)
