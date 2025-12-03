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
- `demo/demo_video.mp4` — short demo showing SAFE → WARNING → DANGER (optional)

## Requirements
```bash
python 3.8+
pip install -r requirements.txt

# Hand Tracking Danger System

Short project description...

## Visual examples

Below are the three images (Safe, Danger, Control) embedded via raw GitHub URLs. These assume the files are at the repository root on branch main and are PNGs. If they're in a folder or have other extensions, update the filenames or paths accordingly.

![Safe](https://raw.githubusercontent.com/Vishwaa6/hand-tracking-danger-system/main/Safe.png)

![Danger](https://raw.githubusercontent.com/Vishwaa6/hand-tracking-danger-system/main/Danger.png)

![Control](https://raw.githubusercontent.com/Vishwaa6/hand-tracking-danger-system/main/Control.png)

If you need them smaller or side-by-side, replace the markdown above with this HTML block (same raw URLs):

<div>
  <img src="https://raw.githubusercontent.com/Vishwaa6/hand-tracking-danger-system/main/Safe.png" alt="Safe" width="300" style="display:inline-block; margin-right:8px;" />
  <img src="https://raw.githubusercontent.com/Vishwaa6/hand-tracking-danger-system/main/Danger.png" alt="Danger" width="300" style="display:inline-block; margin-right:8px;" />
  <img src="https://raw.githubusercontent.com/Vishwaa6/hand-tracking-danger-system/main/Control.png" alt="Control" width="300" style="display:inline-block;" />
</div>

Notes:
- If your images are .jpg/.jpeg/.gif, change the extension (.png) to the correct one.
- If the images are in a folder (for example assets/), use:
  https://raw.githubusercontent.com/Vishwaa6/hand-tracking-danger-system/main/assets/Safe.png
- If you uploaded images using the GitHub web editor (drag‑and‑drop), GitHub may host them under user-images.githubusercontent.com — open the image on GitHub, copy the image address, and paste that full URL into the README instead of the raw.githubusercontent URL.
