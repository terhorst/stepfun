``stepfun`` is a Python class for representing mathematical
step functions. It supports simple arithmetic operations (addition,
subtraction, multiplication, etc.) as well as vectorized evaluation and
integration.

Usage
=====
A step function :math:`f(z)` with :math:`K \ge 1` steps is specified by
real numbers :math:`x_0 < x_1 < \cdots < x_K` and :math:`y_1 < \cdots <
y_K` such that

.. math::

    f(z) = y_k, x_k \le z < x_{k+1}.

The function is undefined for :math:`x \notin [x_0, x_K)`. It is fine
to set :math:`x_0 = -\infty` and/or :math:`x_K = \infty`, allowing
:math:`f` to be supported on the entire real line.

.. code:: python

    >>> from stepfun import StepFunction
    >>> inf = float("infinity")
    >>> s1 = StepFunction(x=[-inf, +inf], y=[1.]) # constant function s1 = 1
    >>> s1
    StepFunction(x=array([-inf,  inf]), y=array([ 1.]))

Mathematical operations
-----------------------
Step functions are closed under the usual operations of addition,
subtraction, multiplication, etc. 

.. code:: python
    
    >>> s1 + s1
    StepFunction(x=array([-inf,  inf]), y=array([ 2.]))
    >>> s2 = StepFunction(x=[-inf, +inf], y=[ 2. ])
    >>> s2 - s1
    StepFunction(x=array([-inf,  inf]), y=array([ 1.]))
    >>> s2 / s1 == s2
    True
    >>> s1 / s2
    StepFunction(x=array([-inf,  inf]), y=array([ 0.5]))

Equality
++++++++
Equality testing is supported, and requires that all elements of both
:math:`\mathbf{x}` and :math:`\mathbf{y}` match exactly.

.. code:: python

    >> s1 == s1
    True
    >> s1 + s1 == s2
    True
    >> s1 == s2
    False
    >> s1 == StepFunction(x=[-inf, 0., inf], y=[1., 1.])
    True # see "Breakpoint compatibility", below

Unary operations
++++++++++++++++
Unary options such as negation and powers are also supported.
    
.. code:: python
    
    >>> s2**2
    StepFunction(x=array([-inf,  inf]), y=array([ 4.]))
    >>> -s1
    StepFunction(x=array([-inf,  inf]), y=array([-1.]))


Breakpoint compatibility
++++++++++++++++++++++++
In the above examples, functions ``s1`` and ``s2`` were defined on the
same set of break points, but this is not necessary in general.

.. code:: python

    >>> s3 = StepFunction(x=[-inf, -1., 1., inf], y=[0, 1., 0])
    >>> s4 = StepFunction(x=[-inf, -1., 0.5, 1.0, inf], y=[0, 1., 2., 3.])
    >>> s3 + s4
    StepFunction(x=array([-inf, -1. ,  0.5,  inf]), y=array([ 0.,  2.,  3.]))

Note that the class constructor will automatically eliminate redundant
elements of the representation.

.. code:: python

    >>> s3 - s3
    StepFunction(x=array([-inf,  inf]), y=array([ 0.]))
    >>> StepFunction(x=[-inf, 0., inf], y=[0., 0.])
    StepFunction(x=array([-inf,  inf]), y=array([ 0.]))


Scalar operations
+++++++++++++++++

It is possible to perform scalar operations on step functions. Any
operand which is not recognized as a companion step function is "passed
through" to the underlying array of :math:`\mathbf{y}` values.

.. code:: python

    >>> s1 * 2
    StepFunction(x=array([-inf,  inf]), y=array([ 2.]))
    >>> s1 - 1 == 0 * s1
    True
    >>> s1 * "error" # don't know how to multiply y by string
    Traceback (most recent call last):
        ...
    TypeError: ...

Evaluation
++++++++++

Step functions may be evaluated using the ``__call__()`` syntax.

.. code:: python

    >>> s1(1.0)
    1.0
    >>> s2(100.0)
    2.0

Vectorized evaluation is also supported.

.. code:: python

    >>> s1([-1, 1, 2, 10])
    array([ 1.,  1.,  1.,  1.])
    >>> s3([-1, 0., 1.5, 2])
    array([ 1.,  1.,  0.,  0.])


Integration
+++++++++++

The ``integral()`` method returns the Riemann integral of the
step function over its domain.

.. code:: python
    
    >>> s1.integral()
    inf
    >>> impulse = StepFunction(x=[-1, 0, 1], y=[-1, 1]) / 2**.5
    >>> impulse.integral()
    0.0
    >>> (impulse**2).integral()
    0.99999999999999978


Installation
============

.. code:: bash

    $ pip install stepfun

Requirements
============
Numpy.

Author
======
Jonathan Terhorst <terhorst@gmail.com>
