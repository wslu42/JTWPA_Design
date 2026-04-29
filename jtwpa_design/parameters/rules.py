from pydantic import Field

from jtwpa_design.parameters._base import ParameterModel


class CPWParams(ParameterModel):
    width: float = 17.0
    gap: float = 10.0


class UnitCellParams(ParameterModel):
    spacing: float = 20.0


class JJGroundMaskParams(ParameterModel):
    width: float = 32.0


class BridgeParams(ParameterModel):
    width: float = 8.0
    pier_radius: float = 2.5
    pier_ground_edge_clearance: float = 3.0


class LayoutRules(ParameterModel):
    cpw: CPWParams = Field(default_factory=CPWParams)
    unit_cell: UnitCellParams = Field(default_factory=UnitCellParams)
    jj_ground_mask: JJGroundMaskParams = Field(default_factory=JJGroundMaskParams)
    bridge: BridgeParams = Field(default_factory=BridgeParams)
