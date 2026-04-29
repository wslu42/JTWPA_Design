from jtwpa_design.parameters._base import ParameterModel


class OpenStubCapacitorParams(ParameterModel):
    i: int = 0
    width: float = 6.0
    length: float = 232.0
    ground_cap_gap: float = 2.0
    contact_pad_height: float = 26.0
    contact_overlap_x: float = 1.0
    contact_overlap_y: float = 3.0
    general: bool = True
