import gdsfactory as gf

from jtwpa_design.tech import Layer


@gf.cell
def rectangle(width: float, height: float, layer: Layer) -> gf.Component:
    c = gf.Component()
    pts = [
        (-width / 2, -height / 2),
        (width / 2, -height / 2),
        (width / 2, height / 2),
        (-width / 2, height / 2),
    ]
    c.add_polygon(pts, layer=layer)
    c.add_port("top", center=(0, height / 2), orientation=90, width=1, layer=layer)
    c.add_port("bottom", center=(0, -height / 2), orientation=270, width=1, layer=layer)
    c.add_port("left", center=(-width / 2, 0), orientation=180, width=1, layer=layer)
    c.add_port("right", center=(width / 2, 0), orientation=0, width=1, layer=layer)
    c.add_port("center", center=(0, 0), orientation=0, width=1, layer=layer)
    return c
