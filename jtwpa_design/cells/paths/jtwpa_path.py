import gdsfactory as gf

from jtwpa_design.helpers.arch_spiral import arch_spiral


def jtwpa_path() -> gf.Path:
    p = arch_spiral(1000, 314, 2.1355, 1000, start_theta=0.0959931, reverse=True)
    p += gf.path.straight(96.724)
    p += gf.path.arc(radius=500, angle=180)
    p += gf.path.arc(radius=500, angle=-180)
    p += gf.path.straight(96.724)
    p += arch_spiral(1000, 314, 2.1355, 1000, start_theta=0.0959931, reverse=False)
    return p
