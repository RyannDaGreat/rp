"""
SuperTonic TTS server - lightning-fast on-device TTS (66M params, 167x realtime).

USAGE:
    python -m rp.libs.supertonic_tts_server run_server [--port=7123]
    python -m rp.libs.supertonic_tts_server ensure_server [--port=7123]

PYTHON API:
    import rp
    rp.text_to_speech_via_supertonic("Hello world")
    rp.text_to_speech_via_supertonic("Fast", speed=2.0, voice="M1", volume=1.5)
    rp.text_to_speech_via_supertonic_set_defaults(voice="F2", speed=1.5, volume=1.0)
    rp.text_to_speech_via_supertonic_get_defaults()

HTTP API ENDPOINTS:
    All endpoints return JSON. Server runs on localhost:7123 by default.

    GET /health
        Health check. Returns {"status": "ok", "tts": "supertonic", "voices": [...]}

    GET /defaults
        Get current default settings.
        Returns: {"voice": "F1", "speed": 1.5, "volume": 1.0, "steps": 5}

    GET /set_defaults?voice=F1&speed=1.5&volume=1.0&steps=5
        Set default voice, speed, volume, and/or steps (persists for all clients).
        Parameters (all optional):
            voice: F1-F5 (female) or M1-M5 (male)
            speed: 0.7 to 2.0 (float)
            volume: 0.0 to 2.0 (float, 1.0 = normal)
            steps: 1 to 10 (int, quality - higher = better but slower)
        Returns: {"ok": true, "defaults": {"voice": "F1", "speed": 1.5, "volume": 1.0, "steps": 5}}

    GET /speak?text=Hello&voice=F1&speed=1.5&volume=1.0&steps=5
        Synthesize and play text through speakers.
        Parameters:
            text: (required) Text to speak
            voice: (optional) F1-F5 or M1-M5, defaults to server default
            speed: (optional) 0.7-2.0, defaults to server default
            volume: (optional) 0.0-2.0, defaults to server default
            steps: (optional) 1-10, quality steps, defaults to server default
        Returns: {"ok": true, "duration": 1.23, "text": "Hello", "voice": "F1", "speed": 1.5, "volume": 1.0, "steps": 5}

    POST /speak
        Same as GET but with JSON body: {"text": "Hello", "voice": "F1", "speed": 1.5, "volume": 1.0, "steps": 5}

CURL EXAMPLES:
    # Health check
    curl http://localhost:7123/health

    # Speak text (URL-encoded)
    curl "http://localhost:7123/speak?text=Hello%20world"

    # Speak with custom voice, speed, and volume
    curl "http://localhost:7123/speak?text=Fast%20speech&voice=M1&speed=2.0&volume=1.5"

    # Set defaults for all future requests
    curl "http://localhost:7123/set_defaults?voice=F2&speed=1.8&volume=1.0"

    # Get current defaults
    curl http://localhost:7123/defaults

    # POST with JSON body
    curl -X POST http://localhost:7123/speak -H "Content-Type: application/json" -d '{"text": "Hello"}'

VOICES:
    Female: F1, F2, F3, F4, F5
    Male:   M1, M2, M3, M4, M5

SPEED:
    Range: 0.7 (slow) to 2.0 (fast)
    Default: 1.5
    Normal speech: 1.0

VOLUME:
    Range: 0.0 (mute) to 2.0 (loud)
    Default: 1.0
    Normal: 1.0

STEPS (Quality):
    Range: 1 (fast/low quality) to 10 (slow/high quality)
    Default: 5
    Recommended: 3-5 for real-time, 8-10 for offline generation
"""
import sys

TMUX_SESSION = 'SuperTonicTTS'
DEFAULT_PORT = 7123
VOICES = ['F1', 'F2', 'F3', 'F4', 'F5', 'M1', 'M2', 'M3', 'M4', 'M5']

# Defaults that can be changed at runtime
_defaults = {
    'voice': 'F1',
    'speed': 1.5,
    'volume': 1.0,
    'steps': 5,  # Quality: 1-10, higher = better quality but slower
}


def set_defaults(voice=None, speed=None, volume=None, steps=None):
    """Set default voice, speed, volume, and steps for TTS requests."""
    if voice is not None:
        if voice not in VOICES:
            raise ValueError(f'Invalid voice: {voice}. Choose from: {", ".join(VOICES)}')
        _defaults['voice'] = voice
    if speed is not None:
        if not 0.7 <= speed <= 2.0:
            raise ValueError(f'Speed must be between 0.7 and 2.0, got {speed}')
        _defaults['speed'] = speed
    if volume is not None:
        if not 0.0 <= volume <= 2.0:
            raise ValueError(f'Volume must be between 0.0 and 2.0, got {volume}')
        _defaults['volume'] = volume
    if steps is not None:
        if not 1 <= steps <= 10:
            raise ValueError(f'Steps must be between 1 and 10, got {steps}')
        _defaults['steps'] = steps


def get_defaults():
    """Get current default settings."""
    return _defaults.copy()


def _get_port_from_tmux():
    """Get port from tmux window name if session exists and server is responding."""
    import rp
    if TMUX_SESSION not in rp.tmux_get_all_session_names():
        return None
    # Window name contains port
    window_name = rp.shell_command(
        f'tmux list-windows -t {TMUX_SESSION} -F "#{{window_name}}" 2>/dev/null'
    ).strip().split('\n')[0]
    try:
        port = int(window_name)
    except (ValueError, IndexError):
        return None
    # Check if responding
    if rp.shell_command(
        f'curl -s -o /dev/null -w "%{{http_code}}" http://localhost:{port}/health 2>/dev/null'
    ).strip() == '200':
        return port
    return None


def ensure_server(port=DEFAULT_PORT):
    """Ensure server is running. Returns port."""
    import rp

    # Check if already running
    existing_port = _get_port_from_tmux()
    if existing_port:
        return existing_port

    # Kill stale session
    if TMUX_SESSION in rp.tmux_get_all_session_names():
        rp.tmux_kill_session(TMUX_SESSION)

    # Find free port
    port = rp.get_next_free_port(port)

    # Start in tmux with window name = port
    cmd = f'{sys.executable} -m rp.libs.supertonic_tts_server run_server --port={port}'
    rp.shell_command(f'tmux new-session -d -s {TMUX_SESSION} -n {port} {rp.shlex.quote(cmd)}')

    # Wait for ready (SuperTonic takes longer to load model)
    print(f'[supertonic_tts] Starting server on port {port}...')
    for i in range(120):  # Up to 60 seconds
        if rp.shell_command(
            f'curl -s -o /dev/null -w "%{{http_code}}" http://localhost:{port}/health 2>/dev/null'
        ).strip() == '200':
            print(f'[supertonic_tts] Server ready on port {port}')
            return port
        rp.sleep(0.5)

    raise RuntimeError(f'SuperTonic TTS server failed to start on port {port}')


def run_server(port=DEFAULT_PORT):
    """Run the server (blocking)."""
    import rp

    # Ensure dependencies are installed
    print('[supertonic_tts] Checking dependencies...')
    rp.pip_import('supertonic', auto_yes=True)
    rp.pip_import('sounddevice', auto_yes=True)
    rp.pip_import('numpy', auto_yes=True)

    # Now import normally
    import http.server
    import json
    import socketserver
    import urllib.parse
    import numpy as np
    import sounddevice as sd
    from supertonic import TTS

    print('[supertonic_tts] Loading model (~305MB on first run)...')
    tts = TTS(auto_download=True)
    print(f'[supertonic_tts] Model loaded. Sample rate: {tts.sample_rate}Hz')
    print(f'[supertonic_tts] Voices: {tts.voice_style_names}')

    voice_styles = {v: tts.get_voice_style(voice_name=v) for v in tts.voice_style_names}

    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            print(f'[supertonic_tts] {args[0]}')

        def _send_json(self, data, status=200):
            body = json.dumps(data).encode()
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(body))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)

            if parsed.path == '/health':
                self._send_json({'status': 'ok', 'tts': 'supertonic', 'voices': VOICES})
                return

            if parsed.path == '/defaults':
                self._send_json(_defaults)
                return

            if parsed.path == '/set_defaults':
                voice = params.get('voice', [None])[0]
                speed = params.get('speed', [None])[0]
                volume = params.get('volume', [None])[0]
                steps = params.get('steps', [None])[0]
                try:
                    set_defaults(
                        voice=voice,
                        speed=float(speed) if speed else None,
                        volume=float(volume) if volume else None,
                        steps=int(steps) if steps else None
                    )
                    self._send_json({'ok': True, 'defaults': _defaults})
                except ValueError as e:
                    self._send_json({'error': str(e)}, 400)
                return

            if parsed.path != '/speak':
                self._send_json({'error': 'Use GET /speak?text=...'}, 404)
                return

            text = params.get('text', [''])[0]
            voice = params.get('voice', [_defaults['voice']])[0]
            speed_str = params.get('speed', [None])[0]
            speed = float(speed_str) if speed_str else _defaults['speed']
            volume_str = params.get('volume', [None])[0]
            volume = float(volume_str) if volume_str else _defaults['volume']
            steps_str = params.get('steps', [None])[0]
            steps = int(steps_str) if steps_str else _defaults['steps']

            if not text:
                self._send_json({'error': 'Missing text parameter'}, 400)
                return

            if voice not in voice_styles:
                self._send_json({'error': f'Invalid voice: {voice}'}, 400)
                return

            try:
                wav, duration = tts.synthesize(
                    text,
                    voice_style=voice_styles[voice],
                    lang='en',
                    speed=speed,
                    total_steps=steps
                )
                wav = np.squeeze(wav)
                # Apply volume scaling
                if volume != 1.0:
                    wav = wav * volume
                sd.play(wav, samplerate=tts.sample_rate)
                sd.wait()
                dur = float(duration[0]) if hasattr(duration, '__getitem__') else float(duration)
                self._send_json({'ok': True, 'duration': dur, 'text': text, 'voice': voice, 'speed': speed, 'volume': volume, 'steps': steps})
            except Exception as e:
                self._send_json({'error': str(e)}, 500)

        def do_POST(self):
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode()

            try:
                data = json.loads(body) if body else {}
            except json.JSONDecodeError:
                data = {'text': body}

            # Redirect to GET handler with params
            text = data.get('text', '')
            voice = data.get('voice', _defaults['voice'])
            speed = data.get('speed', _defaults['speed'])

            self.path = f'/speak?text={urllib.parse.quote(text)}&voice={voice}&speed={speed}'
            self.do_GET()

    class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        allow_reuse_address = True

    with ThreadedServer(('0.0.0.0', port), Handler) as server:
        print(f'[supertonic_tts] Ready on http://localhost:{port}')
        server.serve_forever()


if __name__ == '__main__':
    import rp
    rp.pip_import('fire')
    import fire
    fire.Fire()
