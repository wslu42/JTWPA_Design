import gdsfactory as gf

from jtwpa_design.cells.components.rectangle import rectangle
from jtwpa_design.tech import LAYER


@gf.cell
def text_id(id: str = "W01", text_size: float = 300, margin: float = 50) -> gf.Component:
    c = gf.Component()
    text = c << gf.components.text(text=id, size=text_size, layer=LAYER.MAIN_METAL)
    text.move((-c.x, -c.y))
    c << rectangle(width=c.xsize + 2 * margin, height=c.ysize + 2 * margin, layer=LAYER.GROUND_MASK)
    return c
