import math

import gdsfactory as gf
import numpy as np
from gdsfactory.cross_section import ComponentAlongPath

from jtwpa_design.cells.components.rectangle import rectangle
from jtwpa_design.cells.paths.jtwpa_path import jtwpa_path
from jtwpa_design.config import PATH
from jtwpa_design.pdk import get_pdk
from jtwpa_design.tech import LAYER

get_pdk().activate()

cap_arc1 = []
cap_arc2 = []
cap_arch_spiral = []
JJ_arc1 = []
JJ_arc2 = []
JJ_arch_spiral = []

p = jtwpa_path()


def _unit_cell_anchor() -> gf.Component:
    c = gf.Component()
    c << rectangle(width=1, height=1, layer=LAYER.MAIN_METAL)
    JJ_anchor = c << rectangle(width=1, height=1, layer=LAYER.JJ)
    JJ_anchor.movex(10)
    return c


via = ComponentAlongPath(
    component=_unit_cell_anchor(),
    spacing=20,
    padding=0,
    offset=0,
)

s = gf.Section(width=0.5, offset=0, layer=LAYER.GROUND_MASK, port_names=("o1", "o2"))
x = gf.CrossSection(sections=(s,), components_along_path=(via,))

c = gf.path.extrude(p, cross_section=x)

cap_centers = []
cap_region = c.get_region(layer=LAYER.MAIN_METAL)
JJ_centers = []
JJ_region = c.get_region(layer=LAYER.JJ)

for poly in cap_region:
    xs = []
    ys = []

    for p in poly.each_point_hull():
        xs.append(p.x)
        ys.append(p.y)

    cx = sum(xs) / (len(xs) * 1000)
    cy = sum(ys) / (len(ys) * 1000)
    cap_centers.append([cx, cy])

for cx, cy in cap_centers:
    r = math.sqrt(cx**2 + cy**2)
    if -510 <= cx <= 0 and 0 <= cy <= 1010:
        cap_arc1.append([cx, cy, r])
    elif 0 <= cx <= 510 and -1000 <= cy <= 10:
        cap_arc2.append([cx, cy, r])
    else:
        cap_arch_spiral.append([cx, cy, r])

for poly in JJ_region:
    xs = []
    ys = []

    for p in poly.each_point_hull():
        xs.append(p.x)
        ys.append(p.y)

    cx = sum(xs) / (len(xs) * 1000)
    cy = sum(ys) / (len(ys) * 1000)
    if -1771.1 <= cx <= -1769.7 and -1531.1 <= cy <= -1529.7:
        # print(cx, cy)
        continue
    JJ_centers.append([cx, cy])

for cx, cy in JJ_centers:
    if -510 <= cx <= 0 and 0 <= cy <= 1010:
        JJ_arc1.append([cx, cy])
    elif 0 <= cx <= 510 and -1000 <= cy <= 10:
        JJ_arc2.append([cx, cy])
    else:
        JJ_arch_spiral.append([cx, cy])

arranged_points = []

sorted_arch_spiral = sorted(cap_arch_spiral, key=lambda x: x[2], reverse=True)
sorted_arc1 = sorted(cap_arc1, key=lambda x: x[2], reverse=True)
sorted_arc2 = sorted(cap_arc2, key=lambda x: x[2], reverse=False)

spiral1 = []
spiral2 = []
for cx, cy, r in sorted_arch_spiral:
    if cx <= 0 and cy >= 0 and r >= 2400:
        spiral1.append([cx, cy, np.degrees(np.arctan2(cx, cy))])
    elif cx <= 0 and cy <= 0 and r >= 2220:
        spiral1.append([cx, cy, np.degrees(np.arctan2(cx, cy))])
    elif cx >= 0 and cy <= 0 and 2260 >= r >= 2050:
        spiral1.append([cx, cy, np.degrees(np.arctan2(cx, cy))])
    elif cx >= 0 and cy >= 0 and 2100 >= r >= 1930:
        spiral1.append([cx, cy, np.degrees(np.arctan2(cx, cy))])
    elif cx <= 0 and cy >= 0 and 1970 >= r >= 1775:
        spiral1.append([cx, cy, np.degrees(np.arctan2(cx, cy))])
    elif cx <= 0 and cy <= 0 and 1820 >= r >= 1610:
        spiral1.append([cx, cy, np.degrees(np.arctan2(cx, cy))])
    elif cx >= 0 and cy <= 0 and 1635 >= r >= 1445:
        spiral1.append([cx, cy, np.degrees(np.arctan2(cx, cy))])
    elif cx >= 0 and cy >= 0 and 1480 >= r >= 1315:
        spiral1.append([cx, cy, np.degrees(np.arctan2(cx, cy))])
    elif cx <= 0 and cy >= 0 and 1345 >= r >= 1150:
        spiral1.append([cx, cy, np.degrees(np.arctan2(cx, cy))])
    elif cx <= 0 and cy <= 0 and 1190 >= r >= 980:
        spiral1.append([cx, cy, np.degrees(np.arctan2(cx, cy))])
    else:
        spiral2.append([cx, cy, np.degrees(np.arctan2(cx, cy))])

for item in spiral2:
    arranged_points.append(item)
for item in sorted_arc1:
    arranged_points.append([item[0], item[1], np.degrees(np.arctan2(item[0], item[1]))])
for item in sorted_arc2:
    arranged_points.append([item[0], item[1], np.degrees(np.arctan2(item[0], item[1]))])
for item in spiral1[::-1]:
    arranged_points.append(item)

np.save(PATH.npy / "arranged_capacitor_points.npy", arranged_points)
np.save(PATH.npy / "JJ_arch_spiral.npy", JJ_arch_spiral)
np.save(PATH.npy / "JJ_arc1.npy", JJ_arc1)
np.save(PATH.npy / "JJ_arc2.npy", JJ_arc2)
