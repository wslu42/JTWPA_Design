from jtwpa_design.parameters._base import ParameterModel


class WaferParams(ParameterModel):
    wafer_size: float = 101600.0
    wafer_id: str = "W01"
    text_size: float = 3000.0
    text_margin: float = 1000.0
    text_coordinate: float = -37500.0
