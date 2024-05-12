def powers_of(logbase, count, lower=0, include_zero=True):
    """Returns a list of count powers of logbase (from logbase**lower)."""
    if not include_zero:
        return [logbase**i for i in range(lower, count + lower)]
    else:
        return [0] + [logbase**i for i in range(lower, count + lower)]
