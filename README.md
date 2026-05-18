# Sensor Drawing

This repository contains scripts and utilities for visualizing sensor data and kinematics. 

## Features
- Kinematics calculation (`xram_kinematics.py`)
- Drawing and visualization (`draw_sensors.py`, `example_draw.py`)
- Normalization and transformations (`normalizer.py`, `transforms/`)

## Example

![Example](example_all_modes.jpg)

## Draw Modes & Arguments

The `draw_on_image` method of `SensorDrawer` allows flexible rendering of sensor data on the image. It supports the following modes (passed via the `mode` parameter):
- `"points9_arrow"`: Draws 9 dots and 9 force arrows per side (requires `is_spatial=True`).
- `"points1_arrow"`: Draws 1 center dot and 1 averaged force arrow per side (requires `is_spatial=True`).
- `"points1_contact"`: Draws 1 center dot per side only when any sensor magnitude exceeds a threshold (`>= 0.05`). Supports spatial mapping and 2D overlay.
- `"points9_color"`: Draws 9 dots per side with no arrows. The dots are colored based on sensor XYZ readings mapped linearly to RGB. Supports spatial mapping and 2D overlay.

### Main Arguments
- `image`: The BGR/RGB numpy array (current version 640x480 only since camera K matrix is hardcoded with 640*480 resolution) to draw on.
- `angles`: List of 7 joint angles from xArm (degrees).
- `grip_pos`: Gripper position value.
- `dot_size`: Diameter for sensor dots.
- `is_spatial`: If `True`, points will be spatially mapped based on kinematics onto image space. If `False`, uses a simple 2D display at the corners of the image.
- `left_color` / `right_color`: RGBA colors for left and right sensor representations.
- `scale`: Multiplier for sensor local points positioning.
- `color_scale`: Multiplier applied to sensor xyz values before mapping to colors (used in `points9_color`).
- `arrow_length_scale` and `arrow_thickness`: Modifiers for 3D arrow visualizations based on sensor forces.

## Installation

Install the required Python packages using:

```bash
pip install -r requirements.txt
```

## Usage

Run the example drawing script to see the outputs:

```bash
python example_draw.py
```
