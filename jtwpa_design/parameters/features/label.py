from jtwpa_design.parameters._base import ParameterModel


class ChipLabelStyleParams(ParameterModel):
    text_size: float = 300.0
    text_margin: float = 50.0


class WaferLabelStyleParams(ParameterModel):
    text_size: float = 3000.0
    text_margin: float = 1000.0
    text_coordinate: float = -37500.0
