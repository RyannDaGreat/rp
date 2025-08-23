# RP Library: Math Scientific

Mathematical and scientific computing functions: algorithms, calculations, and numerical operations.

**Total Functions: 43**

## Function Inventory

| Function | Line | Description |
|----------|------|-------------|
| `is_numpy_array()` | 4637 | Checks if object is NumPy ndarray without requiring numpy import.  Enhanced Documentation: - Used fo... |
| `is_torch_tensor()` | 4657 | Checks if an object is a PyTorch tensor without requiring torch to be imported.  Enhanced Documentat... |
| `temporary_numpy_random_seed()` | 5271 | A context manager that sets the random seed for the duration of the context block using NumPy's rand... |
| `_load_image_from_file_via_scipy()` | 6185 | *(No description)* |
| `set_numpy_print_options()` | 7870 | np.set_printoptions is used to format the printed output of arrays. It makes the terminal output muc... |
| `matrix_to_tuples()` | 16414 | My attempt to analyze frequencies by taking the least-squares fit of a bunch of sinusoids to a signa... |
| `encode_float_matrix_to_rgba_byte_image()` | 16615 | Can encode a 32-bit float into the 4 channels of an RGBA image The values should be between 0 and 1 ... |
| `decode_float_matrix_from_rgba_byte_image()` | 16635 | This function is the inverse of encode_float_matrix_to_rgba_image Takes an rgba byte-image (that was... |
| `rotation_matrix()` | 29279 |  Set out_of to 360 to use degrees instead of radians  theta = angle/out_of*tau#Convert to radians c,... |
| `squared_distance_matrix()` | 29686 | if to_points is None, it defaults to from_points (returning a symmetric matrix) This function exists... |
| `distance_matrix()` | 29702 | if to_points is None, it defaults to from_points (returning a symmetric matrix) from_points and to_p... |
| `is_euclidean_affine_matrix()` | 30062 | mx+b in the complex plane corresponds to a euclidean transform This function takes a euclidean affin... |
| `is_affine_matrix()` | 30067 | mx+b in the complex plane corresponds to a euclidean transform This function takes a euclidean affin... |
| `_torch_tensor_to_bytes_for_hashing()` | 30140 | This function is really handy! Meant for hashing things that can't normally be hashed, like lists an... |
| `split_tensor_into_regions()` | 36104 | Return the tensor into multiple rectangular regions specified by th number of cuts we make on each d... |
| `apply_tensor_mapping()` | 36183 | The final dim of the indices_tensor is mapped to its corresponding address in mapping tensor  More s... |
| `apply_tensor_mapping_slowly()` | 36191 | indices_tensor = indices_tensor.astype(int)  indices_shape = indices_tensor.shape mapping_shape = ma... |
| `as_numpy_array()` | 36579 | Will convert x into type np.ndarray This should convert anything that can be converted into a numpy ... |
| `_tensorify()` | 42448 | Convert input to tensor-like format (NumPy array or torch tensor).  Private utility function that en... |
| `is_a_matrix()` | 42470 | Square matrices are of shape (N,N) where N is some integer This function returns N Lets you not have... |
| `is_a_square_matrix()` | 42474 | Square matrices are of shape (N,N) where N is some integer This function returns N Lets you not have... |
| `square_matrix_size()` | 42478 | Square matrices are of shape (N,N) where N is some integer This function returns N Lets you not have... |
| `_hsv_to_rgb_via_numpy()` | 46683 | Convert an HSV image to RGB using numpy. The input HSV values are assumed to be in the range [0, 1].... |
| `_rgb_to_hsv_via_numpy()` | 46755 | Convert an RGB image to HSV using numpy. The input RGB values are assumed to be in the range [0, 1].... |
| `get_computer_name()` | 47713 | Returns the name of the current computer https://stackoverflow.com/questions/799767/getting-name-of-... |
| `random_rotation_matrix()` | 47749 | Also known as a real orthonormal matrix Every vector in the output matrix is orthogonal to every vec... |
| `validate_tensor_shapes()` | 48726 | Validates that tensor dimensions match expected shapes and extracts dimension values. Reads the tens... |
| `_test_validate_tensor_shapes()` | 49073 | Run a test function and report results. print("\n{}\nTEST: {}\n{}".format('='*80, name, '-'*80)) try... |
| `test_single_tensor()` | 49096 | *(No description)* |
| `test_multiple_tensors_consistent()` | 49103 | *(No description)* |
| `test_mixed_tensor_types()` | 49111 | *(No description)* |
| `test_missing_tensor()` | 49128 | *(No description)* |
| `test_not_a_tensor()` | 49134 | *(No description)* |
| `_copy_tensor()` | 49443 |  works across libraries - such as numpy, torch  if is_numpy_array (x): return copy(x) #After benchma... |
| `play_the_matrix_animation()` | 51225 | Plays a super cool animation in your terminal that makes it look like you're hacking the matrix (Fro... |
| `get_matrix_code_chars()` | 51296 | Make rain forever by choosing a random column from pool and make rain at that column and repeat :par... |
| `calculate_flows()` | 53375 | Calculates optical flow for a whole video, given a video and a function that computes flow(prev_fram... |
| `as_numpy_images()` | 54628 |  Will convert an array of images to BHWC np.ndarray form if it isn't already - supports BCHW torch t... |
| `as_numpy_image()` | 54722 |  Will convert an image to HWC np.ndarray form if it isn't already - supports CHW torch tensors, PIL ... |
| `as_numpy_video()` | 54751 | Convert video to NumPy THWC format from various input formats.  Enhanced Documentation: - Handles to... |
| `as_numpy_videos()` | 54777 | Convert batch of videos to NumPy BTHWC format.  Handles torch BTCHW → numpy BTHWC conversion for bat... |
| `load_safetensors()` | 54861 | Loads tensors from a .safetensors file.  Args: path (str): Path to .safetensors file, or a glob for ... |
| `save_safetensors()` | 54956 | Saves tensors to a .safetensors file.  Args: tensors (dict or easydict): Dictionary of tensors to sa... |

## Architectural Analysis


## Function Relationships

### Type Conversion
- `is_numpy_array()` ↔ `as_numpy_array()`

### Batch Operations
- `as_numpy_image()` ↔ `as_numpy_images()`
- `as_numpy_video()` ↔ `as_numpy_videos()`

