from jtwpa_design.parameters._base import ParameterModel


class SpiralParams(ParameterModel):
    chip_size: float = 6000.0
    wafer_id: str = "W01"
    chip_id: str = "C01"
    text_size: float = 300.0
    text_margin: float = 50.0
    marker_coordinate: float = 2200.0
    marker_size: float = 100.0
    marker_width: float = 4.0
    marker_boundary: float = 50.0
    include_dicing: bool = True
