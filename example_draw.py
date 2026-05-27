"""
Example usage of SensorDrawer: draw normalized sensor data (0, 0, 0.4) for all 9 readings
on both left and right sides, using all modes and both cameras.
Modes that support is_spatial=False (points1_contact, points9_color, bin_bar) are drawn both ways.
"""
import numpy as np
import cv2
from draw_sensors import SensorDrawer

# Example robot state (7 joint angles in degrees, gripper position 0-850)
angles = [4.223157, -20.635018, 3.554114, 53.757822, 2.931596, 74.793452, 2.056632]
grip_pos = 840

# Normalized sensor data: 9 readings of (0, 0, 0.4) for both left and right
sensor_data = np.full((9, 3), [0.0, 0.0, 0.4])

# Colors: left=red, right=blue, alpha=0.3 (77/255)
left_color = (255, 0, 0, 77)
right_color = (0, 0, 255, 77)

# (mode, is_spatial, arrow_length_scale)
draw_configs = [
    ("points9_arrow",   True,  0.06),    # 0.5x of default 0.12
    ("points1_arrow",   True,  0.006),   # 0.1x of default 0.12
    ("points1_contact", True,  0.12),
    ("points9_color",   True,  0.12),
    ("points1_contact", False, 0.12),
    ("points9_color",   False, 0.12),
    ("bin_bar",         False, 0.12),
]

results = []

# --- Side camera (327122079374.jpg) ---
side_drawer = SensorDrawer(camera_select='side')
side_img = cv2.imread("327122079374.jpg")
assert side_img is not None, "Could not load 327122079374.jpg"

for mode, is_spatial, arrow_scale in draw_configs:
    color_kwargs = {} if mode == "points9_color" else dict(left_color=left_color, right_color=right_color)
    img = side_drawer.draw_on_image(
        side_img, angles, grip_pos,
        normalized_left_sensor=sensor_data,
        normalized_right_sensor=sensor_data,
        mode=mode,
        is_spatial=is_spatial,
        arrow_length_scale=arrow_scale,
        **color_kwargs,
    )
    spatial_tag = "spatial" if is_spatial else "flat"
    label = f"side_{mode}_{spatial_tag}"
    cv2.putText(img, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    results.append(img)

# --- Wrist camera (332322072612.jpg) ---
wrist_drawer = SensorDrawer(camera_select='wrist')
wrist_img = cv2.imread("332322072612.jpg")
assert wrist_img is not None, "Could not load 332322072612.jpg"

for mode, is_spatial, arrow_scale in draw_configs:
    color_kwargs = {} if mode == "points9_color" else dict(left_color=left_color, right_color=right_color)
    img = wrist_drawer.draw_on_image(
        wrist_img, angles, grip_pos,
        normalized_left_sensor=sensor_data,
        normalized_right_sensor=sensor_data,
        mode=mode,
        is_spatial=is_spatial,
        arrow_length_scale=arrow_scale,
        **color_kwargs,
    )
    spatial_tag = "spatial" if is_spatial else "flat"
    label = f"wrist_{mode}_{spatial_tag}"
    cv2.putText(img, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    results.append(img)

# --- Tile all 14 results into a single image (2 rows x 7 cols) ---
n_configs = len(draw_configs)
target_h, target_w = 480, 640
resized = [cv2.resize(img, (target_w, target_h)) for img in results]

row_top = np.hstack(resized[:n_configs])      # side camera configs
row_bottom = np.hstack(resized[n_configs:])   # wrist camera configs
tiled = np.vstack([row_top, row_bottom])

cv2.imwrite("example_all_modes.jpg", tiled)
print(f"Saved example_all_modes.jpg ({tiled.shape[1]}x{tiled.shape[0]})")

# --- third_image mode: raw sensor frame, black background, no camera/robot transforms ---
# Middle sensor (idx 4) = (0.4, 0.4, 1) → red; all others = (0.4, 0.4, 0) → green
sensor_third = np.full((9, 3), [0.4, 0.4, 0.0])
sensor_third[4] = [0.4, 0.4, 1.0]

dummy_img = np.zeros((480, 640, 3), dtype=np.uint8)
img_third = side_drawer.draw_on_image(
    dummy_img, angles, grip_pos,
    normalized_left_sensor=sensor_third,
    normalized_right_sensor=sensor_third,
    mode="third_image",
)
cv2.putText(img_third, "third_image", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
cv2.imwrite("example_third_image.jpg", img_third)
print(f"Saved example_third_image.jpg ({img_third.shape[1]}x{img_third.shape[0]})")
