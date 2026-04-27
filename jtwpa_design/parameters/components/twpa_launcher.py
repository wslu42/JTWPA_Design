from jtwpa_design.parameters._base import ParameterModel


class TwpaLauncherParams(ParameterModel):
    pad_height: float = 261.0
    pad_width: float = 178.0 
    taper_length: float = 115.0
    gapx: float = 82.0
    gapy: float = 76.0
    cpw_width: float = 17.0
    cpw_gap: float = 10.0
