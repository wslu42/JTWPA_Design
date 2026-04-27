import gdsfactory as gf

from jtwpa_design.tech import LAYER, Layer

from .rectangle import rectangle


def _JJ_feet(width: float, height: float, layer: Layer) -> gf.Component:
    c = gf.Component()
    pts = [
        (-width / 2, -height / 2),
        (width / 2, -height / 2),
        (width / 2, height / 2),
        (-width / 2, height / 2),
    ]
    c.add_polygon(pts, layer=layer)
    c.add_port(
        "top_right", center=(width / 2 - 0.5, height / 2), orientation=90, width=1, layer=layer
    )
    c.add_port(
        "top_left", center=(-width / 2 + 0.5, height / 2), orientation=90, width=1, layer=layer
    )
    c.add_port(
        "bottom_right", center=(width / 2 - 0.5, -height / 2), orientation=270, width=1, layer=layer
    )
    c.add_port(
        "bottom_left", center=(-width / 2 + 0.5, -height / 2), orientation=270, width=1, layer=layer
    )
    return c


@gf.cell()
def JJ1(
    width: float = 1.0,
    length: float = 8.0,
    feet_width_L: float = 6,
    feet_width_R: float = 6,
    feet_height: float = 3,
    extend_L: bool = False,
    extend_R: bool = False,
) -> gf.Component:
    c = gf.Component()

    if extend_L:
        JJ_1 = c << rectangle(width=width, height=length + 1, layer=LAYER.JJ)
        JJ_1.move((0, -((length + 1) / 2 - 2.5 - width / 2)))
    else:
        JJ_1 = c << rectangle(width=width, height=length, layer=LAYER.JJ)
        JJ_1.move((0, -(length / 2 - 2.5 - width / 2)))
    if extend_R:
        JJ_2 = c << rectangle(width=length + 1, height=width, layer=LAYER.JJ)
        JJ_2.move(((length + 1) / 2 - 2.5 - width / 2, 0))
    else:
        JJ_2 = c << rectangle(width=length, height=width, layer=LAYER.JJ)
        JJ_2.move((length / 2 - 2.5 - width / 2, 0))
    extend_1 = c << _JJ_feet(width=feet_width_R, height=feet_height, layer=LAYER.JJ)
    extend_2 = c << _JJ_feet(width=feet_width_L, height=feet_height, layer=LAYER.JJ)

    JJ_1.rotate(-45)
    JJ_2.rotate(-45)
    extend_1.connect("top_right", JJ_1.ports["bottom"])
    extend_2.connect("top_left", JJ_2.ports["right"])
    c.flatten()

    return c


@gf.cell()
def JJ2(
    width: float = 1.0,
    length: float = 8.0,
    feet_width_L: float = 6,
    feet_width_R: float = 6,
    feet_height: float = 3,
    extend_L: bool = False,
    extend_R: bool = False,
):
    c = gf.Component()

    if extend_R:
        JJ_1 = c << rectangle(width=width, height=length + 1, layer=LAYER.JJ)
        JJ_1.move((0, -((length + 1) / 2 - 2.5 - width / 2)))
    else:
        JJ_1 = c << rectangle(width=width, height=length, layer=LAYER.JJ)
        JJ_1.move((0, -(length / 2 - 2.5 - width / 2)))
    if extend_L:
        JJ_2 = c << rectangle(width=length + 1, height=width, layer=LAYER.JJ)
        JJ_2.move((-((length + 1) / 2 - 2.5 - width / 2), 0))
    else:
        JJ_2 = c << rectangle(width=length, height=width, layer=LAYER.JJ)
        JJ_2.move((-(length / 2 - 2.5 - width / 2), 0))
    extend_1 = c << _JJ_feet(width=feet_width_R, height=feet_height, layer=LAYER.JJ)
    extend_2 = c << _JJ_feet(width=feet_width_L, height=feet_height, layer=LAYER.JJ)

    JJ_1.rotate(-45)
    JJ_2.rotate(-45)
    extend_1.connect("top_left", JJ_1.ports["bottom"])
    extend_2.connect("top_right", JJ_2.ports["left"])
    c.flatten()

    return c
