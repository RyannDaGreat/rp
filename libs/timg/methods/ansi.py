import numpy as np
import io

# Try to use CFFI for native code acceleration if available
try:
    from cffi import FFI
    ffi = FFI()
    ffi.cdef("""
    void render_ansi_block(
        unsigned char* img_data, int width, int height, int channels,
        char* output_buffer, int buffer_size, int* output_length
    );
    """)
    
    # Define C implementation for ultra-fast rendering
    c_code = """
    void render_ansi_block(
        unsigned char* img_data, int width, int height, int channels,
        char* output_buffer, int buffer_size, int* output_length
    ) {
        // Ensure even height for pairing pixels
        if (height % 2 != 0) height -= 1;
        
        // Track position in output buffer
        int pos = 0;
        
        // Process the image in pairs of rows
        for (int y = 0; y < height; y += 2) {
            for (int x = 0; x < width; x++) {
                // Get upper and lower pixel colors
                int upper_idx = (y * width + x) * channels;
                int lower_idx = ((y+1) * width + x) * channels;
                
                // Write FG color sequence
                pos += sprintf(output_buffer + pos, "\\033[38;2;%d;%d;%dm", 
                    img_data[lower_idx], img_data[lower_idx+1], img_data[lower_idx+2]);
                
                // Write BG color sequence
                pos += sprintf(output_buffer + pos, "\\033[48;2;%d;%d;%dm", 
                    img_data[upper_idx], img_data[upper_idx+1], img_data[upper_idx+2]);
                
                // Write block character
                pos += sprintf(output_buffer + pos, "▄");
            }
            
            // Add reset and newline
            pos += sprintf(output_buffer + pos, "\\033[0m\\n");
        }
        
        // Set output length
        *output_length = pos;
    }
    """
    
    # Compile the C code
    lib = ffi.verify(c_code)
    HAS_CFFI = True
except ImportError:
    HAS_CFFI = False
    pass

class ANSIMethod:
  TRAILER = '\033[0m'
  BLOCK_CHAR = "▄"
  
  @staticmethod
  def rgb8(r, g, b):
    '''Return 8-bit color code from an rgb value'''
    # If grayscale
    if abs(r-g) < 10 and abs(r-b) < 10 and abs(g-b) < 10:
      avg = (r+g+b)/3
      grayscale_step = int(avg/10.625) - 1
      return 232 + grayscale_step
    
    # Color mode
    r_, g_, b_ = int(r/51), int(g/51), int(b/51)
    return 16 + 36*r_ + 6*g_ + b_

  @staticmethod
  def fg8(r, g, b):
    '''Return 8-bit fg color ANSI escape sequence from an rgb value'''
    return '\033[38;5;{}m'.format(ANSIMethod.rgb8(r, g, b))

  @staticmethod
  def bg8(r, g, b):
    '''Return 8-bit bg color ANSI escape sequence from an rgb value'''
    return "\033[48;5;{}m".format(ANSIMethod.rgb8(r, g, b))

  @staticmethod
  def fg24(r, g, b):
    '''Return 24-bit fg color ANSI escape sequence from an rgb value'''
    return f"\033[38;2;{r};{g};{b}m"

  @staticmethod
  def bg24(r, g, b):
    '''Return 24-bit bg color ANSI escape sequence from an rgb value'''
    return f"\033[48;2;{r};{g};{b}m"

  def __init__(self, image):
    self.image = image
    self._color_cache = {}

  def c_optimized_render(self):
    """Ultra-fast ANSI rendering using native C code"""
    # Get image as contiguous numpy array
    img = np.array(self.image, dtype=np.uint8, order='C')
    height, width, channels = img.shape
    
    # Calculate maximum buffer size needed
    # Each pixel needs ~25 bytes for ANSI sequences
    buffer_size = width * height * 25
    
    # Create output buffer and length variable
    output_buffer = ffi.new(f"char[{buffer_size}]")
    output_length = ffi.new("int*")
    
    # Get pointer to image data
    img_ptr = ffi.cast("unsigned char*", img.ctypes.data)
    
    # Call C function to render ANSI blocks
    lib.render_ansi_block(img_ptr, width, height, channels, 
                         output_buffer, buffer_size, output_length)
    
    # Get result as Python string
    result = ffi.string(output_buffer, output_length[0]).decode('utf8')
    
    return result

  def efficient_rendering(self):
    """Efficient Python implementation with StringIO"""
    # Get image as numpy array
    img = np.array(self.image)
    height, width, channels = img.shape
    
    # Ensure even height
    if height % 2 != 0:
        height -= 1
    
    # Create buffer for output
    output = io.StringIO()
    cache = {}
    
    # Process rows
    for y in range(0, height, 2):
        for x in range(width):
            # Get colors
            fg_color = tuple(map(int, img[y+1, x, :3]))
            bg_color = tuple(map(int, img[y, x, :3]))
            
            # Get or build color sequences
            fg_key = ('fg', fg_color)
            if fg_key not in cache:
                cache[fg_key] = f"\033[38;2;{fg_color[0]};{fg_color[1]};{fg_color[2]}m"
                
            bg_key = ('bg', bg_color)
            if bg_key not in cache:
                cache[bg_key] = f"\033[48;2;{bg_color[0]};{bg_color[1]};{bg_color[2]}m"
            
            # Write to buffer
            output.write(cache[fg_key])
            output.write(cache[bg_key])
            output.write(ANSIMethod.BLOCK_CHAR)
        
        # End line
        output.write(ANSIMethod.TRAILER)
        output.write('\n')
    
    # Return result
    return output.getvalue().rstrip('\n')

  def to_block(self, bits, hblock=False):
    # Use optimized implementation for 24-bit hblock mode
    if bits == 24 and hblock:
        if HAS_CFFI:
            try:
                # Use C implementation if available
                return self.c_optimized_render()
            except Exception:
                pass
                
        # Fallback to Python implementation
        return self.efficient_rendering()
    
    # Regular implementation for other modes
    w, h = self.image.size
    pix = self.image.load()
    string = ''
    
    for y in range(0, h, 2):
      for x in range(w):
        try:
          fg_color = pix[x, y+1][:3] if y+1 < h else pix[x, y][:3]
          bg_color = pix[x, y][:3]
        except IndexError:
          continue
        
        if bits == 8:
          fg, bg = (
            ANSIMethod.fg8(*fg_color),
            ANSIMethod.bg8(*bg_color))
        elif bits == 24:
          fg, bg = (
            ANSIMethod.fg24(*fg_color),
            ANSIMethod.bg24(*bg_color))
        
        if hblock:
          string += '{}{}▄'.format(fg, bg)
        else:
          string += '{} '.format(bg)
      string += '{}\n'.format(ANSIMethod.TRAILER)
    
    return string

  def to_8_bit_hblock(self):
    return self.to_block(8, hblock=True)

  def to_24_bit_hblock(self):
    return self.to_block(24, hblock=True)

  def to_8_bit_fblock(self):
    return self.to_block(8, hblock=False)

  def to_24_bit_fblock(self):
    return self.to_block(24, hblock=False)