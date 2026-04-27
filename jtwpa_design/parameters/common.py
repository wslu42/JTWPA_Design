from ._base import ParameterModel


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
    pier_ground_edge: float = 3.0
