from pydantic import Field

from jtwpa_design.parameters._base import ParameterModel
from jtwpa_design.parameters.components.open_stub_capacitor import OpenStubCapacitorParams
from jtwpa_design.parameters.components.twpa_launcher import TwpaLauncherParams


class JTWPALineParams(ParameterModel):
    launcher: TwpaLauncherParams = Field(default_factory=TwpaLauncherParams)
    capacitor: OpenStubCapacitorParams = Field(default_factory=OpenStubCapacitorParams)
