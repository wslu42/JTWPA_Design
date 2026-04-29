import gdsfactory as gf

from jtwpa_design.cells.components.open_stub_capacitor import open_stub_capacitor
from jtwpa_design.parameters.components.open_stub_capacitor import OpenStubCapacitorParams
from jtwpa_design.parameters.rules import LayoutRules


def make_open_stub_capacitor(
    params: OpenStubCapacitorParams,
    rules: LayoutRules,
) -> gf.Component:
    return open_stub_capacitor(
        i=params.i,
        width=params.width,
        length=params.length,
        ground_cap_gap=params.ground_cap_gap,
        contact_pad_height=params.contact_pad_height,
        contact_overlap_x=params.contact_overlap_x,
        contact_overlap_y=params.contact_overlap_y,
        general=params.general,
        unit_cell_spacing=rules.unit_cell.spacing,
        jj_ground_mask_width=rules.jj_ground_mask.width,
        bridge_width=rules.bridge.width,
        pier_radius=rules.bridge.pier_radius,
        pier_ground_edge=rules.bridge.pier_ground_edge_clearance,
    )
