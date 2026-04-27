import numpy as np

def tukey_window(i, N, alpha=0.5):
    i = np.asarray(i, dtype=float)
    n = i - 1.0

    if alpha <= 0:
        return np.ones_like(n)
    if alpha >= 1:
        return 0.5*(1 - np.cos(2*np.pi*n/(N-1)))

    aN = alpha*(N-1.0)
    w = np.ones_like(n)
    left  = n <  aN/2
    right = n > (N-1)*(1 - alpha/2)

    w[left]  = 0.5*(1 + np.cos(np.pi*(2*n[left]/aN - 1)))
    w[right] = 0.5*(1 + np.cos(np.pi*(2*n[right]/aN - 2/alpha + 1)))
    return w