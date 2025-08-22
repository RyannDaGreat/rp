# Google Colab Utilities

## Overview
**File**: `google_colab.py`  
**Type**: Standalone utility module  
**Purpose**: Helper function for displaying MP4 videos in Google Colab notebooks

## Functionality
Provides a simple utility to embed MP4 videos directly in Jupyter/Colab notebooks using base64 encoding.

## Core Function

### `mp4_to_html(path)`
Converts an MP4 video file to an HTML video element with embedded base64 data.

```python
def mp4_to_html(path):
    from base64 import b64encode
    mp4 = open(path,'rb').read()
    data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
    return("""
    <video width=800 controls>
        <source src="%s" type="video/mp4">
    </video>
    """ % data_url)
```

## Usage

### Basic Usage
```python
from rp.google_colab import mp4_to_html

# Convert video to HTML
html_video = mp4_to_html('my_video.mp4')

# Display in Jupyter/Colab
from IPython.display import HTML
HTML(html_video)
```

### Complete Example
```python
# In a Google Colab cell
from rp.google_colab import mp4_to_html
from IPython.display import HTML

# Generate or load a video file
video_path = 'output_video.mp4'

# Convert to displayable HTML
video_html = mp4_to_html(video_path)

# Display inline in notebook
HTML(video_html)
```

## How It Works

### 1. File Reading
Reads the entire MP4 file as binary data:
```python
mp4 = open(path,'rb').read()
```

### 2. Base64 Encoding
Converts binary data to base64 string:
```python
data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
```

### 3. HTML Generation
Creates an HTML5 video element with embedded data:
```html
<video width=800 controls>
    <source src="data:video/mp4;base64,AAAAHGZ0eXBpc29tAAACAGlzb21pc28yYXZjMW1wNDE..." type="video/mp4">
</video>
```

## Technical Details

### Data URI Format
Uses the standard data URI scheme:
```
data:[<mediatype>][;base64],<data>
```

Where:
- `mediatype`: `video/mp4`
- `encoding`: `base64` 
- `data`: Base64-encoded video content

### HTML Video Element
- **Width**: Fixed at 800px
- **Controls**: Shows play/pause, seek bar, volume controls
- **Source**: Embedded base64 data (no external file required)

## Advantages

### Self-Contained
- **No external dependencies**: Video data embedded in HTML
- **Portable notebooks**: No need to maintain separate video files
- **Version control friendly**: Single notebook file contains everything

### Colab Compatibility
- **No file uploads needed**: Video data included in notebook
- **Persistent across sessions**: Videos remain after runtime restart
- **Shareable**: Works when sharing notebooks with others

## Limitations

### File Size Constraints
- **Large files**: Base64 encoding increases size by ~33%
- **Memory usage**: Entire video loaded into memory
- **Notebook bloat**: Makes notebook files very large

### Performance Impact
- **Slow rendering**: Large base64 strings slow down notebook loading
- **Browser limitations**: Very large data URIs may fail in some browsers
- **No streaming**: Must load entire video before playback

## Best Practices

### Optimize Video Files
```python
# Use RP's video compression before embedding
import rp

# Compress video first
compressed_path = rp.compress_video_file(
    'large_video.mp4',
    output_path='small_video.mp4', 
    quality=0.7,
    max_resolution=(640, 480)
)

# Then embed the smaller file
html = mp4_to_html(compressed_path)
```

### Size Recommendations
```python
import os

def check_video_size(path, max_mb=10):
    """Check if video is suitable for embedding"""
    size_mb = os.path.getsize(path) / (1024 * 1024)
    if size_mb > max_mb:
        print(f"Warning: Video is {size_mb:.1f}MB, consider compressing")
        return False
    return True

# Usage
if check_video_size('my_video.mp4'):
    HTML(mp4_to_html('my_video.mp4'))
else:
    print("Video too large for embedding")
```

## Alternative Approaches

### External Hosting
```python
def mp4_to_html_external(url):
    """Use external URL instead of embedding"""
    return f"""
    <video width=800 controls>
        <source src="{url}" type="video/mp4">
    </video>
    """

# Usage with cloud storage
video_url = "https://storage.googleapis.com/my-bucket/video.mp4"
HTML(mp4_to_html_external(video_url))
```

### Progressive Enhancement
```python
def mp4_to_html_smart(path, max_size_mb=5):
    """Embed small videos, link large ones"""
    import os
    size_mb = os.path.getsize(path) / (1024 * 1024)
    
    if size_mb <= max_size_mb:
        # Embed small videos
        return mp4_to_html(path)
    else:
        # Link to large videos
        return f"""
        <p>Video too large to embed ({size_mb:.1f}MB)</p>
        <a href="{path}" target="_blank">Open video in new tab</a>
        """
```

## Integration with RP Workflows

### Video Generation Pipeline
```python
import rp
from rp.google_colab import mp4_to_html
from IPython.display import HTML

# Generate video using RP
images = rp.generate_image_sequence()
video_path = rp.images_to_video(images, 'output.mp4', fps=30)

# Optimize for embedding
compressed_path = rp.compress_video_for_web(video_path)

# Display in notebook
HTML(mp4_to_html(compressed_path))
```

### Machine Learning Visualization
```python
# Common use case: displaying training progress videos
def visualize_training_progress(model_checkpoints):
    for epoch, checkpoint in enumerate(model_checkpoints):
        # Generate visualization
        visualization = model.generate_sample(checkpoint)
        
        # Save as video
        video_path = f'training_epoch_{epoch}.mp4'
        rp.save_video(visualization, video_path)
        
        # Display inline
        print(f"Epoch {epoch}:")
        display(HTML(mp4_to_html(video_path)))
```

## Related RP Functions

### Video Processing
- `rp.images_to_video()`: Create videos from image sequences
- `rp.compress_video_file()`: Optimize file sizes
- `rp.get_video_info()`: Check video properties
- `rp.extract_video_frames()`: Convert videos back to images

### Colab Detection
```python
# Check if running in Colab (from main RP)
if rp.running_in_google_colab():
    # Use embedded videos
    HTML(mp4_to_html(video_path))
else:
    # Use local video player
    rp.display_video(video_path)
```

This utility demonstrates RP's focus on practical, simple solutions for common data science workflows in cloud environments.