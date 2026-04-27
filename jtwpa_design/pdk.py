from functools import lru_cache
from typing import cast

from gdsfactory.cross_section import get_cross_sections
from gdsfactory.get_factories import get_cells
from gdsfactory.pdk import Pdk
from gdsfactory.typings import ComponentFactory
from qpdk import get_pdk as get_base_pdk


@lru_cache
def get_pdk() -> Pdk:
    from jtwpa_design import cells, tech

    project_cells = cast(
        dict[str, ComponentFactory],
        get_cells(cells),
    )

    return Pdk(
        name="jtwpa_design",
        base_pdks=[get_base_pdk()],
        cells=project_cells,
        cross_sections=get_cross_sections(cells.xsections),
        layers=tech.LAYER,
        layer_views=tech.LAYER_VIEWS,
        # layer_stack=tech.LAYER_STACK,
        # connectivity=tech.LAYER_CONNECTIVITY,
        # routing_strategies=tech.routing_strategies,
    )


def __getattr__(name: str):
    if name == "PDK":
        return get_pdk()
    raise AttributeError(f"module {__name__} has no attribute {name}")
