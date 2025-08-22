# RP Library: Functional System

Functional programming foundation: composition, mapping, filtering, and transformation utilities.

**Total Functions: 52**

## Function Inventory

| Function | Line | Description |
|----------|------|-------------|
| `seq_map()` | 413 | See lazy_par_map for doc. buffer_limit defaults to 0 because we return everything all at once anyway... |
| `par_map()` | 422 | See lazy_par_map for doc. buffer_limit defaults to 0 because we return everything all at once anyway... |
| `lazy_par_map()` | 484 | A parallelized version of the built-in map using ThreadPoolExecutor.  Parameters: - func: The functi... |
| `test_par_map()` | 506 | from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED  if num_threads is not None... |
| `max_filter()` | 4235 | *(No description)* |
| `min_filter()` | 4274 | *(No description)* |
| `med_filter()` | 4313 | *(No description)* |
| `range_filter()` | 4352 | *(No description)* |
| `grid2d_map()` | 4363 | A private function used by image resizing functions in rp when their interp=='auto'  'area' interpol... |
| `skip_filter()` | 5657 | *(No description)* |
| `_filter_dict_via_fzf()` | 11266 | Uses fzf to select a subset of a dict and returns that dict. #Refactored using GPT4 from a mess: htt... |
| `map_constructor()` | 14426 | Walk the mapping, recording any duplicate keys.  deep=False mapping=JunctionList() for key_node, val... |
| `cluster_filter()` | 16561 | EXAMPLE: cluster_filter([2,3,5,9,4,6,1,2,3,4],lambda x:x%2==1) --> [[3, 5, 9], [1], [3]]  <---- It s... |
| `_cdh_folder_is_protected()` | 17735 | *(No description)* |
| `get_folder_size()` | 26520 | Given a file size in bytes, return a string that represents how large it is in megabytes, gigabytes ... |
| `reduced_row_echelon_form()` | 27182 | TODO: See if this is the same thing as a toeplitz matrix TODO: There might be a faster way of doing ... |
| `with_folder_name()` | 32944 | Like with_file_name, except it will always replace the extension (unlike with_file_name, where if na... |
| `get_all_folders()` | 33530 |  Take a folder, and return a list of all of its subfolders  assert folder_exists(folder),'Folder '+r... |
| `get_subfolders()` | 33535 |  Take a folder, and return a list of all of its subfolders  assert folder_exists(folder),'Folder '+r... |
| `folder_is_empty()` | 33555 | Determines whether a folder is empty or not.  This function uses os.scandir() to iterate over the co... |
| `get_random_folders()` | 33636 | Get a single random folder from the specified directory.  Enhanced Documentation: Utility function f... |
| `get_random_folder()` | 33643 | Get a single random folder from the specified directory.  Enhanced Documentation: Utility function f... |
| `apply_tensor_mapping()` | 36183 | The final dim of the indices_tensor is mapped to its corresponding address in mapping tensor  More s... |
| `apply_tensor_mapping_slowly()` | 36191 | indices_tensor = indices_tensor.astype(int)  indices_shape = indices_tensor.shape mapping_shape = ma... |
| `is_empty_folder()` | 38292 | Check if a path points to an existing file.  Enhanced Documentation: This is a fundamental file syst... |
| `delete_folder()` | 38574 | Will recursively delete a folder and all of its contents permanent exists for safety reasons. It can... |
| `delete_folders()` | 38654 | #Chooses between copy_directory and copy_file, whichever makes more sense. #If extract is True, it w... |
| `copy_to_folder()` | 38674 | Copy a file or directory to a folder, keeping the same file name For example, copy_to_folder('/docs/... |
| `reduce_wrap()` | 42895 | Decorator that extends a binary (two-argument) function to accept variable arguments. The function s... |
| `input_select_folder()` | 43204 | I use this to select arduinos when I want to connect to one with a serial port After this, I general... |
| `_load_ryan_lazygit_config()` | 44201 | config_lines=unindent( # < RP Lazygit Config Start > #DEFAULTS: https://github.com/jesseduffield/laz... |
| `_install_lazygit()` | 44237 | r LAZYGIT_VERSION=$(curl -s "https://api.github.com/repos/jesseduffield/lazygit/releases/latest" \| ... |
| `make_zip_file_from_folder()` | 46174 | Creates a .zip file on your hard drive. Zip the contents of some src_folder and return the output zi... |
| `extract_zip_file()` | 46206 | Extracts a zip or tar file to a specified folder. If the folder doesn't exist, it is created.  Param... |
| `_maybe_unbury_folder()` | 46313 | Checks if the given folder contains a single subfolder with the same name. If so, it moves all conte... |
| `get_normal_map()` | 46421 | Turn a bump map aka a height map, into a normal map This is used for 3d graphics, such as in video g... |
| `get_rgb_byte_color_identity_mapping_image()` | 47256 | Save this image, and color-grade it. Then the new image can be used as a map! Originally made for co... |
| `apply_colormap_to_image()` | 47281 | https://stackoverflow.com/questions/52498777/apply-matplotlib-or-custom-colormap-to-opencv-image/526... |
| `cv_image_filter()` | 47722 | Convolves an image with a custom kernel matrix on a per-channel basis  EXAMPLE: img=load_image('http... |
| `display_pandas_correlation_heatmap()` | 47796 | This function is used for exploratory analysis with pandas dataframes. It lets you see which variabl... |
| `torch_remap_image()` | 48419 | Remap an image tensor using the given x and y coordinate tensors. Out-of-bounds regions will be give... |
| `apply_uv_map()` | 48594 | Applies a UV map to an image to remap it Unlike cv_remap_image or torch_remap_image, UV maps are on ... |
| `get_identity_uv_map()` | 48685 | Returns an RGB UV-Map image with the form uv_form  EXAMPLE: >>> display_image( ...     with_alpha_ch... |
| `compose_rgb_image()` | 51111 |  Create an RGB image from three separate channels  r=as_grayscale_image(r) g=as_grayscale_image(g) b... |
| `compose_rgba_image()` | 51125 |  Create an RGBA image from four separate channels  r=as_grayscale_image(r) g=as_grayscale_image(g) b... |
| `compose_image_from_channels()` | 51142 |  Create an RGB or RGBA image from three or four separate channels  assert len(channels) in (3,4),'Ca... |
| `zip_folder_to_bytes()` | 51798 | Similar to file_to_bytes Takes a folder_path, zips it into a .zip file, then returns the bytes of th... |
| `map_network()` | 51938 | Maps the network :param pool_size: amount of parallel ping processes :return: list of valid ip addre... |
| `cv_remap_image()` | 53551 | If image is RGBA, then out-of-bounds regions will have 0-alpha This is like a UV mapping - where x a... |
| `filter_by_extension()` | 55915 | *(No description)* |
| `filter_pids_exist()` | 56965 | Returns the amount of free VRAM for a GPU given its ID. The returned value is in bytes. If gpu_id is... |
| `_get_kernel_to_pid_mapping()` | 57385 | *(No description)* |

## Architectural Analysis


## Function Relationships

### Batch Operations
- `get_random_folder()` ↔ `get_random_folders()`
- `delete_folder()` ↔ `delete_folders()`

