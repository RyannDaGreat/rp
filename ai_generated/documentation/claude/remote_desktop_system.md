# RP Remote Desktop System

## Overview
**Files**: `remote_desktop_client.py`, `remote_desktop_server.py`  
**Type**: Standalone remote control system (uses web_evaluator)  
**Purpose**: Stream desktop with real-time mouse/keyboard control over network

## Integration Points
- **Dependencies**: Uses `rp.web_evaluator` for client-server communication
- **Video streaming**: Uses `rp.libs.video_streaming.video_codec_streams` for VP9 encoding
- **Usage**: Both components use web_evaluator: client connects to server's web_evaluator instance

## Architecture
A client-server system that provides remote desktop functionality using RP's web evaluator framework and video streaming capabilities.

## Server Component (`remote_desktop_server.py`)

### Functionality
Minimal server that provides remote desktop access by running a web evaluator server.

```python
import rp.web_evaluator

print("Starting RP Remote Desktop Server...")
rp.web_evaluator.run_server()
print("Server stopped.")
```

### How It Works
- Runs `rp.web_evaluator.run_server()` on default port (43234)
- Automatically exposes all RP functions including:
  - `rp.load_image_from_screenshot()`
  - `rp.set_mouse_position()`
  - `rp.mouse_left_press()`/`rp.mouse_left_release()`
  - Keyboard control via `pynput`

### Setup
```bash
# On the server machine
python -m rp.remote_desktop_server
# Or
python remote_desktop_server.py
```

## Client Component (`remote_desktop_client.py`)

### Core Features
- **Real-time video streaming** using VP9 codec
- **Mouse control** with coordinate mapping
- **Keyboard control** with full key support
- **Dynamic window resizing** with stream restart
- **Connection monitoring** and automatic recovery

### Configuration
```python
SERVER_IP = "127.0.0.1"      # Local testing
SERVER_IP = "glass.clarinet" # Network hostname  
SERVER_IP = "24.185.152.190" # Internet IP
```

### Main Components

#### Video Streaming System
```python
# Uses RP's video streaming library
from rp.libs.video_streaming import video_codec_streams

codec = 'VP9'
decoder = video_codec_streams.VideoStreamDecoder(codec)

# Server-side encoder setup
encoder = video_codec_streams.VideoStreamEncoder(codec)
chunk_stream = encoder.encode_video(get_frames(width, height))
```

#### Screenshot Capture (Server-side)
```python
def get_frames(width, height):
    '''Generator that captures, resizes, and yields frames.'''
    while True:
        try:
            frame = rp.load_image_from_screenshot_via_mss(monitor_number)
            # Resize on server to save bandwidth
            yield rp.cv_resize_image(frame, (height, width), interp='area')
        except Exception:
            break
```

#### Mouse Control
```python
# Normalize coordinates for different resolutions
norm_x, norm_y = event.pos[0] / w, event.pos[1] / h

# Map to remote screen coordinates
code = f"""
    abs_x = norm_x * {remote_w}
    abs_y = norm_y * {remote_h}
    rp.set_mouse_position(abs_x, abs_y)
    rp.mouse_left_press()  # or mouse_left_release()
"""
client.evaluate(code, norm_x=norm_x, norm_y=norm_y)
```

#### Keyboard Control
```python
# Server-side keyboard controller (persistent)
from pynput.keyboard import Key, Controller
keyboard = Controller()

# Key mapping for special keys
key_map = {name: getattr(Key, name) for name in [
    'backspace', 'tab', 'enter', 'esc', 'space', 'delete',
    'up', 'down', 'left', 'right', 'home', 'end', 'page_up', 'page_down',
    'shift_l', 'shift_r', 'ctrl_l', 'ctrl_r', 'alt_l', 'alt_r',
    'caps_lock', 'cmd', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7',
    'f8', 'f9', 'f10', 'f11', 'f12'
]}

# Key press/release
key_to_act_on = key_map.get(key_name, key_name)
keyboard.press(key_to_act_on)  # or keyboard.release(key_to_act_on)
```

## Usage

### Server Setup
```bash
# Terminal 1: Start the server
cd /path/to/rp
python remote_desktop_server.py
```

### Client Connection
```bash
# Terminal 2: Connect from client machine
cd /path/to/rp
python remote_desktop_client.py
```

### Interactive Control
1. **Video Display**: Real-time screen streaming in resizable window
2. **Mouse Control**: Click and drag in client window controls remote mouse
3. **Keyboard Input**: Type in client window, keys sent to remote machine
4. **Window Resize**: Automatically restarts stream with new resolution

## Technical Implementation

### Performance Optimizations

#### Bandwidth Reduction
- **Server-side resizing**: Images resized before transmission
- **VP9 compression**: Efficient video codec for screen content
- **Motion-only streaming**: Only sends changed regions

#### Resolution Handling
```python
# Client window size drives remote stream resolution
window_size = (1280, 800)
width, height = window_size

# Server captures at native resolution, resizes for transmission
remote_h, remote_w = get_image_dimensions(screenshot)
yield cv_resize_image(frame, (height, width), interp='area')
```

#### Connection Management
```python
def restart_stream():
    # Close previous encoder to free resources
    client.evaluate("if 'encoder' in locals(): encoder.close()")
    
    # Restart with new parameters
    setup_code = create_stream_setup_code()
    result = client.evaluate(setup_code, width=width, height=height)
```

### Error Handling

#### Stream Recovery
```python
try:
    chunk_result = client.evaluate("next(chunk_stream)")
    if chunk_result.errored:
        print("Stream ended or errored. Restarting...")
        restart_stream()
        continue
except Exception as e:
    print(f"Decode error: {e}. Restarting stream...")
    restart_stream()
```

#### Connection Resilience
```python
try:
    # Main event loop
    frames = decoder.decode_chunk(chunk)
    display_frame(frames[-1])
except Exception as e:
    print(f"Unexpected error: {e}. Attempting to restart stream.")
    try:
        restart_stream()
    except Exception as restart_e:
        print(f"Failed to restart stream: {restart_e}. Exiting.")
        running = False
```

## Dependencies

### Client Requirements
```python
import pygame  # Window management and input handling
from rp.libs.video_streaming import video_codec_streams  # Video decoding
import rp.web_evaluator  # Remote communication
```

### Server Requirements
```python
import rp.web_evaluator  # HTTP server
# Automatically includes:
# - mss (screenshot capture)
# - cv2 (image resizing) 
# - pynput (keyboard/mouse control)
# - video encoding libraries
```

## Performance Characteristics

### Bandwidth Usage
The system includes bandwidth monitoring:
```python
global total_bytes
total_bytes += len(chunk)
rp.fansi_print(rp.human_readable_file_size(total_bytes), 'green bold')
```

### Latency Factors
1. **Network latency**: Round-trip time for commands
2. **Video encoding**: VP9 compression on server
3. **Video decoding**: Client-side decompression  
4. **Screen capture**: Server screenshot frequency
5. **Input processing**: Mouse/keyboard event handling

## Security Considerations

### Network Security
- **No encryption**: All communication is plain HTTP
- **No authentication**: Server accepts any client connections
- **Full system access**: Client can execute arbitrary code on server

### Recommended Usage
- **Trusted networks only**: LAN or VPN environments
- **Firewall protection**: Restrict server port access
- **Temporary sessions**: Not intended for permanent deployment

## Limitations

### Platform Support
- **Server**: Requires desktop environment with screenshot capability
- **Client**: Requires Pygame and display capability
- **Input methods**: Currently only mouse left-click and basic keyboard

### Feature Limitations
- **Single monitor**: Only captures primary display
- **No audio**: Video streaming only
- **No file transfer**: Pure remote control functionality
- **No clipboard sync**: Cannot share clipboard between machines

## Potential Enhancements

### Advanced Input
```python
# Multi-button mouse support
elif event.button == 1:  # Left
    action = 'rp.mouse_left_press()'
elif event.button == 2:  # Middle  
    action = 'rp.mouse_middle_press()'
elif event.button == 3:  # Right
    action = 'rp.mouse_right_press()'

# Scroll wheel support
elif event.type == pygame.MOUSEWHEEL:
    client.evaluate(f"rp.scroll_mouse({event.y})")
```

### Multi-Monitor
```python
# Monitor selection
monitor_number = 1  # Secondary display
shot = lambda: rp.load_image_from_screenshot_via_mss(monitor_number)
```

### Security Improvements
```python
# Basic authentication
def secure_server():
    def auth_handler(request):
        if request.headers.get('Authorization') != 'Bearer secret-token':
            return 401
    
    rp.web_evaluator.run_server(auth_handler=auth_handler)
```

This remote desktop system demonstrates RP's capability to build sophisticated distributed applications using its web evaluator and media processing infrastructure.