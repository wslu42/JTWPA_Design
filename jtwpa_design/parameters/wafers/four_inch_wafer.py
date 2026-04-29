from pydantic import Field

from jtwpa_design.parameters._base import ParameterModel
from jtwpa_design.parameters.chips.twenty_five_mm_chip import TwentyFiveMMChipParams
from jtwpa_design.parameters.features.label import WaferLabelStyleParams


class WaferParams(ParameterModel):
    wafer_size: float = 101600.0
    wafer_id: str = "W01"
    label: WaferLabelStyleParams = Field(default_factory=WaferLabelStyleParams)
    twenty_five_mm_chip: TwentyFiveMMChipParams = Field(default_factory=TwentyFiveMMChipParams)
