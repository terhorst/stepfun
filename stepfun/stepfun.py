import numpy as np
import operator


def _reconcile(s1, s2):
    pts = np.unique(np.sort(np.concatenate([s1._x, s2._x])))
    # Handle case when endpoints are inf
    cpts = pts.copy()
    cpts[0] = min(np.min(cpts[1:]), 0.) - 1
    cpts[-1] = max(np.max(cpts[:-1]), 0.) + 1
    mps = (cpts[1:] + cpts[:-1]) / 2.
    return [(pts, s(mps)) for s in (s1, s2)]
    

class StepFunction:
    '''A step function.'''
    def __init__(self, x, y):
        '''Initialize step function with breakpoints x and function values y.

        x and y are arrays such that

            f(z) = y[k], x[k] <= z < x[k + 1], 0 <= k < K.

        Thus, len(x) == len(y) + 1 and domain of f is (x[0], x[K - 1]).
        '''
        if len(x) != 1 + len(y):
            raise RuntimeError("len(x) != 1 + len(y)")
        self._x = np.array(x)
        self._y = np.array(y)
        self._compress()

    def _compress(self):
        # Combine steps which have equal values
        ny = np.concatenate([[np.nan], self._y, [np.nan]])
        ys = np.diff(ny) != 0
        self._x = self._x[ys]
        self._y = self._y[ys[:-1]]

    def _binary_op(self, other, op, desc):
        if isinstance(other, StepFunction):
            (s1_x, s1_y), (s2_x, s2_y) = _reconcile(self, other)
            return StepFunction(s1_x, op(s1_y, s2_y))
        # Fall back to normal semantics otherwise
        return StepFunction(self._x, op(self._y, other))


    def __add__(self, other):
        return self._binary_op(other, operator.add, "add")

    def __radd__(self, other):
        return self + other


    def __sub__(self, other):
        return self._binary_op(other, operator.sub, "subtract")


    def __rsub__(self, other):
        return -self + other


    def __mul__(self, other):
        return self._binary_op(other, operator.mul, "multiply")


    def __rmul__(self, other):
        return self * other


    def __div__(self, other):
        return self._binary_op(other, operator.div, "divide")


    def __rdiv__(self, other):
        return (self**-1) * other


    def __neg__(self):
        return StepFunction(self._x, -self._y)


    def __pow__(self, p):
        return StepFunction(self._x, pow(self._y, p))

    
    def __eq__(self, other):
        if isinstance(other, StepFunction):
            return np.array_equal(self._x, other._x) and np.array_equal(self._y, other._y)
        return False


    def __call__(self, s):
        return self._y[np.searchsorted(self._x, s, side="right") - 1]


    def __str__(self):
        return "Step function\nx: %s\ny: %s" % (str(self._x), str(self._y))


    def __repr__(self):
        return "StepFunction(x=%s, y=%s)" % (repr(self._x), repr(self._y))


    def integral(self):
        nz = self._y != 0
        d = np.diff(self._x)
        return (d[nz] * self._y[nz]).sum()
