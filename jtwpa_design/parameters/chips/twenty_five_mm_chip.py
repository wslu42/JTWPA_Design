from pydantic import Field

from jtwpa_design.parameters._base import ParameterModel
from jtwpa_design.parameters.chips.spiral import SpiralChipParams
from jtwpa_design.parameters.chips.test import TestChipParams


class TwentyFiveMMChipParams(ParameterModel):
    chip_size: float = 25000.0
    spiral_chip: SpiralChipParams = Field(default_factory=SpiralChipParams)
    test_chip: TestChipParams = Field(default_factory=TestChipParams)
    marker_size: float = 400.0
    marker_width: float = 20.0
    marker_boundary: float = 200.0
    marker_coordinate: float = 11200.0
