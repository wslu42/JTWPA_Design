import gdsfactory as gf
import numpy as np
from gdsfactory.cross_section import ComponentAlongPath

from jtwpa_design.cells.components.dicing import dicing
from jtwpa_design.cells.components.JJ import JJ1, JJ2
from jtwpa_design.cells.components.marker import four_marker
from jtwpa_design.cells.components.open_stub_capacitor import open_stub_capacitor
from jtwpa_design.cells.components.rectangle import rectangle
from jtwpa_design.cells.components.text_id import text_id
from jtwpa_design.cells.components.twpa_launcher import twpa_launcher
from jtwpa_design.cells.paths.jtwpa_path import jtwpa_path
from jtwpa_design.config import PATH
from jtwpa_design.helpers.generate_bridge_paths import create_bridge_paths
from jtwpa_design.helpers.tukey_window import tukey_window
from jtwpa_design.parameters.chips.spiral import SpiralParams
from jtwpa_design.parameters.common import BridgeParams, CPWParams, JJGroundMaskParams
from jtwpa_design.parameters.components.dicing import DicingParams
from jtwpa_design.parameters.components.open_stub_capacitor import OpenStubCapacitorParams
from jtwpa_design.parameters.components.twpa_launcher import TwpaLauncherParams
from jtwpa_design.tech import LAYER


@gf.cell()
def capacitors_JJs() -> gf.Component:
    capacitor_points = np.load(
        "jtwpa_design/cells/chips/npy/arranged_capacitor_points.npy", allow_pickle=False
    )
    JJ_arch_spiral = np.load("jtwpa_design/cells/chips/npy/JJ_arch_spiral.npy", allow_pickle=False)
    JJ_arc1 = np.load("jtwpa_design/cells/chips/npy/JJ_arc1.npy", allow_pickle=False)
    JJ_arc2 = np.load("jtwpa_design/cells/chips/npy/JJ_arc2.npy", allow_pickle=False)
    c = gf.Component()

    num_of_capacitors = len(capacitor_points)

    boundary_capacitor_params = OpenStubCapacitorParams(length=116.0, general=False)
    first_capacitor = c << open_stub_capacitor(**boundary_capacitor_params.to_kwargs())
    first_capacitor.rotate(-capacitor_points[0][2])
    first_capacitor.move((capacitor_points[0][0], capacitor_points[0][1]))
    final_capacitor = c << open_stub_capacitor(**boundary_capacitor_params.to_kwargs())
    final_capacitor.rotate(-capacitor_points[num_of_capacitors - 1][2])
    final_capacitor.move(
        (capacitor_points[num_of_capacitors - 1][0], capacitor_points[num_of_capacitors - 1][1])
    )

    for i in range(1, num_of_capacitors - 1):
        W = tukey_window(i, num_of_capacitors - 2, alpha=0.5)
        phase = np.cos(2 * np.pi * (i - 0.5) / 30)
        i_capacitor_length = 232 * (1 + 0.08 * W * phase) ** (-2)
        i_capacitor_params = OpenStubCapacitorParams(i=i - 1, length=i_capacitor_length)
        cx = capacitor_points[i][0]
        cy = capacitor_points[i][1]
        if 1 <= i <= 1122:
            i_capacitor = c << open_stub_capacitor(**i_capacitor_params.to_kwargs())
            i_capacitor.rotate(-capacitor_points[i][2])
            i_capacitor.move((cx, cy))
        elif 1123 <= i <= 1200:
            i_capacitor = c << open_stub_capacitor(**i_capacitor_params.to_kwargs())
            i_capacitor.rotate(-np.degrees(np.arctan2(cx, cy - 500)))
            i_capacitor.move((cx, cy))
        elif 1201 <= i <= 1279:
            i_capacitor = c << open_stub_capacitor(**i_capacitor_params.to_kwargs())
            theta_deg = np.degrees(np.arctan2(cx, cy + 500))
            if -10 < cx < 10 and -10 < cy < 10:
                theta_deg = 2
            i_capacitor.rotate(-theta_deg)
            i_capacitor.move((cx, cy))
        else:
            i_capacitor = c << open_stub_capacitor(**i_capacitor_params.to_kwargs())
            i_capacitor.rotate(-capacitor_points[i][2])
            i_capacitor.move((cx, cy))

    for cx, cy in JJ_arch_spiral:
        theta_deg = np.degrees(np.arctan2(cy, cx))
        if -1757 < cx < -1755 and -1545 < cy < -1543:
            JJ_ref = c << JJ1(feet_width_R=8, extend_R=True)
            JJ_ref.move((1, 1))
            JJ_ref.rotate(-15)
        elif 1747 < cx < 1749 and 1554 < cy < 1556:
            JJ_ref = c << JJ1(feet_width_R=10)
            JJ_ref.move((1, 1))
            JJ_ref.rotate(-15)
        elif 75 <= abs(theta_deg) <= 105:
            JJ_ref = c << JJ1(feet_width_L=8, feet_width_R=8)
            JJ_ref.rotate(-15)
        elif 60 <= theta_deg < 75 or -120 <= theta_deg < -105:
            JJ_ref = c << JJ1(feet_width_R=8)
            JJ_ref.rotate(-15)
        elif 30 <= theta_deg < 60 or -150 <= theta_deg < -120:
            JJ_ref = c << JJ1(feet_width_R=10, extend_R=True)
            JJ_ref.move((1, 1))
            JJ_ref.rotate(-15)
        elif 105 < theta_deg <= 120 or -75 < theta_deg <= -60:
            JJ_ref = c << JJ1(feet_width_L=10)
            JJ_ref.move((-1, 1))
            JJ_ref.rotate(-15)
        elif abs(theta_deg) <= 15 or abs(theta_deg) >= 165:
            JJ_ref = c << JJ2(feet_width_L=8, feet_width_R=8)
            JJ_ref.rotate(-15)
        elif 150 <= theta_deg < 165 or -30 <= theta_deg < -15:
            JJ_ref = c << JJ2(feet_width_L=8)
            JJ_ref.rotate(-15)
        elif 120 < theta_deg < 150 or -60 < theta_deg < -30:
            JJ_ref = c << JJ2(feet_width_L=10, extend_R=True)
            JJ_ref.move((1, -1))
            JJ_ref.rotate(-15)
        elif 15 < theta_deg <= 30 or -165 < theta_deg <= -150:
            JJ_ref = c << JJ2(feet_width_R=10)
            JJ_ref.move((1, 1))
            JJ_ref.rotate(-15)
        else:
            continue
        JJ_ref.move((cx, cy))
    for cx, cy in JJ_arc1:
        theta_deg = np.degrees(np.arctan2(cy - 500, cx))
        if 75 <= abs(theta_deg) <= 105:
            JJ_ref = c << JJ1(feet_width_L=8, feet_width_R=8)
            JJ_ref.rotate(-15)
        elif 60 <= theta_deg < 75 or -120 <= theta_deg < -105:
            JJ_ref = c << JJ1(feet_width_R=8)
            JJ_ref.rotate(-15)
        elif 30 <= theta_deg < 60 or -150 <= theta_deg < -120:
            JJ_ref = c << JJ1(feet_width_R=10, extend_R=True)
            JJ_ref.move((1, 1))
            JJ_ref.rotate(-15)
        elif 105 < theta_deg <= 120 or -75 < theta_deg <= -60:
            JJ_ref = c << JJ1(feet_width_L=10)
            JJ_ref.move((-1, 1))
            JJ_ref.rotate(-15)
        elif abs(theta_deg) <= 15 or abs(theta_deg) >= 165:
            JJ_ref = c << JJ2(feet_width_L=8, feet_width_R=8)
            JJ_ref.rotate(-15)
        elif 150 <= theta_deg < 165 or -30 <= theta_deg < -15:
            JJ_ref = c << JJ2(feet_width_L=8)
            JJ_ref.rotate(-15)
        elif 120 < theta_deg < 150 or -60 < theta_deg < -30:
            JJ_ref = c << JJ2(feet_width_L=10, extend_R=True)
            JJ_ref.move((1, -1))
            JJ_ref.rotate(-15)
        elif 15 < theta_deg <= 30 or -165 < theta_deg <= -150:
            JJ_ref = c << JJ2(feet_width_R=10)
            JJ_ref.move((1, 1))
            JJ_ref.rotate(-15)
        else:
            continue
        JJ_ref.move((cx, cy))
    for cx, cy in JJ_arc2:
        theta_deg = np.degrees(np.arctan2(cy + 500, cx))
        if 75 <= abs(theta_deg) <= 105:
            JJ_ref = c << JJ1(feet_width_L=8, feet_width_R=8)
            JJ_ref.rotate(-15)
        elif 60 <= theta_deg < 75 or -120 <= theta_deg < -105:
            JJ_ref = c << JJ1(feet_width_R=8)
            JJ_ref.rotate(-15)
        elif 30 <= theta_deg < 60 or -150 <= theta_deg < -120:
            JJ_ref = c << JJ1(feet_width_R=10, extend_R=True)
            JJ_ref.move((1, 1))
            JJ_ref.rotate(-15)
        elif 105 < theta_deg <= 120 or -75 < theta_deg <= -60:
            JJ_ref = c << JJ1(feet_width_L=10)
            JJ_ref.move((-1, 1))
            JJ_ref.rotate(-15)
        elif abs(theta_deg) <= 15 or abs(theta_deg) >= 165:
            JJ_ref = c << JJ2(feet_width_L=8, feet_width_R=8)
            JJ_ref.rotate(-15)
        elif 150 <= theta_deg < 165 or -30 <= theta_deg < -15:
            JJ_ref = c << JJ2(feet_width_L=8)
            JJ_ref.rotate(-15)
        elif 120 < theta_deg < 150 or -60 < theta_deg < -30:
            JJ_ref = c << JJ2(feet_width_L=10, extend_R=True)
            JJ_ref.move((1, -1))
            JJ_ref.rotate(-15)
        elif 15 < theta_deg <= 30 or -165 < theta_deg <= -150:
            JJ_ref = c << JJ2(feet_width_R=10)
            JJ_ref.move((1, 1))
            JJ_ref.rotate(-15)
        else:
            continue
        JJ_ref.move((cx, cy))

    c.add_port("center", center=(0, 0), orientation=0, width=1, layer=LAYER.GROUND_MASK)
    c.flatten()

    return c


@gf.cell()
def JJ_ground_mask() -> gf.Component:
    p = jtwpa_path()
    mask_section = gf.Section(
        width=JJGroundMaskParams().width, offset=0, layer=LAYER.GROUND_MASK, port_names=("o1", "o2")
    )
    x = gf.CrossSection(sections=(mask_section,))
    c = gf.path.extrude(p, cross_section=x)
    c.add_port("center", center=(0, 0), orientation=180, width=1, layer=LAYER.GROUND_MASK)
    return c


@gf.cell()
def bridge_on_cpw() -> gf.Component:
    c = gf.Component()
    pier_radius = BridgeParams().pier_radius
    bridge_width = BridgeParams().width
    pier_ground_edge = BridgeParams().pier_ground_edge
    cpw_width = CPWParams().width
    cpw_gap = CPWParams().gap
    pier1 = c << gf.components.circle(radius=pier_radius, layer=LAYER.AIR_BRIDGE_CONTACT)
    pier1.movey(cpw_width / 2 + cpw_gap + pier_radius + pier_ground_edge)
    pier2 = c << gf.components.circle(radius=pier_radius, layer=LAYER.AIR_BRIDGE_CONTACT)
    pier2.movey(-(cpw_width / 2 + cpw_gap + pier_radius + pier_ground_edge))
    c << rectangle(
        width=bridge_width,
        height=cpw_width
        + 2 * cpw_gap
        + 2 * pier_ground_edge
        + 4 * pier_radius
        + (bridge_width - 2 * pier_radius),
        layer=LAYER.AIR_BRIDGE,
    )
    return c


@gf.cell()
def twpa_cpw() -> gf.Component:
    via = ComponentAlongPath(
        component=bridge_on_cpw(),
        spacing=200,
        padding=100,
        offset=0,
    )
    r = 100
    p = gf.path.arc(radius=1250, angle=-12.5)
    p += gf.path.straight(length=184.827 - r)
    p += gf.path.arc(radius=r, angle=90)
    # p += gf.path.straight(length=50)
    cpw_width = CPWParams().width
    cpw_gap = CPWParams().gap
    s0 = gf.Section(width=cpw_width, offset=0, layer=LAYER.MAIN_METAL)
    s1 = gf.Section(
        width=cpw_width + 2 * cpw_gap, offset=0, layer=LAYER.GROUND_MASK, port_names=("o1", "o2")
    )
    x = gf.CrossSection(sections=(s0, s1), components_along_path=(via,))
    c = gf.path.extrude(p, cross_section=x)
    return c


def spiral_bridges():
    capacitor_points = np.load(PATH.npy / "arranged_capacitor_points.npy", allow_pickle=False)
    path1, path2 = create_bridge_paths(capacitor_points)
    bridge_width = BridgeParams().width
    s = gf.Section(width=bridge_width, offset=0, layer=LAYER.AIR_BRIDGE)
    x = gf.CrossSection(sections=(s,))
    bridge1 = gf.path.extrude(path1, cross_section=x)
    bridge1.add_port("center", center=(0, 0), orientation=90, width=1, layer=LAYER.GROUND_MASK)
    bridge2 = gf.path.extrude(path2, cross_section=x)
    bridge2.add_port("center", center=(0, 0), orientation=90, width=1, layer=LAYER.GROUND_MASK)
    return bridge1, bridge2


@gf.cell()
def jtwpa_line() -> gf.Component:
    c = gf.Component()
    c_J = c << capacitors_JJs()
    JJ_ground_mask_ref = c << JJ_ground_mask()
    JJ_ground_mask_ref.connect("center", c_J.ports["center"])
    cpw_1 = c << twpa_cpw()
    cpw_1.rotate(132.5)
    cpw_1.move((-1764, -1536.85))
    cpw_2 = c << twpa_cpw()
    cpw_2.rotate(-47.5)
    cpw_2.move((1756.15, 1547.4))
    launcher_1 = c << twpa_launcher(**TwpaLauncherParams().to_kwargs())
    launcher_1.connect("right", cpw_1.ports["o2"], allow_layer_mismatch=True)
    launcher_2 = c << twpa_launcher(**TwpaLauncherParams().to_kwargs())
    launcher_2.connect("right", cpw_2.ports["o2"], allow_layer_mismatch=True)
    pier_radius = BridgeParams().pier_radius
    pier_center_1 = c << gf.components.circle(radius=pier_radius, layer=LAYER.AIR_BRIDGE_CONTACT)
    pier_center_1.move((-14.48, -15.11))
    pier_center_2 = c << gf.components.circle(radius=pier_radius, layer=LAYER.AIR_BRIDGE_CONTACT)
    pier_center_2.move((-13.63, 26.86))
    spiral_bridge_1, spiral_bridge_2 = spiral_bridges()
    c << spiral_bridge_1
    c << spiral_bridge_2
    bridge_region = c.get_region(layer=LAYER.AIR_BRIDGE, merge=True)
    c.remove_layers(layers=[LAYER.AIR_BRIDGE])
    c.add_polygon(bridge_region, layer=LAYER.AIR_BRIDGE)
    c.add_port("center", center=(c.x, c.y), orientation=30, width=1, layer=LAYER.GROUND_MASK)
    c.flatten()
    return c


def _unprocessed_ground(size: float = 5900):
    c = gf.Component()
    c << rectangle(width=size, height=size, layer=LAYER.GROUND_MASK)
    c.add_port("center", center=(0, 0), orientation=180, width=1, layer=LAYER.GROUND_MASK)
    return c


@gf.cell()
def spiral_chip(params: SpiralParams = SpiralParams()) -> gf.Component:
    c = gf.Component()
    jtwpa_line_ref = c << jtwpa_line()
    marker_coordinate = params.marker_coordinate
    marker_size = params.marker_size
    marker_width = params.marker_width
    marker_boundary = params.marker_boundary
    wafer_id = c << text_id(
        id=params.wafer_id,
        text_size=params.text_size,
        margin=params.text_margin,
    )
    wafer_id.move((-marker_coordinate, marker_coordinate))
    chip_id = c << text_id(
        id=params.chip_id,
        text_size=params.text_size,
        margin=params.text_margin,
    )
    chip_id.move((marker_coordinate, -marker_coordinate))
    marker_1 = c << four_marker(size=marker_size, width=marker_width, boundary=marker_boundary)
    marker_1.move((-marker_coordinate, -marker_coordinate))
    marker_2 = c << four_marker(size=marker_size, width=marker_width, boundary=marker_boundary)
    marker_2.move((marker_coordinate, marker_coordinate))
    unprocessed_ground = _unprocessed_ground(size=params.chip_size - DicingParams().width)
    if params.include_dicing:
        c << dicing(**DicingParams().to_kwargs())
    jtwpa_line_ref.connect("center", unprocessed_ground.ports["center"])
    ground = gf.boolean(
        A=unprocessed_ground,
        B=c,
        operation="not",
        layer1=LAYER.GROUND_MASK,
        layer2=LAYER.GROUND_MASK,
        layer=LAYER.MAIN_METAL,
    )
    c.add_ref(ground)
    c.flatten()
    return c
