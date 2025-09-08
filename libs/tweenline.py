# timeline.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List, Iterable, Callable, Mapping

import numpy as np
import rp

__all__ = ["tween"]  # only export tween

# -----------------------------------------------------------------------------
# Easing registry (internal)
# -----------------------------------------------------------------------------

def _linear(t: float) -> float:
    return t

def _cubic_in_out(t: float) -> float:
    return 4 * t * t * t if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2

def _ease_in_quad(t: float) -> float:
    return t * t

def _ease_out_quad(t: float) -> float:
    return 1 - (1 - t) * (1 - t)

_EASES: Dict[str, Callable[[float], float]] = {
    "linear": _linear,
    "cubic": _cubic_in_out,
    "quad_in": _ease_in_quad,
    "quad_out": _ease_out_quad,
}

def _resolve_ease(ease: Any) -> Callable[[float], float]:
    if callable(ease):
        return ease
    if isinstance(ease, str):
        key = ease.lower()
        if key in _EASES:
            return _EASES[key]
        valid = ", ".join(sorted(_EASES.keys()))
        raise ValueError(
            f"Unknown easing '{ease}'. Valid options are: {valid}. "
            "You may also pass a callable ease(t: float) -> float."
        )
    raise TypeError(
        f"ease must be a string ({', '.join(sorted(_EASES.keys()))}) or a callable, got {type(ease).__name__}"
    )

# -----------------------------------------------------------------------------
# Helpers (ease-aware) — unchanged behavior
# -----------------------------------------------------------------------------

def blend_values(x, y, a):
    if not (
        rp.is_number(x) and rp.is_number(y)
        or rp.is_numpy_array(x) and rp.is_numpy_array(y) and x.shape == y.shape
    ):
        # The non-numerical case
        return y

    # The numerical case
    value = rp.blend(x, y, a)

    if isinstance(x, int) and isinstance(y, int) and not isinstance(x, bool) and not isinstance(y, bool):
        # If interpolating between two integers, we often need to return an int
        value = round(value)

    if isinstance(x, bool) and isinstance(y, bool):
        # If interpolating between two booleans, round to True or False
        value = bool(round(value))

    return value

# -----------------------------------------------------------------------------
# Core DSL (simple, phase-free)
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class _Atom:
    """
    A single tween/wait that starts at 'start' (offset in steps),
    runs for 'duration' steps, and blends from captured start-state
    to 'end' using 'ease_fn'. An empty 'end' means a wait (no deltas).
    """
    start: int
    duration: int
    end: Dict[str, Any]                # empty ⇒ wait
    ease_fn: Callable[[float], float]

class _Program:
    """
    Phase-free program: a flat multiset of atoms with start offsets.
    - Parallel (+): union atoms (starting at their own offsets).
    - Sequential (>>): shift the right program's atoms by the left program's duration.
    - Call with an initial state to materialize into a Timeline.
    """
    def __init__(self, atoms: List[_Atom] | None = None):
        self.atoms: List[_Atom] = atoms or []

    @property
    def duration(self) -> int:
        if not self.atoms:
            return 0
        return max((a.start + a.duration) for a in self.atoms)

    # Parallel composition (union)
    def __add__(self, other):
        if isinstance(other, _Program):
            return _Program(self.atoms + other.atoms)
        if isinstance(other, Timeline):
            return other + self  # Delegate to Timeline.__add__
        return NotImplemented

    # Sequential composition (shift)
    def __rshift__(self, other: "_Program") -> "_Program":
        if not isinstance(other, _Program):
            return NotImplemented
        shift = self.duration
        shifted = [_Atom(a.start + shift, a.duration, a.end, a.ease_fn) for a in other.atoms]
        return _Program(self.atoms + shifted)

    # Materialize with an initial state
    def __call__(self, init: Dict[str, Any]) -> "Timeline":
        return Timeline(init) >> self

    # Allow Program + Timeline or Program + dict-like (overlay or materialize)
    def __radd__(self, left):
        if isinstance(left, Timeline):
            return left + self
        if isinstance(left, Mapping):
            return Timeline(dict(left)) + self
        return NotImplemented

    # Allow dict-like >> Program (sequential)
    def __rrshift__(self, left):
        if isinstance(left, Timeline):
            return left >> self
        if isinstance(left, Mapping):
            return Timeline(dict(left)) >> self
        return NotImplemented

    def __mul__(self, count: int) -> "_Program":
        """Repeat this program count times using * operator."""
        if not isinstance(count, int):
            return NotImplemented
        if count <= 0:
            raise ValueError(f"count must be positive, got {count}")
        if count == 1:
            return _Program(self.atoms[:])

        # Repeat by sequentially shifting copies by multiples of duration
        result = _Program(self.atoms[:])
        unit = _Program(self.atoms[:])
        for _ in range(count - 1):
            result = result >> unit
        return result

    def __rmul__(self, count: int) -> "_Program":
        """Support count * program syntax."""
        return self.__mul__(count)

class Timeline:
    """
    Concrete timeline of deltas derived from an initial state and compositions.
    - Use >> to apply a Program or concatenate another Timeline.
    - Use + to overlay with another Timeline or with a Program.
    """
    def __init__(self, initial: Dict[str, Any]):
        self.initial: Dict[str, Any] = dict(initial)
        self.deltas: List[Dict[str, Any]] = []

    def __len__(self) -> int:
        """Number of frames (initial + deltas)."""
        return len(self.deltas) + 1

    def __getitem__(self, t: int) -> Dict[str, Any]:
        """State at frame t (1-based for deltas; 0 = initial)."""
        s = dict(self.initial)
        for d in self.deltas[:t]:
            s.update(d)
        return s

    def __iter__(self) -> Iterable[Dict[str, Any]]:
        """Iterate states from initial through all frames."""
        s = dict(self.initial)
        yield s
        for d in self.deltas:
            s = s | d
            yield s

    def _clone(self) -> "Timeline":
        """Shallow clone: copy initial and deltas (no deep copy of values)."""
        c = Timeline(self.initial)
        c.deltas = [dict(d) for d in self.deltas]
        return c

    def __rshift__(self, other):
        """
        Sequential:
        - Timeline >> Program → materialize atoms to extend this timeline.
        - Timeline >> Timeline → append the other's deltas.
        """
        if isinstance(other, _Program):
            L = other.duration
            if L <= 0:
                return self

            # Stable ordering: earlier-start atoms first; later ones override keys on conflicts.
            atoms = sorted(other.atoms, key=lambda a: (a.start,))

            # The captured start-state for each atom (lazily filled when the atom activates).
            captured: List[Dict[str, Any]] = [{} for _ in atoms]

            # Current state at the beginning of materialization
            cur = self[len(self.deltas)]

            # Simulate frames 1..L
            for t in range(1, L + 1):
                delta: Dict[str, Any] = {}
                for idx, a in enumerate(atoms):
                    # Active if a.start < t <= a.start + a.duration
                    if not (a.start < t <= a.start + a.duration):
                        continue

                    # Wait atoms (empty end dict) extend time but don't write deltas
                    if not a.end:
                        continue

                    # Capture start-state for the controlled keys on activation
                    if not captured[idx]:
                        # Validate keys exist
                        missing = [k for k in a.end.keys() if k not in cur]
                        if missing:
                            raise ValueError(
                                f"Tween cannot add new elements to state. "
                                f"Missing keys in start state: {sorted(missing)}. "
                                f"Available keys: {sorted(cur.keys())}."
                            )
                        captured[idx] = {k: cur[k] for k in a.end.keys()}

                    # Compute eased alpha in [0..1], where step = 1..duration
                    step = t - a.start
                    alpha = float(a.ease_fn(step / a.duration))

                    # Blend each key; last-writer-wins within the frame
                    for k, target in a.end.items():
                        start_val = captured[idx][k]
                        delta[k] = blend_values(start_val, target, alpha)

                self.deltas.append(delta)
                cur = cur | delta
            return self

        if isinstance(other, Timeline):
            # Sequential concat: append other's deltas (not states)
            self.deltas += list(other.deltas)
            return self

        return self

    def __add__(self, other):
        """
        Overlay (parallel):
        - Timeline + Timeline → framewise merge of deltas; keep left initial.
        - Timeline + Program  → materialize program on a copy, then overlay.
        """
        if isinstance(other, Timeline):
            out = self._clone()
            L = max(len(self.deltas), len(other.deltas))
            out.deltas = [
                {
                    **(self.deltas[i] if i < len(self.deltas) else {}),
                    **(other.deltas[i] if i < len(other.deltas) else {})
                }
                for i in range(L)
            ]
            return out

        if isinstance(other, _Program):
            tmp = Timeline(self.initial) >> other  # materialize from same initial state
            return self + tmp                      # overlay with timeline+timeline

        return NotImplemented

    def __radd__(self, other):
        """Support Program + Timeline and Timeline + Timeline (commuted)."""
        if isinstance(other, _Program):
            return self + other
        if isinstance(other, Timeline):
            return other + self
        if isinstance(other, Mapping):
            # Mapping + Timeline → treat mapping as initial state
            return Timeline(dict(other)) + self
        return NotImplemented

    def __mul__(self, count: int) -> "Timeline":
        """Repeat this timeline count times using * operator."""
        if not isinstance(count, int):
            return NotImplemented
        if count <= 0:
            raise ValueError(f"count must be positive, got {count}")
        if count == 1:
            return self._clone()

        result = self._clone()
        for _ in range(count - 1):
            result = result >> self
        return result

    def __rmul__(self, count: int) -> "Timeline":
        """Support count * timeline syntax."""
        return self.__mul__(count)

# -----------------------------------------------------------------------------
# Public factory (only export)
# -----------------------------------------------------------------------------

def tween(n: int = 1, *, ease: Any = "linear", **end) -> _Program:
    """
    Create a tween block (or a wait if no kwargs).
    - n: number of steps (must be > 0)
    - ease: string name ('linear', 'cubic', 'quad_in', 'quad_out')
            or a callable ease(t: float) -> float, all in range 0 to 1.
    - **end: target sub-state (e.g., x=10, y=50). If empty, this is a wait.

    Returns a _Program you can compose with + (parallel) and >> (sequential).
    Also supports dict-like on the left:
      {'x':0,'y':0} >> tween(10, x=20, ease='cubic')
      {'x':0} + tween(5, y=10)  # overlay

    EXAMPLE:
        >>> from rp.libs.tweenline import tween
        ... 
        ... timeline = dict(v=0, w=0, x=0, y=0, z=0) >> (
        ...     (
        ...         (
        ...             (tween(5, x=5) >> tween(5, x=0))
        ...             + tween(5, y=5)
        ...             + (tween(5) >> tween(5, z=5))
        ...             + tween(10, w=10)
        ...         )
        ...         >> tween(5, w=0)
        ...     )
        ...     + tween(15, v=15)
        ... )
        ... print("\n".join(map(str, timeline)))
        {'v':  0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}
        {'v':  1, 'w': 1, 'x': 1, 'y': 1, 'z': 0}
        {'v':  2, 'w': 2, 'x': 2, 'y': 2, 'z': 0}
        {'v':  3, 'w': 3, 'x': 3, 'y': 3, 'z': 0}
        {'v':  4, 'w': 4, 'x': 4, 'y': 4, 'z': 0}
        {'v':  5, 'w': 5, 'x': 5, 'y': 5, 'z': 0}
        {'v':  6, 'w': 6, 'x': 4, 'y': 5, 'z': 1}
        {'v':  7, 'w': 7, 'x': 3, 'y': 5, 'z': 2}
        {'v':  8, 'w': 8, 'x': 2, 'y': 5, 'z': 3}
        {'v':  9, 'w': 9, 'x': 1, 'y': 5, 'z': 4}
        {'v': 10, 'w':10, 'x': 0, 'y': 5, 'z': 5}
        {'v': 11, 'w': 8, 'x': 0, 'y': 5, 'z': 5}
        {'v': 12, 'w': 6, 'x': 0, 'y': 5, 'z': 5}
        {'v': 13, 'w': 4, 'x': 0, 'y': 5, 'z': 5}
        {'v': 14, 'w': 2, 'x': 0, 'y': 5, 'z': 5}
        {'v': 15, 'w': 0, 'x': 0, 'y': 5, 'z': 5}

    """
    ease_fn = _resolve_ease(ease)
    if n <= 0:
        raise ValueError(f"duration n must be a positive integer, got {n}")
    # Represent as a single atom starting at offset 0.
    return _Program([_Atom(start=0, duration=n, end=end, ease_fn=ease_fn)])


# -----------------------------------------------------------------------------
# Example (optional manual test)
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    tl = (
        Timeline(dict(x=0, y=0, z=0))
        >> (tween(10, x=20) + tween(5, y=60))
        >> tween(10)
        >> (tween(10, x=10) + tween(10, y=100))
    )
    for t, state in enumerate(tl):
        print(t, state)
