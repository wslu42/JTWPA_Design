import numpy as np
from gdsfactory import Path


def generate_bridge_points(capacitor_points: list):
    bridge_1_centers = []
    bridge_2_centers = []

    bridge_1_centers.append([1766.924, 1566.626])
    bridge_2_centers.append([1734.919, 1537.908])

    for i in range(len(capacitor_points)):
        if 1 <= i <= 1122:
            theta = np.arctan2(capacitor_points[i][0], capacitor_points[i][1])
            cx = 10 * np.cos(theta) + 21.5 * np.sin(theta) + capacitor_points[i][0]
            cy = -10 * np.sin(theta) + 21.5 * np.cos(theta) + capacitor_points[i][1]
            bridge_1_centers.append([cx, cy])
            cx = 10 * np.cos(theta) - 21.5 * np.sin(theta) + capacitor_points[i][0]
            cy = -10 * np.sin(theta) - 21.5 * np.cos(theta) + capacitor_points[i][1]
            bridge_2_centers.append([cx, cy])
        elif 1123 <= i <= 1200:
            theta = np.arctan2(capacitor_points[i][0], capacitor_points[i][1] - 500)
            cx = 10 * np.cos(theta) + 21.5 * np.sin(theta) + capacitor_points[i][0]
            cy = -10 * np.sin(theta) + 21.5 * np.cos(theta) + capacitor_points[i][1]
            bridge_1_centers.append([cx, cy])
            # if i == 1210:
            # print(cx, cy)
            cx = 10 * np.cos(theta) - 21.5 * np.sin(theta) + capacitor_points[i][0]
            cy = -10 * np.sin(theta) - 21.5 * np.cos(theta) + capacitor_points[i][1]
            bridge_2_centers.append([cx, cy])
            # if i == 1210:
            # print(cx, cy)
        elif 1201 <= i <= 1279:
            theta = np.arctan2(capacitor_points[i][0], capacitor_points[i][1] + 500)
            cx = 10 * np.cos(theta) - 21.5 * np.sin(theta) + capacitor_points[i][0]
            cy = -10 * np.sin(theta) - 21.5 * np.cos(theta) + capacitor_points[i][1]
            bridge_1_centers.append([cx, cy])
            # if i == 1211:
            # print(cx, cy)
            cx = 10 * np.cos(theta) + 21.5 * np.sin(theta) + capacitor_points[i][0]
            cy = -10 * np.sin(theta) + 21.5 * np.cos(theta) + capacitor_points[i][1]
            bridge_2_centers.append([cx, cy])
            # if i == 1211:
            # print(cx, cy)
        elif 1280 <= i <= 2401:
            theta = np.arctan2(capacitor_points[i][0], capacitor_points[i][1])
            cx = 10 * np.cos(theta) - 21.5 * np.sin(theta) + capacitor_points[i][0]
            cy = -10 * np.sin(theta) - 21.5 * np.cos(theta) + capacitor_points[i][1]
            bridge_1_centers.append([cx, cy])
            cx = 10 * np.cos(theta) + 21.5 * np.sin(theta) + capacitor_points[i][0]
            cy = -10 * np.sin(theta) + 21.5 * np.cos(theta) + capacitor_points[i][1]
            bridge_2_centers.append([cx, cy])

    bridge_1_centers.append([-1742.793, -1527.252])
    bridge_2_centers.append([-1774.96, -1555.788])

    return bridge_1_centers, bridge_2_centers


def create_bridge_paths(capacitor_points: list):
    bridge_1_centers, bridge_2_centers = generate_bridge_points(capacitor_points)

    path1 = Path(np.array(bridge_1_centers))
    path2 = Path(np.array(bridge_2_centers))

    return path1, path2
