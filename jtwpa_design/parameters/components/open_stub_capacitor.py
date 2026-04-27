from jtwpa_design.parameters._base import ParameterModel


class OpenStubCapacitorParams(ParameterModel):
    i: int = 0
    width: float = 6.0
    length: float = 232.0
    ground_cap_gap: int = 2
    contact_pad_height: float = 26.0
    contact_overlap_x: float = 1.0
    contact_overlap_y: float = 3.0
    unit_cell_spacing: float = 20.0
    jj_ground_mask_width: float = 32.0
    bridge_width: float = 8.0
    pier_radius: float = 2.5
    pier_ground_edge: float = 3.0
    general: bool = True
