# Mathematical and Scientific Functions in RP Module

## Overview

The RP module contains an extensive collection of mathematical and scientific computing functions spanning multiple domains. This document catalogs all mathematical/scientific functions, their relationships, computational workflows, and algorithm chains discovered through comprehensive analysis.

## Mathematical Constants

### Core Constants
```python
π = pi = 3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862
τ = tau = 2 * π  # Tau = 2*pi for cleaner circular mathematics
```

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:15635-15636`

## Function Categories

### 1. Basic Mathematical Operations

#### Universal Math Functions (Cross-Library Compatibility)
These functions work across NumPy, PyTorch, and pure Python:

**Trigonometric Functions**
- `_sin(x)` - Sine function
- `_cos(x)` - Cosine function  
- `_tan(x)` - Tangent function
- `_asin(x)` - Arcsine function
- `_acos(x)` - Arccosine function
- `_atan(x)` - Arctangent function
- `_atan2(y, x)` - Two-argument arctangent
- `_sinh(x)` - Hyperbolic sine
- `_cosh(x)` - Hyperbolic cosine
- `_tanh(x)` - Hyperbolic tangent

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:49182-49330`

**Exponential and Logarithmic Functions**
- `_exp(x)` - Exponential function
- `_log(x)` - Natural logarithm
- `_log10(x)` - Base-10 logarithm
- `_log2(x)` - Base-2 logarithm
- `_sqrt(x)` - Square root

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:49200-49222`

**Utility Functions**
- `_abs(x)` - Absolute value
- `_pow(x, y)` - Power function
- `_ceil(x)` - Ceiling function
- `_floor(x)` - Floor function
- `_round(x)` - Rounding function
- `_sign(x)` - Sign function
- `_clamp(x, min_val, max_val)` - Clamp to range
- `_clip(x, min_val, max_val)` - Alias for clamp
- `_degrees(x)` - Convert radians to degrees
- `_radians(x)` - Convert degrees to radians

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:49164-49348`

#### Pure Python Math Functions
- `sign(x, zero=0)` - Sign function with configurable zero handling
- `clamp(x, min_value, max_value)` - Constrain value to range
- `int_clamp(x, min_value, max_value)` - Integer clamp
- `float_clamp(x, min_value, max_value)` - Float clamp

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:13538, 16107-16113`

### 2. Statistical Functions

#### Basic Statistics
- `mean(*x)` - Arithmetic mean with flexible input handling
- `median(*x)` - Median value calculation  
- `_mean(x, dim=None, keepdim=False)` - Cross-library mean function
- `_sum(x, dim=None, keepdim=False)` - Cross-library sum function

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:41790-41819, 49430-49441`

#### Normal Distribution Functions
- `norm_cdf(x, mean=0, std=1)` - Normal cumulative distribution function
- `norm_pdf(x, mean=0, std=1)` - Normal probability density function  
- `inverse_norm_cdf(p, mean=0, std=1)` - Inverse normal CDF (quantile function)

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:41821-41857`

**Computational Pipeline**: Statistical analysis workflow
```
Data → mean/median → norm_pdf → norm_cdf → inverse_norm_cdf → Statistical inference
```

#### Histogram and Distribution Analysis
- `histogram_in_terminal(values, sideways=False)` - Terminal-based histogram display
- `byte_image_histogram(image)` - Image histogram calculation
- `rgb_histogram_image(histograms, *, width=256, height=128, yscale=1, smoothing=0)` - RGB histogram visualization

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:9258, 28676, 28605`

### 3. Linear Algebra and Matrix Operations

#### Matrix Utilities
- `is_a_matrix(matrix)` - Matrix validation
- `is_a_square_matrix(matrix)` - Square matrix check
- `square_matrix_size(matrix)` - Get size N of NxN matrix
- `matrix_to_tuples(m, filter=lambda r,c,val:True)` - Convert matrix to coordinate tuples

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:42470-42486, 16414-16425`

#### Vector Operations
- `magnitude(x, **kwargs)` - Vector magnitude calculation
- `normalized(x, axis=None)` - Vector normalization to unit length
- `cosine_similarity(x, y)` - Cosine similarity between vectors

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:34404-34411, 28940`

#### Transformations and Affine Operations
- `rotation_matrix(angle, out_of=tau)` - 2D rotation matrix generation
- `rotation_affine_2d(angle, pivot=[0,0], *, out_of=tau)` - 2D rotation affine transform
- `least_squares_euclidean_affine(from_points, to_points, *, include_correlation=False)` - Euclidean affine fitting
- `least_squares_regression_line_coeffs(X, Y=None, include_correlation=False)` - Linear regression coefficients
- `combined_affine(*affines)` - Combine multiple affine transforms
- `is_euclidean_affine_matrix(affine)` - Validate euclidean affine matrix
- `is_affine_matrix(affine)` - General affine matrix validation

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:29279, 29855, 29730-29918, 34333-34402, 30062-30067`

**Computational Pipeline**: Geometric transformation workflow
```
Points → least_squares_euclidean_affine → rotation_matrix → combined_affine → Transformed points
```

### 4. Distance and Similarity Metrics

#### Distance Functions
- `squared_euclidean_distance(from_point, to_point)` - Squared Euclidean distance (more efficient)
- `euclidean_distance(from_point, to_point)` - Standard Euclidean distance
- `differential_euclidean_distances(points, *, include_zero=False, loop=False)` - Sequential point distances
- `cumulative_euclidean_distances(points, *, include_zero=False, loop=False)` - Cumulative distance along path
- `distance_matrix(from_points, to_points=None)` - Pairwise distance matrix
- `squared_distance_matrix(from_points, to_points=None)` - Squared distance matrix

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:29480-29518, 29686-29728`

**Computational Pipeline**: Distance analysis workflow
```
Point sets → distance_matrix → closest_points → knn_clusters → Spatial analysis
```

### 5. Clustering and Machine Learning

#### Clustering Algorithms
- `knn_clusters(vectors, k=5, spatial_dict=FlannDict)` - K-nearest neighbor clustering
- `cluster_by_key(iterable, key, *, as_dict=False)` - Group by key function
- `cluster_by_attr(iterable, attr, *, as_dict=False)` - Group by attribute
- `cluster_filter(vec, filter=identity)` - Filter clustering results

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:33994-34039, 16450-16473, 16561-16565`

#### Spatial Data Structures
- `FlannDict` - Fast approximate nearest neighbor spatial dictionary
- `closest_points(from_points, to_points, *, return_values=False)` - Find closest points

**Location**: Referenced in knn_clusters and spatial operations

### 6. Signal Processing and Fourier Analysis

#### Fourier Transform Functions
- `fourier(cyclic_function, freq, cyclic_period=τ, ↈ_riemann_terms=100)` - Continuous Fourier transform
- `discrete_fourier(cyclic_vector, freq)` - Discrete Fourier transform for vectors
- `_fft(x)` - Fast Fourier Transform (cross-library)
- `_ifft(x)` - Inverse Fast Fourier Transform (cross-library)
- `fourier_descriptor(contour, *, order=10, normalize=True)` - Fourier descriptors for shapes
- `fourier_descriptor_distance(contour_1, contour_2, **kwargs)` - Distance using Fourier descriptors
- `fourier_descriptor_similarity(contour_1, contour_2, **kwargs)` - Similarity using Fourier descriptors

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:16398-16413, 49236-49246, 28943-28991`

#### Harmonic Analysis
- `harmonic_analysis_via_least_squares(wave, harmonics: int)` - Frequency analysis via least squares
- `sine_tone_sampler(ƒ=None, T=None, samplerate=None)` - Generate sine wave samples
- `triangle_tone_sampler(ƒ=None, T=None, samplerate=None)` - Generate triangle wave samples

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:16433-16448, 15641-15648`

**Computational Pipeline**: Signal analysis workflow
```
Signal → fourier/discrete_fourier → harmonic_analysis_via_least_squares → Frequency domain analysis
```

### 7. Numerical Integration and Calculus

#### Integration Methods
- `riemann_sum(f, x0, x1, N, left_to_right_sum_ratio=None)` - Riemann sum approximation
- `riemann_mean(f, x0, x1, N, left_to_right_sum_ratio=None)` - Mean value via Riemann sum
- `fractional_integral_in_frequency_domain(coefficients, n=1)` - Fractional calculus in frequency domain

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:16384-16396, 33811`

#### Differential Operations
- `circular_diff(array, axis=0)` - Circular difference operation
- `circ_diff_inverse(x)` - Inverse of circular difference

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:27227, 27330`

### 8. Geometric Algorithms

#### Convex Hull and Computational Geometry
- `convex_hull(points)` - 2D convex hull calculation
- `graham_scan(path)` - Graham scan convex hull algorithm
- `paths_intersect(path_a, path_b)` - Path intersection detection

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:42770-42819`

#### Contour Analysis
- `cv_find_contours(image, *, include_every_pixel=False)` - Find contours in images
- `cv_simplify_contour(contour, epsilon=0.001)` - Simplify contour using Douglas-Peucker
- `cv_distance_to_contour(contour, x, y)` - Distance from point to contour
- `cv_closest_contour_point(contour, x, y)` - Closest point on contour
- `cv_closest_contour(contours, x, y)` - Find closest contour to point
- `cv_contour_length(contour, closed=False)` - Calculate contour perimeter
- `cv_contour_area(contour)` - Calculate contour area
- `cv_contour_match(a, b, scale_invariant=False)` - Compare contour shapes
- `cv_best_match_contour(contour, contours, **kwargs)` - Find best matching contour
- `cv_best_match_contours(contour, contours, n=None, **kwargs)` - Find N best matching contours

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:27886-29072`

#### Path Operations
- `evenly_split_path(path, number_of_pieces=100, *, loop=False)` - Subdivide path evenly by arc length
- `r_transform(path)` - R-transform for path analysis
- `r_transform_inverse(path)` - Inverse R-transform

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:29520-29558, 34041-34052`

**Computational Pipeline**: Geometric analysis workflow
```
Image → cv_find_contours → cv_simplify_contour → fourier_descriptor → Shape analysis
Points → graham_scan → convex_hull → Geometric properties
```

### 9. Number Theory and Combinatorics

#### Prime Numbers and Factorization
- `prime_factors(number)` - Prime factorization with caching
- `prime_number_generator()` - Generate prime numbers
- `gcd(*i)` - Greatest common divisor (supports multiple arguments)
- `lcm(*i)` - Least common multiple (supports multiple arguments)

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:42489-42523, 40433-40468, 27335-27343`

#### Fibonacci Sequence
- `fibonacci(n)` - Fibonacci number calculation (optimized for large n)
- `inverse_fibonacci(n)` - Find Fibonacci index for given number

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:42625-42655`

**Implementation Note**: Uses golden ratio formula for n<71, switches to iterative for accuracy.

### 10. Image Processing Mathematical Operations

#### Morphological Operations
- `max_filter(image, diameter, single_channel=False, mode='reflect', shutup=False)` - Maximum filter
- `min_filter(image, diameter, single_channel=False, mode='reflect', shutup=False)` - Minimum filter
- `med_filter(image, diameter, single_channel=False, mode='reflect', shutup=False)` - Median filter
- `range_filter(image, diameter, single_channel=False, mode='reflect', shutup=False)` - Range filter

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:4235-4364`

#### Kernels and Convolution
- `gaussian_kernel(size=21, sigma=3, dim=2)` - Generate Gaussian kernel
- `flat_circle_kernel(diameter)` - Generate flat circular kernel
- `gauss_blur(image, σ, single_channel=False, mode='reflect', shutup=False)` - Gaussian blur
- `cv_image_filter(image, kernel)` - Apply custom kernel filter

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:2817, 2803, 2739, 47722`

#### Transform Operations
- `cv_distance_transform(mask, distance_to='white', metric='l2', algorithm='precise')` - Distance transform
- `cv_equalize_histogram(image, by_value=True)` - Histogram equalization

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:28889, 51054`

### 11. Interpolation and Fitting

#### Interpolation Methods
- `linterp(values: list, index: float, *, cyclic=False, blend_func=blend)` - Linear interpolation
- `interp(x, x0, x1, y0, y1)` - Two-point interpolation
- `blend(𝓍, 𝓎, α)` - Linear blend (lerp)
- `iblend(z, 𝓍, 𝓎)` - Inverse blend (solve for alpha)
- `delaunay_interpolation_weights(key_points, query_points)` - Delaunay triangulation interpolation

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:9819-9807, 57598`

#### Curve Fitting
- `perpendicular_bisector_function(x0, y0, x1, y1)` - Generate perpendicular bisector function
- `whiten_points_covariance(points)` - Whiten point cloud using covariance

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:16426-16431, 39956`

### 12. Advanced Mathematical Functions

#### Activation Functions (Neural Networks)
- `_sigmoid(x)` - Sigmoid activation function
- `_relu(x)` - ReLU activation function  
- `_softmax(x, dim=-1)` - Softmax activation function
- `_tanh(x)` - Hyperbolic tangent activation

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:49254-49272`

#### Cross-Correlation and Matching
- `circular_cross_correlate(a, b)` - Circular cross-correlation
- `icp_least_squares_euclidean_affine(from_points, to_points, max_iter=5, *, include_extra=False)` - Iterative Closest Point algorithm

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:27262, 29971-30062`

#### Complex Number Operations
- `complex_to_polar(complex)` - Convert complex to polar coordinates
- `euclidean_affine_to_complex_linear_coeffs(affine)` - Convert affine to complex coefficients
- `complex_linear_coeffs_to_euclidean_affine(m, b)` - Convert complex coefficients to affine

**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/r.py:16379-16382, 30070-30088`

## Computational Workflows and Algorithm Chains

### 1. Image Analysis Pipeline
```
Image → cv_find_contours → cv_simplify_contour → fourier_descriptor → 
fourier_descriptor_similarity → Shape matching and classification
```

### 2. Statistical Analysis Workflow
```
Data → mean/median → norm_pdf → norm_cdf → inverse_norm_cdf → 
Statistical inference and hypothesis testing
```

### 3. Point Cloud Processing Pipeline
```
Point sets → distance_matrix → knn_clusters → convex_hull → 
Spatial structure analysis
```

### 4. Signal Processing Chain
```
Time series → fourier/discrete_fourier → harmonic_analysis_via_least_squares → 
Frequency domain analysis → _ifft → Filtered signal
```

### 5. Geometric Transformation Pipeline
```
Source points → least_squares_euclidean_affine → rotation_matrix → 
combined_affine → Transformed geometry
```

### 6. Mathematical Morphology Workflow
```
Binary image → max_filter/min_filter → med_filter → range_filter → 
Morphological analysis
```

## Function Relationships and Dependencies

### Core Mathematical Foundation
- **Constants**: `π`, `τ` provide fundamental mathematical constants
- **Universal functions**: `_sin`, `_cos`, `_exp`, etc. provide cross-library compatibility
- **Basic operations**: `sign`, `clamp`, `magnitude` support higher-level functions

### Statistical Computing Stack
- **Basic statistics**: `mean`, `median` → **Distributions**: `norm_pdf`, `norm_cdf` → **Analysis**: Statistical inference
- **Histogram analysis**: `histogram_in_terminal`, `byte_image_histogram` → Visualization

### Linear Algebra Foundation  
- **Matrix operations**: `is_a_matrix`, `square_matrix_size` → **Transformations**: `rotation_matrix`, `affine operations`
- **Vector operations**: `magnitude`, `normalized` → **Distance metrics**: `euclidean_distance`, `cosine_similarity`

### Geometric Computing Pipeline
- **Contour detection**: `cv_find_contours` → **Simplification**: `cv_simplify_contour` → **Analysis**: `fourier_descriptor`
- **Spatial clustering**: `distance_matrix` → `knn_clusters` → Spatial structure identification

### Signal Processing Chain
- **Time domain**: Raw signals → **Fourier domain**: `fourier`, `discrete_fourier` → **Analysis**: `harmonic_analysis_via_least_squares`
- **Filtering**: `gaussian_kernel` → `gauss_blur` → `cv_image_filter`

## Usage Patterns and Best Practices

### 1. Cross-Library Compatibility
Use underscore-prefixed functions (`_sin`, `_cos`, `_exp`) for operations that need to work across NumPy, PyTorch, and pure Python.

### 2. Performance Optimization
- Use `squared_euclidean_distance` instead of `euclidean_distance` when possible
- Utilize caching in `prime_factors` for repeated calculations
- Choose appropriate Riemann integration terms in Fourier analysis

### 3. Mathematical Workflows
- Combine statistical functions for comprehensive data analysis
- Chain geometric transformations using `combined_affine`
- Use Fourier descriptors for shape analysis and matching

### 4. Integration Points
Most functions are designed to work together through consistent input/output formats:
- Points as NumPy arrays or complex numbers
- Images as NumPy arrays with standard formats
- Matrices following standard linear algebra conventions

## Deprecated/Graveyard Functions

### Historical Mathematical Functions
Located in `/opt/homebrew/lib/python3.10/site-packages/rp/libs/graveyard.py`:

- `k_means_analysis(data_vectors, k_or_initial_centroids, iterations, tries)` - K-means clustering implementation
- `graph_resistance_distance(n, d, x, y)` - Graph resistance distance calculation  
- `xyrgb_normalize(*xyrgb, rgb_old_max=255, rgb_new_max=1, x_new_max=1, y_new_max=1)` - Coordinate and color normalization
- `image_to_all_normalized_xy_rgb_training_pairs(image)` - Convert images to normalized training data

These functions remain accessible but represent older implementations that have been superseded.

## Summary

The RP module provides a comprehensive mathematical and scientific computing foundation with over 200+ mathematical functions spanning:

- **11 major categories** of mathematical operations
- **Cross-library compatibility** ensuring functions work with NumPy, PyTorch, and pure Python
- **Computational pipelines** for complex analysis workflows  
- **Optimized implementations** with caching and performance considerations
- **Consistent interfaces** enabling function composition and chaining

The design philosophy emphasizes the "accept anything, return what makes sense" pattern, automatic type conversion, and comprehensive coverage of mathematical domains needed for scientific computing, computer vision, machine learning, and data analysis applications.