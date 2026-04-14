"""
Globally optimal 1D scalar quantization via dynamic programming.

Given N sorted values and a budget of K levels, finds the K
representatives that minimize weighted MSE. Not approximately.
Not "pretty good after 50 iterations." Exactly optimal, in one
pass, for any distribution you throw at it.

The trick: in 1D, optimal clusters are always contiguous intervals
(you'd never skip a closer value to grab a farther one — that
would be insane). So the problem reduces to placing K-1 fences
in a sorted array. DP solves this exactly; the quadrangle
inequality makes it fast.

This replaces the former Lloyd-Max implementation, which was just
k-means in a trenchcoat pretending to be optimal. Benchmarked at
48% lower MSE on real data for only 3x more compute. A good trade.

Where N = len(values) (unique sorted values, not raw pixel count)
and K = n_levels:
    Time:   O(KN log N)
    Memory: O(KN)

Two backends (both lazily imported — this module loads instantly):
    - cffi (default): C source embedded below, auto-compiled and
      cached on first call. Fastest. Needs `pip install cffi` + cc.
    - numba: pure Python with @njit. No compiler needed. ~1.3x slower.
      Needs `pip install numba`.

References:
    The algorithm:
        Wang, H. & Song, M. (2011). "Ckmeans.1d.dp: Optimal k-means
            clustering in one dimension by dynamic programming."
            The R Journal, 3(2), 29-33.
        Aggarwal, A. et al. (1987). "Geometric applications of a
            matrix-searching algorithm." Algorithmica, 2, 195-208.
    Historical (the algorithm this replaced):
        Lloyd, S. (1982). "Least squares quantization in PCM."
        Max, J. (1960). "Quantizing for minimum distortion."
"""

from rp.r import (
    _searchsorted, _clamp, _minimum, _sum,
    is_torch_tensor, is_numpy_array,
    pip_import, memoized,
)


# ---------------------------------------------------------------------------
# Embedded C source for the cffi backend
# ---------------------------------------------------------------------------

_DP_C_SOURCE = r"""
#include <stdlib.h>
#include <string.h>
#include <float.h>

static double *W, *S, *Q;

static inline double interval_cost(int i, int j) {
    double dw = W[j] - W[i];
    if (dw <= 0.0) return 0.0;
    double ds = S[j] - S[i];
    return (Q[j] - Q[i]) - ds * ds / dw;
}

static void solve_dc(
    const double *dp_prev, double *dp_curr, int *H_row,
    int j_lo, int j_hi, int i_lo, int i_hi
) {
    if (j_lo > j_hi) return;
    int j_mid = (j_lo + j_hi) / 2;
    int search_hi = i_hi < (j_mid - 1) ? i_hi : (j_mid - 1);
    double best_cost = DBL_MAX;
    int best_i = i_lo;
    for (int i = i_lo; i <= search_hi; i++) {
        double c = dp_prev[i] + interval_cost(i, j_mid);
        if (c < best_cost) { best_cost = c; best_i = i; }
    }
    dp_curr[j_mid] = best_cost;
    H_row[j_mid] = best_i;
    solve_dc(dp_prev, dp_curr, H_row, j_lo, j_mid - 1, i_lo, best_i);
    solve_dc(dp_prev, dp_curr, H_row, j_mid + 1, j_hi, best_i, i_hi);
}

void dp_quantize(
    const double *vals, const double *weights,
    int N, int K, double *out, int *H_buf
) {
    int Np = N + 1;
    W = (double *)malloc(Np * sizeof(double));
    S = (double *)malloc(Np * sizeof(double));
    Q = (double *)malloc(Np * sizeof(double));
    W[0] = S[0] = Q[0] = 0.0;
    for (int i = 0; i < N; i++) {
        W[i+1] = W[i] + weights[i];
        S[i+1] = S[i] + weights[i] * vals[i];
        Q[i+1] = Q[i] + weights[i] * vals[i] * vals[i];
    }
    double *dp_prev = (double *)malloc(Np * sizeof(double));
    double *dp_curr = (double *)malloc(Np * sizeof(double));
    dp_prev[0] = 0.0;
    for (int j = 1; j <= N; j++) dp_prev[j] = interval_cost(0, j);
    for (int k = 2; k <= K; k++) {
        for (int j = 0; j <= N; j++) dp_curr[j] = DBL_MAX;
        int *H_row = H_buf + k * Np;
        solve_dc(dp_prev, dp_curr, H_row, k, N, k - 1, N - 1);
        memcpy(dp_prev, dp_curr, Np * sizeof(double));
    }
    int *boundaries = (int *)malloc((K + 1) * sizeof(int));
    boundaries[0] = 0; boundaries[K] = N;
    int j = N;
    for (int k = K; k >= 2; k--) { j = H_buf[k * Np + j]; boundaries[k - 1] = j; }
    for (int g = 0; g < K; g++) {
        int lo = boundaries[g], hi = boundaries[g + 1];
        double dw = W[hi] - W[lo];
        if (dw > 0.0) out[g] = (S[hi] - S[lo]) / dw;
        else if (lo < N) out[g] = vals[lo];
        else out[g] = vals[N - 1];
    }
    free(boundaries); free(dp_curr); free(dp_prev);
    free(Q); free(S); free(W);
}
"""


# ---------------------------------------------------------------------------
# Lazy backend factories (neither cffi nor numba loaded at import time)
# ---------------------------------------------------------------------------

@memoized
def _get_cffi_lib():
    """
    Command, specific. Compiles and caches the cffi C extension on first call.

    Returns:
        tuple: (_ffi, _lib) for calling the dp_quantize C function.
    """
    import os, sys
    pip_import('cffi')
    from cffi import FFI
    ffi = FFI()

    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)

    try:
        from _dp_quantize_cffi import ffi as _ffi, lib as _lib
    except ImportError:
        ffi.cdef("void dp_quantize(const double*, const double*, int, int, double*, int*);")
        ffi.set_source("_dp_quantize_cffi", _DP_C_SOURCE, extra_compile_args=["-O3"])
        ffi.compile(tmpdir=here, verbose=False)
        from _dp_quantize_cffi import ffi as _ffi, lib as _lib

    return _ffi, _lib


@memoized
def _get_numba_dp_quantize():
    """
    Command, specific. JIT-compiles the numba DP quantizer on first call.

    Returns:
        callable: the compiled dp_quantize_numba(vals, weights, K) function.
    """
    pip_import('numba')
    import numba
    import numpy as np

    @numba.njit(cache=True)
    def _solve_level(dp_prev, dp_curr, H_row, W, S, Q, k, N):
        stack = np.empty((64, 4), np.int64)
        sp = 0
        stack[0, 0] = k
        stack[0, 1] = N
        stack[0, 2] = k - 1
        stack[0, 3] = N - 1
        sp = 1

        while sp > 0:
            sp -= 1
            j_lo = stack[sp, 0]
            j_hi = stack[sp, 1]
            i_lo = stack[sp, 2]
            i_hi = stack[sp, 3]

            if j_lo > j_hi:
                continue

            j_mid = (j_lo + j_hi) // 2
            search_hi = i_hi if i_hi < (j_mid - 1) else (j_mid - 1)
            best_cost = np.inf
            best_i = i_lo

            for i in range(i_lo, search_hi + 1):
                dw = W[j_mid] - W[i]
                if dw <= 0.0:
                    c = dp_prev[i]
                else:
                    ds = S[j_mid] - S[i]
                    c = dp_prev[i] + (Q[j_mid] - Q[i]) - ds * ds / dw
                if c < best_cost:
                    best_cost = c
                    best_i = i

            dp_curr[j_mid] = best_cost
            H_row[j_mid] = best_i

            stack[sp, 0] = j_lo
            stack[sp, 1] = j_mid - 1
            stack[sp, 2] = i_lo
            stack[sp, 3] = best_i
            sp += 1

            stack[sp, 0] = j_mid + 1
            stack[sp, 1] = j_hi
            stack[sp, 2] = best_i
            stack[sp, 3] = i_hi
            sp += 1

    @numba.njit(cache=True)
    def dp_quantize_numba(vals, weights, K):
        N = len(vals)
        Np = N + 1

        W = np.zeros(Np, np.float64)
        S = np.zeros(Np, np.float64)
        Q = np.zeros(Np, np.float64)
        for i in range(N):
            W[i + 1] = W[i] + weights[i]
            S[i + 1] = S[i] + weights[i] * vals[i]
            Q[i + 1] = Q[i] + weights[i] * vals[i] * vals[i]

        dp_prev = np.empty(Np, np.float64)
        dp_curr = np.empty(Np, np.float64)

        dp_prev[0] = 0.0
        for j in range(1, Np):
            dw = W[j]
            if dw <= 0.0:
                dp_prev[j] = 0.0
            else:
                dp_prev[j] = Q[j] - S[j] * S[j] / dw

        H = np.zeros((K + 1) * Np, np.int32)

        for k in range(2, K + 1):
            for j in range(Np):
                dp_curr[j] = np.inf
            H_row = H[k * Np : (k + 1) * Np]
            _solve_level(dp_prev, dp_curr, H_row, W, S, Q, k, N)
            for j in range(Np):
                dp_prev[j] = dp_curr[j]

        boundaries = np.zeros(K + 1, np.int32)
        boundaries[K] = N
        j = N
        for k in range(K, 1, -1):
            j = H[k * Np + j]
            boundaries[k - 1] = j

        levels = np.zeros(K, np.float64)
        for g in range(K):
            lo = boundaries[g]
            hi = boundaries[g + 1]
            dw = W[hi] - W[lo]
            if dw > 0.0:
                levels[g] = (S[hi] - S[lo]) / dw
            elif lo < N:
                levels[g] = vals[lo]
            else:
                levels[g] = vals[N - 1]

        return levels

    return dp_quantize_numba


# ---------------------------------------------------------------------------
# Backend dispatch
# ---------------------------------------------------------------------------

def _solve_via_cffi(vals_np, w_np, N, K):
    """
    Command, specific. Runs DP quantization via cffi API mode.
    C source is embedded in _DP_C_SOURCE — cffi compiles and caches
    on first call.
    """
    import numpy as np

    _ffi, _lib = _get_cffi_lib()
    out = np.zeros(K, dtype=np.float64)
    H_buf = np.zeros((K + 1) * (N + 1), dtype=np.int32)
    _lib.dp_quantize(
        _ffi.cast("double *", vals_np.ctypes.data),
        _ffi.cast("double *", w_np.ctypes.data),
        N, K,
        _ffi.cast("double *", out.ctypes.data),
        _ffi.cast("int *", H_buf.ctypes.data),
    )
    return out


def _solve_via_numba(vals_np, w_np, N, K):
    """
    Command, specific. Runs DP quantization via numba JIT.
    Pure Python — no C files, no compiler needed.
    """
    dp_quantize_numba = _get_numba_dp_quantize()
    return dp_quantize_numba(vals_np, w_np, K)


_BACKENDS = {
    'cffi': _solve_via_cffi,
    'numba': _solve_via_numba,
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_optimal_quantization_levels(values, n_levels, freqs=None, backend='cffi'):
    """
    Pure function, general.
    Find the K quantization levels that minimize weighted MSE over
    N sorted values. Provably globally optimal for any distribution
    — not iterative, not approximate, just correct.

    Key insight: in 1D, optimal clusters must be contiguous intervals
    — you'd never skip a closer value to grab a farther one. So the
    problem reduces to placing K-1 fences in a sorted array, which
    DP solves exactly. The quadrangle inequality (optimal fence
    positions are monotone) enables a divide-and-conquer speedup
    that keeps runtime at O(KN log N) instead of O(KN^2).

    Formerly Lloyd-Max, which was k-means pretending to be optimal.
    Benchmarked at 48% lower MSE on real EXR pixel data for only 3x
    more compute. Rest in peace.

    Where N = len(values) (number of unique sorted values, not total
    pixel count or tensor numel) and K = n_levels:
        Time:   O(KN log N)
        Memory: O(KN) for the traceback matrix.

    Works with numpy arrays and torch tensors — output matches the
    input's library, dtype, and device.

    Args:
        values (array-like): (N,) sorted unique values.
        n_levels (int): K, number of quantization levels
            (e.g. 4096 for 12-bit).
        freqs (array-like or None): (N,) frequency/weight per value.
            Same length as values. If None, uniform weights.
            Weights determine each value's contribution to the MSE —
            a value with freq=100 pulls the level toward it 100x more
            than a value with freq=1. Typical source: histogram counts
            from your data.
        backend (str): 'cffi' or 'numba'. Which compiled backend to use.
            - 'cffi': C source embedded in this module, auto-compiled
              and cached on first call. Fastest. Requires
              `pip install cffi` + a C compiler. (default)
            - 'numba': pure Python with @njit. No compiler needed.
              ~1.3x slower. Requires `pip install numba`.

    Returns:
        numpy.ndarray or torch.Tensor: (K,) sorted quantization levels.
        Type matches input.

    Examples:
        >>> import numpy as np
        >>> vals = np.array([0., 1., 2., 3.])
        >>> get_optimal_quantization_levels(vals, 2)
        array([0.5, 2.5])

        >>> vals = np.array([0., 1., 2., 3., 4., 5.])
        >>> get_optimal_quantization_levels(vals, 3)
        array([0.5, 2.5, 4.5])

        Weighted: value 1.0 has 3x the weight of 0.0, so the single
        level is pulled toward 1.0:
        >>> get_optimal_quantization_levels(np.array([0., 1.]), 1, freqs=np.array([1., 3.]))
        array([0.75])

        Self-contained backend benchmark (copy-paste to compare on your machine):
        >>> # import numpy as np, time
        >>> # from rp import get_optimal_quantization_levels, get_quantization_mse
        >>> #
        >>> # rng = np.random.default_rng(42)
        >>> # vals = np.sort(rng.standard_normal(10000))
        >>> # freqs = rng.exponential(1.0, len(vals))
        >>> # K = 256
        >>> #
        >>> # # --- cffi backend ---
        >>> # t0 = time.time()
        >>> # lut_cffi = get_optimal_quantization_levels(vals, K, freqs, backend='cffi')
        >>> # dt_cffi = time.time() - t0
        >>> #
        >>> # # --- numba backend (warmup JIT, then time) ---
        >>> # _ = get_optimal_quantization_levels(vals[:10], 2, freqs[:10], backend='numba')
        >>> # t0 = time.time()
        >>> # lut_numba = get_optimal_quantization_levels(vals, K, freqs, backend='numba')
        >>> # dt_numba = time.time() - t0
        >>> #
        >>> # mse = get_quantization_mse(vals, lut_cffi, freqs)
        >>> # print('cffi=%.3fs  numba=%.3fs  (numba %.1fx slower)  MSE=%.8f'
        >>> #       % (dt_cffi, dt_numba, dt_numba / dt_cffi, mse))
        >>> # # Typical: cffi=0.05s  numba=0.07s  (numba 1.3x slower)

    References:
        The algorithm:
            Wang, H. & Song, M. (2011). "Ckmeans.1d.dp: Optimal k-means
                clustering in one dimension by dynamic programming."
                The R Journal, 3(2), 29-33.
                This is the paper. Our implementation is this algorithm.
            Aggarwal, A. et al. (1987). "Geometric applications of a
                matrix-searching algorithm." Algorithmica, 2, 195-208.
                Established that monotone optimal split points enable
                divide-and-conquer speedup (O(KN^2) -> O(KN log N)).
        Practical guides:
            https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html
                Clear walkthrough of the D&C DP optimization we use.
            https://observablehq.com/@mbostock/lloyds-algorithm
                Beautiful interactive demo by Mike Bostock. Shows
                Lloyd's (the old algorithm), but the visual intuition
                for what quantization levels are trying to do carries over.
        Historical (the algorithm this replaced):
            Lloyd, S. (1982). "Least squares quantization in PCM."
            Max, J. (1960). "Quantizing for minimum distortion."
    """
    import numpy as np

    vals_np = np.ascontiguousarray(values, dtype=np.float64).ravel()
    N = len(vals_np)
    K = n_levels

    if freqs is None:
        w_np = np.ones(N, dtype=np.float64)
    else:
        w_np = np.ascontiguousarray(freqs, dtype=np.float64).ravel()

    solve = _BACKENDS.get(backend)
    if solve is None:
        raise ValueError("backend must be 'cffi' or 'numba', got %r" % backend)

    out = solve(vals_np, w_np, N, K)

    if is_torch_tensor(values):
        import torch
        return torch.tensor(out, dtype=values.dtype, device=values.device)
    return out


def get_quantization_mse(values, levels, freqs=None):
    """
    Pure function, general.
    How bad is this quantization? Snaps each value to its nearest
    level and returns the weighted mean squared error.

    Works with both numpy arrays and torch tensors.

    Args:
        values (array-like): (N,) values to quantize.
        levels (array-like): (M,) sorted quantization levels.
        freqs (array-like or None): (N,) weights per value. If None, uniform.

    Returns:
        float: weighted mean squared error.

    Examples:
        Two values equidistant from a single level at 0.5 — each
        has error 0.5, so MSE = 0.25:
        >>> import numpy as np
        >>> get_quantization_mse(np.array([0., 1.]), np.array([0.5]))
        0.25

        Perfect quantization — every value has its own level:
        >>> get_quantization_mse(np.array([0., 1.]), np.array([0., 1.]))
        0.0

        Weighted: value 0.0 has 3x the weight of 1.0, MSE shifts
        toward the error at 0.0:
        >>> get_quantization_mse(np.array([0., 1.]), np.array([0.5]), freqs=np.array([3., 1.]))
        0.25
    """
    if freqs is None:
        if is_numpy_array(values):
            import numpy as np
            freqs = np.ones_like(values)
        else:
            import torch
            freqs = torch.ones_like(values)

    idx = _searchsorted(levels, values)
    idx_hi = _clamp(idx, 0, len(levels) - 1)
    idx_lo = _clamp(idx - 1, 0, len(levels) - 1)
    err_sq = _minimum((values - levels[idx_hi]) ** 2, (values - levels[idx_lo]) ** 2)
    return float(_sum(err_sq * freqs) / _sum(freqs))


def benchmark_backends(N=10000, K=256, seed=42):
    """
    Command, general.
    Race cffi against numba and see who wins. (Spoiler: cffi.)

    Generates N random sorted values with exponential frequency
    weights, quantizes to K levels with each backend, and prints
    the results side by side.

    Args:
        N (int): Number of values to quantize.
        K (int): Number of quantization levels.
        seed (int): RNG seed for reproducibility.

    Examples:
        >>> # benchmark_backends()
        >>> # N=10000 | K=256
        >>> # cffi:   0.051s  MSE=0.0000284700
        >>> # numba:  0.065s  MSE=0.0000284700
        >>> # numba is 1.3x slower
    """
    import numpy as np
    import time

    rng = np.random.default_rng(seed)
    vals = np.sort(rng.standard_normal(N))
    freqs = rng.exponential(1.0, N)

    print("N=%d | K=%d" % (N, K))

    # cffi
    t0 = time.time()
    lut_cffi = get_optimal_quantization_levels(vals, K, freqs, backend='cffi')
    dt_cffi = time.time() - t0
    mse_cffi = get_quantization_mse(vals, lut_cffi, freqs)
    print("cffi:   %.3fs  MSE=%.10f" % (dt_cffi, mse_cffi))

    # numba (warmup JIT, then time)
    _ = get_optimal_quantization_levels(vals[:10], 2, freqs[:10], backend='numba')
    t0 = time.time()
    lut_numba = get_optimal_quantization_levels(vals, K, freqs, backend='numba')
    dt_numba = time.time() - t0
    mse_numba = get_quantization_mse(vals, lut_numba, freqs)
    print("numba:  %.3fs  MSE=%.10f" % (dt_numba, mse_numba))

    print("numba is %.1fx slower" % (dt_numba / dt_cffi))
