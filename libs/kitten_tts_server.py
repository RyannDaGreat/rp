"""
Kitten TTS server.
Usage: python -m rp.libs.kitten_tts_server run_server [--port=32462]
       python -m rp.libs.kitten_tts_server ensure_server [--port=32462]
"""
import sys

TMUX_SESSION = 'KittenTTS'
DEFAULT_PORT = 32462

def _get_port_from_tmux():
    """Get port from tmux window name if session exists and server is responding."""
    import rp
    if TMUX_SESSION not in rp.tmux_get_all_session_names():
        return None
    # Window name contains port
    window_name = rp.shell_command('tmux list-windows -t ' + TMUX_SESSION + ' -F "#{window_name}" 2>/dev/null').strip().split('\n')[0]
    try:
        port = int(window_name)
    except (ValueError, IndexError):
        return None
    # Check if responding
    if rp.shell_command('curl -s -o /dev/null -w "%{http_code}" http://localhost:' + str(port) + '/ 2>/dev/null').strip() == '200':
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
    cmd = sys.executable + ' -m rp.libs.kitten_tts_server run_server --port=' + str(port)
    rp.shell_command('tmux new-session -d -s ' + TMUX_SESSION + ' -n ' + str(port) + ' ' + rp.shlex.quote(cmd))

    # Wait for ready
    for _ in range(60):
        if rp.shell_command('curl -s -o /dev/null -w "%{http_code}" http://localhost:' + str(port) + '/ 2>/dev/null').strip() == '200':
            return port
        rp.sleep(0.5)

    raise RuntimeError('Kitten TTS server failed to start on port ' + str(port))

def run_server(port=DEFAULT_PORT):
    """Run the server (blocking)."""
    import subprocess
    # Install deps - need specific onnxruntime version for opset compatibility
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-q',
        'https://github.com/KittenML/KittenTTS/releases/download/0.1/kittentts-0.1.0-py3-none-any.whl',
        'fastapi', 'uvicorn', 'websockets', 'numpy', 'onnxruntime>=1.20'], stderr=subprocess.DEVNULL)

    from fastapi import FastAPI, WebSocket, Query
    from fastapi.responses import HTMLResponse
    import uvicorn
    from kittentts import KittenTTS
    import numpy as np

    app = FastAPI()
    model = None

    @app.on_event("startup")
    async def load_model():
        nonlocal model
        print('[kitten_tts] Loading model...')
        model = KittenTTS('KittenML/kitten-tts-nano-0.1')
        print('[kitten_tts] Ready on port ' + str(port))

    @app.get("/")
    async def root():
        return HTMLResponse('<h1>Kitten TTS</h1>')

    @app.websocket("/stream")
    async def stream_tts(
        websocket: WebSocket,
        text: str = Query(...),
        voice: str = Query(default='expr-voice-3-f'),
        speed: float = Query(default=1.0)
    ):
        await websocket.accept()
        try:
            audio = model.generate(text, voice=voice, speed=speed)
            audio_bytes = (audio * 32767).astype(np.int16).tobytes()
            for i in range(0, len(audio_bytes), 9600):
                await websocket.send_bytes(audio_bytes[i:i + 9600])
        except Exception:
            pass
        await websocket.close()

    uvicorn.run(app, host='0.0.0.0', port=port)

if __name__ == '__main__':
    import rp
    rp.pip_import('fire')
    import fire
    fire.Fire()
