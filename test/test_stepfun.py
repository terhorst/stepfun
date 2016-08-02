import pytest
import numpy as np

from stepfun import StepFunction
from stepfun.stepfun import _same_support

@pytest.fixture
def s0():
    return StepFunction([-np.inf, np.inf], [0.])

@pytest.fixture
def s1():
    return StepFunction([-np.inf, np.inf], [1.])

@pytest.fixture
def heaviside():
    return StepFunction([-np.inf, 0, np.inf], [-1., 1.])

@pytest.fixture
def onepfive():
    return StepFunction([-10, 0, 1.5, 10], [1, 10, 2])

@pytest.fixture
def twothree():
    return StepFunction([-10, 0, 2, 3, 10], [1, -1, 1, 2])

def test_check_len():
    with pytest.raises(RuntimeError) as e:
        StepFunction([1.], [1.])

def test_combine(s1, heaviside):
    s = StepFunction([-np.inf, 0., 1., .2, np.inf], [1., 1., 1., 1.])
    assert s1 == s
    s = StepFunction([-np.inf, -1, 0., 1., .2, np.inf], [-1., -1., 1., 1., 1.])
    assert s == heaviside
    s = StepFunction([-np.inf, -1, 0., 1., .2, np.inf], [-1., -1., 1., 1., 2.])
    assert s != heaviside

def test_compatible(heaviside, onepfive):
    assert not _same_support(heaviside, onepfive)
    with pytest.raises(TypeError) as e:
        heaviside <= onepfive
    with pytest.raises(TypeError) as e:
        heaviside >= onepfive

def test_eq(s1, heaviside, onepfive):
    assert s1 == s1
    assert s1 != heaviside
    assert heaviside == heaviside
    assert heaviside != onepfive

def test_ge(s1, heaviside, onepfive):
    for f in (s1, heaviside, onepfive):
        assert f >= f
    assert s1 >= heaviside
    with pytest.raises(TypeError) as e:
        assert not heaviside >= onepfive
    with pytest.raises(TypeError) as e:
        assert not onepfive >= heaviside

def test_le(s1, heaviside, onepfive):
    for f in (s1, heaviside, onepfive):
        assert f <= f
    assert -s1 <= -heaviside
    with pytest.raises(TypeError) as e:
        assert not onepfive <= heaviside
    with pytest.raises(TypeError) as e:
        assert not heaviside <= onepfive

def test_lt(s1, heaviside, onepfive):
    for f in (s1, heaviside, onepfive):
        assert not f < f
    with pytest.raises(TypeError) as e:
        onepfive < heaviside
    with pytest.raises(TypeError) as e:
        heaviside < onepfive

def test_gt(s1, heaviside, onepfive):
    for f in (s1, heaviside, onepfive):
        assert not f > f
    assert not s1 > heaviside
    with pytest.raises(TypeError) as e:
        onepfive > heaviside
    with pytest.raises(TypeError) as e:
        heaviside > onepfive

def test_add(s1, heaviside):
    assert s1 + s1 == StepFunction([-np.inf, np.inf], [2.])
    assert s1 + heaviside == StepFunction([-np.inf, 0, np.inf], [0., 2.])

def test_add_uneven(onepfive, twothree):
    assert onepfive + twothree == StepFunction([-10, 0, 1.5, 2, 3, 10], [2, 9, 1, 3, 4])

def test_sub(s1, heaviside):
    assert s1 - s1 == StepFunction([-np.inf, np.inf], [0.])
    assert s1 + heaviside == StepFunction([-np.inf, 0, np.inf], [0., 2.])

def test_neg(s1, heaviside):
    assert s1 - s1 == s1 + (-s1)

def test_mul(s1, heaviside):
    assert s1 * s1 == s1
    assert s1 * heaviside == heaviside * s1
    assert s1 * heaviside == StepFunction([-np.inf, 0, np.inf], [-1, 1])

def test_mul(s0, s1, heaviside):
    assert s1 * s1 == s1
    assert heaviside * heaviside == s1
    assert s0 * s1 == s0 * heaviside == s0

def test_mul_cons(s0, s1):
    assert 0 * s1 == s1 * 0 == s0
    assert -1 * s1 == s1 * -1 == -s1

def test_div_cons(s0, s1):
    assert s1 / 1. == s1
    assert 0 / s1 == s0

def test_div(s0, s1, heaviside):
    assert s1 / s1 == s1
    assert s0 / s1 == s0
    assert s1 / heaviside == heaviside / s1 == heaviside

def test_pow(s1, heaviside, onepfive):
    assert s1**2 == s1 * s1 == s1
    assert heaviside**2 == s1
    assert onepfive * onepfive == onepfive**2

def test_noninf():
    s = StepFunction([-2., 2.], [1.])
    s2 = StepFunction([-2., 1., 2.], [1., -1])
    assert (s * s2) == s2

def test_integral(s1):
    assert s1.integral() == np.inf
    s2 = StepFunction([-2., 1., 2.], [1., -1])
    assert s2.integral() == 3 - 1
    s3 = StepFunction([-np.inf, -1, 1, np.inf], [0., 1., 0.])
    assert (s1 * s3).integral() == 2

def test_repr(s1):
    assert repr(s1) == """StepFunction(x=array([-inf,  inf]), y=array([ 1.]))"""
    array = np.array
    inf = np.inf
    assert eval(repr(s1)) == s1

def test_abs(s1, heaviside):
    assert abs(heaviside) == s1

def test_K(s1, heaviside, onepfive):
    assert s1.K == 1
    assert heaviside.K == 2
    assert onepfive.K == 3
