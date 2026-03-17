"""
siri_tts — Synthesize speech using macOS Siri voices via private SiriTTSService.framework.

Command, specific.

Glossary:
    sirittsd        macOS daemon (LaunchAgent) that performs Siri TTS synthesis.
                    Lives at SiriTTSService.framework/sirittsd. Communicates via XPC.
    XPC             Apple's inter-process communication mechanism. We send synthesis
                    requests to sirittsd and receive audio data back via XPC callbacks.
    ASBD            AudioStreamBasicDescription — a 9-field struct describing audio
                    format (sample rate, format ID, channels, bit depth, etc.).
                    Returned with each audio callback from sirittsd.
    LPCM            Linear Pulse Code Modulation — raw uncompressed audio samples.
                    FourCC 'lpcm' (0x6C70636D). What we typically get from sirittsd.
    Opus            A lossy audio codec (unrelated to Claude Opus). FourCC 'opus'
                    (0x6F707573). sirittsd may send this instead of LPCM in some
                    configurations. Requires libopus to decode (brew install opus).
    pyobjc          Python-to-Objective-C bridge. Used to call Apple framework APIs
                    (SiriTTSDaemonSession, etc.) from Python.
    natural         Voice type 6 — highest quality Siri voices (Aaron, Martha, etc.)
    neuralAX        Voice type 5 — Accessibility neural voices (Aman, Tara, etc.)
    neural          Voice type 4 — standard neural voices (Simone neural, Nora neural)
    BCP-47          Language tag format, e.g. "en-US", "en-GB", "kk-KZ".
    fallback        When sirittsd silently substitutes a different (lower quality)
                    voice instead of the one requested. Can happen due to thermal
                    throttling, missing voice data, or wrong language tag.
                    We guard against this with disableCompactVoice,
                    disableThermalFallback, and getSynthesisVoiceMatching validation.
    WOM             "Works On My Machine" — code that relies on local state (e.g.
                    which voices are downloaded) rather than being portable.

This module provides a simple interface to Apple's high-quality Siri neural TTS voices
(Aaron, Martha, Simone, Damon, Quinn, Nora, etc.) which are NOT accessible through the
standard `say` command or NSSpeechSynthesizer with explicit voice selection.

Requires:
    - macOS with Siri voices downloaded (System Settings > Accessibility > Spoken Content)
    - pyobjc (typically available in system Python; conda may need pyobjc-core)
    - libopus only if sirittsd sends Opus-encoded audio (brew install opus)

Usage:
    from siri_tts import text_to_speech
    text_to_speech("Hello world", "Aaron")

Three known methods for Siri voice access on macOS (for future reference):

    Method 1 (XPC — IMPLEMENTED HERE):
        dlopen SiriTTSService.framework, use SiriTTSDaemonSession to send synthesis
        requests to the sirittsd daemon via XPC. Audio format varies — sirittsd may
        send LPCM (raw PCM) or Opus-encoded audio, detected at runtime via the ASBD.
        Typically 48kHz 16-bit mono.
        Pros: Direct voice selection, no system state mutation, 48kHz quality,
              full control (rate/pitch/volume/whisper).
        Cons: Private API — could break on macOS updates.

    Method 2 (defaults write + say):
        Write desired voice ID to com.apple.Accessibility
        SpokenContentDefaultVoiceSelectionsByLanguage, then call `say` with no -v flag.
        The `say` command picks up the new default. Save/restore original pref around it.
        Pros: No private frameworks, simple subprocess call.
        Cons: Mutates system Accessibility preference — crash leaves bad state.
              Race condition if user changes voice concurrently.

    Method 3 (NSSpeechSynthesizer .premium):
        NSSpeechSynthesizer with voice IDs like "com.apple.voice.Aman.premium".
        Only works for 4 neuralAX voices (Aman, Aru, Ona, Tara) — NOT the main
        en-US natural voices (Aaron, Martha, Simone, Damon, Quinn).
        Pros: Clean API, no system mutation.
        Cons: Only 4 non-US voices work. Useless for en-US Siri voices.
"""

import ctypes
import struct
import threading
import time
import wave
import os
import tempfile
import subprocess


_SIRI_CHANNELS = 1
_SIRI_SAMPLE_WIDTH = 2  # 16-bit

# AudioFormatID FourCC values
_FMT_LPCM = 0x6C70636D  # 'lpcm'
_FMT_OPUS = 0x6F707573  # 'opus'

# Common libopus paths on macOS (only needed if daemon sends Opus)
_OPUS_SEARCH_PATHS = [
    "/opt/homebrew/lib/libopus.dylib",       # ARM Homebrew
    "/usr/local/lib/libopus.dylib",          # Intel Homebrew
    "/opt/homebrew/lib/libopus.0.dylib",
    "/usr/local/lib/libopus.0.dylib",
]


# ---------------------------------------------------------------------------
# Opus decoder — only loaded if sirittsd sends Opus-encoded audio
# ---------------------------------------------------------------------------

_opus_lib = None
_OPUS_MAX_FRAME_SIZE = 5760  # 120ms at 48kHz


def _load_opus():
    """
    Command, general. Lazily load libopus shared library via ctypes.

    Returns:
        ctypes.CDLL

    Raises:
        OSError: if libopus not found (install via `brew install opus`)
    """
    global _opus_lib
    if _opus_lib is not None:
        return _opus_lib

    for path in _OPUS_SEARCH_PATHS:
        if os.path.exists(path):
            _opus_lib = ctypes.CDLL(path)
            break

    if _opus_lib is None:
        raise OSError(
            "sirittsd sent Opus-encoded audio but libopus not found. "
            "Install it with: brew install opus"
        )

    _opus_lib.opus_decoder_create.restype = ctypes.c_void_p
    _opus_lib.opus_decoder_create.argtypes = [
        ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int),
    ]
    _opus_lib.opus_decode.restype = ctypes.c_int
    _opus_lib.opus_decode.argtypes = [
        ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int32,
        ctypes.POINTER(ctypes.c_int16), ctypes.c_int, ctypes.c_int,
    ]
    _opus_lib.opus_decoder_destroy.restype = None
    _opus_lib.opus_decoder_destroy.argtypes = [ctypes.c_void_p]

    return _opus_lib


def _decode_opus_chunks(opus_chunks, sample_rate):
    """
    Pure function, general. Decode Opus-encoded chunks to 16-bit PCM.

    Each chunk is (raw_opus_bytes, packet_descriptions_bytes).
    Packet descriptions are packed AudioStreamPacketDescription structs (16 bytes each):
        int64  mStartOffset
        uint32 mVariableFramesInPacket
        uint32 mDataByteSize

    Args:
        opus_chunks: list of (bytes, bytes)
        sample_rate: int, e.g. 48000

    Returns:
        bytes: raw 16-bit signed LE mono PCM

    Examples:
        >>> _decode_opus_chunks([], 48000)
        b''
    """
    if not opus_chunks:
        return b""

    lib = _load_opus()
    err = ctypes.c_int(0)
    decoder = lib.opus_decoder_create(sample_rate, 1, ctypes.byref(err))
    if err.value != 0 or not decoder:
        raise RuntimeError("opus_decoder_create failed: error %d" % err.value)

    pcm_parts = []
    try:
        for raw_data, pkt_descs in opus_chunks:
            if not raw_data:
                continue
            if pkt_descs and len(pkt_descs) >= 16:
                # Parse packet descriptions to extract individual Opus frames
                for i in range(len(pkt_descs) // 16):
                    offset = struct.unpack_from("<q", pkt_descs, i * 16)[0]
                    byte_size = struct.unpack_from("<I", pkt_descs, i * 16 + 12)[0]
                    if byte_size == 0:
                        continue
                    frame = raw_data[offset:offset + byte_size]
                    pcm_buf = (ctypes.c_int16 * _OPUS_MAX_FRAME_SIZE)()
                    n = lib.opus_decode(decoder, frame, len(frame), pcm_buf, _OPUS_MAX_FRAME_SIZE, 0)
                    if n > 0:
                        pcm_parts.append(bytes(ctypes.string_at(ctypes.addressof(pcm_buf), n * 2)))
            else:
                # No packet descriptions — try decoding the whole blob as one frame
                pcm_buf = (ctypes.c_int16 * _OPUS_MAX_FRAME_SIZE)()
                n = lib.opus_decode(decoder, raw_data, len(raw_data), pcm_buf, _OPUS_MAX_FRAME_SIZE, 0)
                if n > 0:
                    pcm_parts.append(bytes(ctypes.string_at(ctypes.addressof(pcm_buf), n * 2)))
    finally:
        lib.opus_decoder_destroy(decoder)

    return b"".join(pcm_parts)


# ---------------------------------------------------------------------------
# SiriTTSService framework interface
# ---------------------------------------------------------------------------

_framework_loaded = False


def _ensure_framework():
    """
    Command, specific. Load SiriTTSService.framework and register ObjC block metadata.

    Idempotent — safe to call multiple times.

    Raises:
        OSError: if framework cannot be loaded
    """
    global _framework_loaded
    if _framework_loaded:
        return

    fw_path = (
        "/System/Library/PrivateFrameworks/"
        "SiriTTSService.framework/SiriTTSService"
    )
    ctypes.cdll.LoadLibrary(fw_path)

    import objc

    # Register block type metadata for the callback parameters.
    # Without this, pyobjc cannot create the ObjC blocks correctly.
    _block_meta = {
        "callable": {
            "retval": {"type": b"v"},
            "arguments": [{"type": b"@?"}, {"type": b"@"}],
        }
    }
    objc.registerMetaDataForSelector(
        b"SiriTTSDaemonSession",
        b"synthesizeWithRequest:didFinish:",
        {"arguments": {3: _block_meta}},
    )
    objc.registerMetaDataForSelector(
        b"SiriTTSSynthesisContext",
        b"setDidGenerateAudio:",
        {"arguments": {2: _block_meta}},
    )
    objc.registerMetaDataForSelector(
        b"SiriTTSDaemonSession",
        b"downloadedVoicesMatching:reply:",
        {"arguments": {3: _block_meta}},
    )
    objc.registerMetaDataForSelector(
        b"SiriTTSDaemonSession",
        b"getSynthesisVoiceMatching:reply:",
        {
            "arguments": {
                3: {
                    "callable": {
                        "retval": {"type": b"v"},
                        "arguments": [
                            {"type": b"@?"},
                            {"type": b"@"},
                            {"type": b"@"},
                        ],
                    }
                }
            }
        },
    )

    _framework_loaded = True


def _pump_runloop(done_event, timeout_seconds):
    """
    Command, specific. Spin the NSRunLoop until done_event is set or timeout.

    Args:
        done_event (threading.Event): signals completion
        timeout_seconds (float): max wait time

    Raises:
        TimeoutError: if done_event not set within timeout
    """
    import Foundation

    run_loop = Foundation.NSRunLoop.currentRunLoop()
    deadline = time.time() + timeout_seconds
    while not done_event.is_set() and time.time() < deadline:
        run_loop.runUntilDate_(
            Foundation.NSDate.dateWithTimeIntervalSinceNow_(0.05)
        )
    if not done_event.is_set():
        raise TimeoutError(
            "Siri TTS timed out after %d seconds" % timeout_seconds
        )


_cached_voices = None

_TYPE_MAP = {4: "neural", 5: "neuralAX", 6: "natural"}
_TYPE_RMAP = {"neural": 4, "neuralAX": 5, "natural": 6}
_GENDER_MAP = {1: "male", 2: "female", 3: "neutral"}
# Higher = better quality. Used to pick the best variant when a name has duplicates.
_TYPE_RANK = {"natural": 2, "neural": 1, "neuralAX": 0}


def _verify_voice(session, voice_obj):
    """
    Query, specific. Ask sirittsd to resolve a voice and check it won't fall back.

    Uses getSynthesisVoiceMatching:reply: to see what voice the daemon would
    actually use. If the resolved name differs from what we asked for, the
    voice would fall back at synthesis time.

    Args:
        session: SiriTTSDaemonSession instance
        voice_obj: SiriTTSSynthesisVoice to verify

    Returns:
        bool: True if the daemon resolves to the same voice (no fallback)
    """
    done = threading.Event()
    result = [None]

    def on_reply(resolved_voice, error):
        if resolved_voice is not None:
            result[0] = str(resolved_voice.name())
        done.set()

    session.getSynthesisVoiceMatching_reply_(voice_obj, on_reply)

    import Foundation
    run_loop = Foundation.NSRunLoop.currentRunLoop()
    deadline = time.time() + 2
    while not done.is_set() and time.time() < deadline:
        run_loop.runUntilDate_(
            Foundation.NSDate.dateWithTimeIntervalSinceNow_(0.02)
        )

    if not done.is_set():
        return False

    requested = str(voice_obj.name())
    return result[0] == requested


def _list_voices(verify=True):
    """
    Query, specific. List downloaded Siri voices, optionally filtering out fallbacks.

    When verify=True (default), each voice is checked via getSynthesisVoiceMatching
    to confirm the daemon would actually use it and not silently substitute another.
    Cached after first call.

    Deduplicates voices that appear under multiple quality tiers (e.g. Simone exists
    as both 'natural' and 'neural'). Keeps only the highest quality variant per
    (name, language) pair. Ranking: natural > neural > neuralAX.

    Args:
        verify (bool): If True, exclude voices that would fall back. Adds ~500ms
            on first call (all voices checked via XPC, ~20ms each).

    Returns:
        list of dict: each with keys 'name', 'language', 'type', 'gender'
            type is one of: 'natural' (6), 'neuralAX' (5), 'neural' (4)
            gender is one of: 'male' (1), 'female' (2), 'neutral' (3)

    Examples:
        >>> # Returns list of dicts like:
        >>> # [{'name': 'Aaron', 'language': 'en-US', 'type': 'natural', 'gender': 'male'}, ...]
    """
    global _cached_voices
    if _cached_voices is not None:
        return _cached_voices

    _ensure_framework()

    import objc

    DaemonSession = objc.lookUpClass("SiriTTSDaemonSession")
    SynthVoice = objc.lookUpClass("SiriTTSSynthesisVoice")
    session = DaemonSession.alloc().init()

    raw_voices = []
    done = threading.Event()

    def on_reply(voice_list):
        if voice_list:
            for v in voice_list:
                raw_voices.append(v)
        done.set()

    session.downloadedVoicesMatching_reply_(None, on_reply)
    _pump_runloop(done, 5)

    # Build dicts, deduplicating by (name, language) — keep highest quality type
    best = {}  # (name, language) -> voice dict
    for v in raw_voices:
        name = str(v.name())
        lang = str(v.language())
        vtype = _TYPE_MAP.get(v.type(), "unknown_%d" % v.type())

        if verify:
            test_voice = SynthVoice.alloc().initWithLanguage_name_(lang, name)
            if not _verify_voice(session, test_voice):
                continue

        key = (name, lang)
        rank = _TYPE_RANK.get(vtype, -1)
        existing = best.get(key)
        if existing is None or rank > _TYPE_RANK.get(existing["type"], -1):
            best[key] = {
                "name": name,
                "language": lang,
                "type": vtype,
                "gender": _GENDER_MAP.get(v.gender(), "unknown_%d" % v.gender()),
            }

    voices = list(best.values())
    _cached_voices = voices
    return voices


def _resolve_voice(voice_name):
    """
    Query, specific. Look up language and type for a voice name from the cached voice list.

    Returns the best-quality variant when duplicates exist (natural > neural > neuralAX).

    Args:
        voice_name (str): e.g. "Aaron", "Martha"

    Returns:
        tuple: (language, type_str) e.g. ("en-US", "natural"), ("en-GB", "natural")

    Raises:
        ValueError: if voice_name not found in downloaded voices

    Examples:
        >>> # _resolve_voice("Aaron") -> ("en-US", "natural")
        >>> # _resolve_voice("Martha") -> ("en-GB", "natural")
    """
    for v in _list_voices(verify=False):
        if v["name"] == voice_name:
            return v["language"], v["type"]
    raise ValueError(
        "Voice '%s' not found in downloaded Siri voices. "
        "Available: %s" % (voice_name, ", ".join(v["name"] for v in _list_voices(verify=False)))
    )


def _synthesize(text, voice_name, language=None, rate=1.0, pitch=1.0, volume=1.0):
    """
    Command, specific. Synthesize text to 48kHz 16-bit mono PCM bytes using a Siri voice.

    The sirittsd daemon streams audio via callbacks. The ASBD (AudioStreamBasicDescription)
    on each callback determines the format — either LPCM (raw PCM) or Opus (needs decoding).
    This function handles both transparently.

    When language is None (default), auto-resolves both language and voice type from
    _list_voices(). The voice type is pinned on the SiriTTSSynthesisVoice object so
    the daemon uses the best available variant (natural > neural > neuralAX) rather
    than picking arbitrarily when a name has multiple tiers (e.g. Simone).

    Args:
        text (str): Text to speak
        voice_name (str): Capitalized voice name, e.g. "Aaron", "Martha", "Simone"
        language (str or None): BCP-47 language tag. Auto-detected if None.
        rate (float): Speech rate multiplier (default 1.0)
        pitch (float): Pitch multiplier (default 1.0)
        volume (float): Volume 0.0-1.0 (default 1.0)

    Returns:
        tuple: (pcm_bytes, sample_rate) — raw 16-bit signed LE mono PCM and its sample rate

    Raises:
        TimeoutError: if synthesis takes longer than 30 seconds
        RuntimeError: if sirittsd returns an error or unknown audio format
        ValueError: if voice_name not found in downloaded voices
    """
    voice_type = None
    if language is None:
        language, voice_type = _resolve_voice(voice_name)

    _ensure_framework()

    import objc

    DaemonSession = objc.lookUpClass("SiriTTSDaemonSession")
    SynthVoice = objc.lookUpClass("SiriTTSSynthesisVoice")
    SynthRequest = objc.lookUpClass("SiriTTSSynthesisRequest")

    voice = SynthVoice.alloc().initWithLanguage_name_(language, voice_name)
    # Pin to the best quality type so the daemon doesn't pick a worse variant
    if voice_type is not None and voice_type in _TYPE_RMAP:
        voice.setType_(_TYPE_RMAP[voice_type])
    request = SynthRequest.alloc().initWithText_voice_(text, voice)
    ctx = request.synthesisContext()

    ctx.setRate_(rate)
    ctx.setPitch_(pitch)
    ctx.setVolume_(volume)

    # Prevent sirittsd from silently falling back to a compact/lower-quality voice
    # when under thermal pressure or resource constraints
    ctx.setDisableCompactVoice_(True)
    ctx.setDisableThermalFallback_(True)

    # Collect audio chunks and detect format from ASBD
    lpcm_parts = []
    opus_chunks = []
    format_ref = [None]  # will be set from first non-empty callback
    sample_rate_ref = [48000]
    done = threading.Event()
    error_ref = [None]

    def on_audio(audio_data):
        raw = audio_data.audioData()
        if not raw or len(raw) == 0:
            return
        raw_bytes = bytes(raw)

        # Read ASBD to determine format (only need to detect once)
        if format_ref[0] is None:
            try:
                asbd = audio_data.asbd()
                # asbd is a 9-tuple: (sampleRate, formatID, formatFlags,
                #   bytesPerPacket, framesPerPacket, bytesPerFrame,
                #   channelsPerFrame, bitsPerChannel, reserved)
                format_ref[0] = int(asbd[1])
                sample_rate_ref[0] = int(asbd[0])
            except Exception:
                # If we can't read ASBD, assume LPCM
                format_ref[0] = _FMT_LPCM

        if format_ref[0] == _FMT_LPCM:
            lpcm_parts.append(raw_bytes)
        elif format_ref[0] == _FMT_OPUS:
            pkt = audio_data.packetDescriptions()
            pkt_bytes = bytes(pkt) if pkt else b""
            opus_chunks.append((raw_bytes, pkt_bytes))
        else:
            # Unknown format — collect as raw and hope for the best
            lpcm_parts.append(raw_bytes)

    ctx.setDidGenerateAudio_(on_audio)

    def on_done(error):
        if error is not None:
            error_ref[0] = str(error)
        done.set()

    session = DaemonSession.alloc().init()
    session.synthesizeWithRequest_didFinish_(request, on_done)

    _pump_runloop(done, 30)

    if error_ref[0] is not None:
        raise RuntimeError("Siri TTS error: %s" % error_ref[0])

    sample_rate = sample_rate_ref[0]

    if format_ref[0] == _FMT_OPUS:
        pcm = _decode_opus_chunks(opus_chunks, sample_rate)
    else:
        pcm = b"".join(lpcm_parts)

    return pcm, sample_rate


def list_voice_names():
    """
    Query, specific. List available Siri voice names, sorted alphabetically then by tier.

    Returns only names that are downloaded and verified to not fall back.
    Deduplicated — if a voice exists in multiple tiers, only the best is kept.
    Sorted alphabetically first, then stably sorted so natural voices come before
    neural, which come before neuralAX.

    Returns:
        list of str: voice names, e.g. ["Aaron", "Arthur", "Catherine", ...]

    Examples:
        >>> # list_voice_names() -> ["Aaron", "Arthur", "Catherine", "Damon", ...]
    """
    voices = _list_voices()
    # Sort alphabetically by name
    voices = sorted(voices, key=lambda v: v["name"].lower())
    # Stable sort by tier: natural first, then neural, then neuralAX
    voices = sorted(voices, key=lambda v: _TYPE_RANK.get(v["type"], -1), reverse=True)
    return [v["name"] for v in voices]


def text_to_speech(text, voice="Aaron", rate=1.0, pitch=1.0, volume=1.0, output_path=None):
    """
    Command, specific. Speak text using a Siri voice, or save to WAV file.

    If output_path is None, plays audio through the default output device via afplay.
    If output_path is given, saves a WAV file at the detected sample rate.
    Language is auto-detected from the voice name.

    Use list_voice_names() to get available voices. Which voices are available
    depends on what's downloaded in System Settings > Accessibility > Spoken Content.
    Example output on a machine with all English Siri voices downloaded:

        >>> list_voice_names()
        ['Aaron', 'Aidan', 'Arthur', 'Catherine', 'Damon', 'en-AU-C',
         'en-AU-D', 'en-GB-C', 'en-GB-D', 'Gordon', 'Leona', 'Maeve',
         'Martha', 'Quinn', 'Simone', 'Xander',  # natural tier
         'Nora',                                   # neural tier
         'Aman', 'Aru', 'Ona', 'Tara']             # neuralAX tier

    Args:
        text (str): Text to speak
        voice (str): Voice name from list_voice_names(), e.g. "Aaron", "Martha"
        rate (float): Speech rate multiplier (default 1.0). <1 slower, >1 faster.
        pitch (float): Pitch multiplier (default 1.0). <1 lower, >1 higher.
        volume (float): Volume 0.0-1.0 (default 1.0)
        output_path (str or None): Path to save WAV file, or None to play immediately

    Returns:
        str or None: output_path if saving, None if playing

    Raises:
        TimeoutError: if synthesis exceeds 30 seconds
        RuntimeError: if sirittsd returns an error or voice not downloaded
        ValueError: if voice not found in downloaded voices

    Examples:
        >>> text_to_speech("Hello world", voice="Aaron")           # plays immediately
        >>> text_to_speech("Hello", voice="Martha", rate=0.8)      # slower British voice
        >>> text_to_speech("Hi", voice="Simone", output_path="/tmp/out.wav")  # save WAV
        '/tmp/out.wav'
    """
    pcm, sample_rate = _synthesize(text, voice, rate=rate, pitch=pitch, volume=volume)

    if not pcm:
        raise RuntimeError(
            "Siri TTS returned empty audio for voice '%s'. "
            "Is the voice downloaded in System Settings > Accessibility > Spoken Content?"
            % voice
        )

    if output_path is not None:
        wav_path = output_path
    else:
        wav_path = tempfile.mktemp(suffix=".wav", prefix="siri_tts_")

    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(_SIRI_CHANNELS)
        wf.setsampwidth(_SIRI_SAMPLE_WIDTH)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm)

    if output_path is not None:
        return output_path

    # Play and clean up
    try:
        subprocess.run(["afplay", wav_path], check=True)
    finally:
        if os.path.exists(wav_path):
            os.unlink(wav_path)

    return None


# ---------------------------------------------------------------------------
# CLI — fire-based
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import fire

    def speak(text, voice="Aaron", rate=1.0, pitch=1.0, volume=1.0, output=None):
        """Speak text using a Siri voice, or save to WAV."""
        result = text_to_speech(
            text, voice=voice, rate=rate, pitch=pitch, volume=volume, output_path=output
        )
        if result:
            print("Saved: %s" % result)

    def voices():
        """List available Siri voice names."""
        for name in list_voice_names():
            print(name)

    fire.Fire({"speak": speak, "voices": voices})
