# Hand Boundary Detection POC

**Prototype**: Real-time hand/fingertip tracking + virtual object boundary (CPU-only, OpenCV)

## Overview
- Detects hand via HSV skin segmentation + contours + convex hull (no MediaPipe/OpenPose).
- Draws a virtual rectangular object on the live webcam feed.
- Computes distance from fingertip to object and classifies states: SAFE / WARNING / DANGER.
- Displays **DANGER DANGER** when in danger state.
- Target: ≥ 8 FPS on CPU (tested on 640×480).

## Files
- `hand_boundary_poc.py` — main demo script (OpenCV + NumPy)
- `requirements.txt` — Python dependencies

## Visual Examples

### 🟢 SAFE Zone
This image shows when the hand is far from the boundary — fully safe.

![Safe](https://raw.githubusercontent.com/Vishwaa6/hand-tracking-danger-system/main/Safe.png)

### 🔴 DANGER Zone
Here, the hand moves too close to the virtual object. The system switches to **DANGER**, triggering the on-screen alert.

![Danger](https://raw.githubusercontent.com/Vishwaa6/hand-tracking-danger-system/main/Danger.png)

### ⚙️ CONTROL Reference
This screenshot shows the adjustable HSV and proximity controls used during calibration to fine-tune the detection under different lighting conditions.

![Control](https://raw.githubusercontent.com/Vishwaa6/hand-tracking-danger-system/main/Control.png)


## Requirements
```bash
python 3.8+
pip install -r requirements.txt




