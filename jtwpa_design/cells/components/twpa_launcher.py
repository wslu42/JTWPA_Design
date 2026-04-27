import gdsfactory as gf

from jtwpa_design.tech import LAYER


@gf.cell
def twpa_launcher(
    pad_height: float = 261.0,
    pad_width: float = 178.0,
    taper_length: float = 115.0,
    gapx: float = 82.0,
    gapy: float = 76.0,
    cpw_width: float = 17.0,
    cpw_gap: float = 10.0,
) -> gf.Component:
    c = gf.Component()
    dy = (pad_height - cpw_width) / 2
    pts = [
        (0, 0),
        (pad_width, 0),
        (pad_width + taper_length, dy),
        (pad_width + taper_length, dy + cpw_width),
        (pad_width, pad_height),
        (0, pad_height),
    ]
    c.add_polygon(pts, layer=LAYER.MAIN_METAL)

    region_pts = [
        (-gapx, -gapy),
        (pad_width, -gapy),
        (pad_width + taper_length, dy - cpw_gap),
        (pad_width + taper_length, dy + cpw_width + cpw_gap),
        (pad_width, pad_height + gapy),
        (-gapx, pad_height + gapy),
    ]
    c.add_polygon(region_pts, layer=LAYER.GROUND_MASK)

    # 左中
    c.add_port(
        name="left",
        center=(0, pad_height / 2),
        orientation=180,  # 朝左
        width=1,
        layer=LAYER.MAIN_METAL,
    )

    # 右中
    c.add_port(
        name="right",
        center=(pad_width + taper_length, pad_height / 2),
        orientation=0,  # 朝右
        width=37,
        layer=LAYER.MAIN_METAL,
    )

    return c
