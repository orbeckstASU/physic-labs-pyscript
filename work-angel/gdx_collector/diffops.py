# differentiation operator module

def D_fd(y, t, h):
    """Forward difference"""
    ### my implementations
    forward_diff = (y(t+h) - y(t))/h
    return forward_diff


def D_cd(y, t, h):
    """Central difference"""
    central_diff = (y(t + h/2) - y(t - h/2)) / h
    return central_diff


def D_ed(y, t, h):
    """Extended difference"""
    ext_diff = (8 * (y(t + h / 4) - y(t - h / 4)) - (y(t + h / 2) - y(t - h / 2))) / (3 * h)
    return ext_diff


# code for testing differentiation


def error(Dxx, y, y1, t, h):
    """Relative error.

    Parameters
    ----------
    Dxx : function
          The derivative function must have call signature Dxx(y, t,
          h) where y is a numpy ufunc, t is an array of values at
          which to determine dy(t)/dt, h is the step size for the
          finite difference operator.
    y : function
          numpy ufunc that for which the derivative is evaluated
    y1 : function
          numpy ufunc that implements the exact analytical derivative
          of y: y1(t) = y'(t) = dy/dt
    t : float or array
          evaluate dy/dt at all points in t
    h : float or array
          step size for the finite difference algorithm

    Returns
    -------
    errors : array
         Array of errors for all t values at fixed h or for all h values at fixed t,
         (approx - analytical)/analytical.
    """
    # Hint: write E = (Dy(t) - y'(t))/y'(t) with numpy ufuncs (it will
    # just be a single line if you have defined your Dxx, y, and y1 as
    # ufuncs)
    rel_error = (Dxx(y, t, h) - y1(t)) / y1(t)
    return rel_error



