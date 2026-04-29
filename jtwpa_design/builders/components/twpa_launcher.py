import gdsfactory as gf

from jtwpa_design.cells.components.twpa_launcher import twpa_launcher
from jtwpa_design.parameters.components.twpa_launcher import TwpaLauncherParams
from jtwpa_design.parameters.rules import LayoutRules


def make_twpa_launcher(
    params: TwpaLauncherParams,
    rules: LayoutRules,
) -> gf.Component:
    return twpa_launcher(
        pad_height=params.pad_height,
        pad_width=params.pad_width,
        taper_length=params.taper_length,
        gapx=params.gapx,
        gapy=params.gapy,
        cpw_width=rules.cpw.width,
        cpw_gap=rules.cpw.gap,
    )
