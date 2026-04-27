import gdsfactory as gf
import numpy as np

def arch_spiral(min_bend_radius, separation, loops, npoints, start_theta=0.0, reverse=False) -> gf.Path:
    thetas = np.linspace(start_theta, loops*2*np.pi, npoints)
    r = (separation/np.pi)*thetas + min_bend_radius
    xy = np.stack([r*np.sin(thetas), r*np.cos(thetas)], axis=1)

    if reverse:
        xy = xy[::-1]

    return gf.Path(xy)