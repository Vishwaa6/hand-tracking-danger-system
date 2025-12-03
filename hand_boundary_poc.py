import cv2
import numpy as np
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--camera", type=int, default=0)
parser.add_argument("--width", type=int, default=640)
parser.add_argument("--height", type=int, default=480)
parser.add_argument("--min_area", type=int, default=3000, help="min contour area to be considered hand")
args = parser.parse_args()

# ------------------ TRACKBAR UI ------------------
def nothing(x): pass

cv2.namedWindow("controls", cv2.WINDOW_NORMAL)
cv2.resizeWindow("controls", 450, 300)

# More realistic skin defaults
cv2.createTrackbar("H_min", "controls", 0, 179, nothing)
cv2.createTrackbar("H_max", "controls", 25, 179, nothing)
cv2.createTrackbar("S_min", "controls", 40, 255, nothing)
cv2.createTrackbar("S_max", "controls", 200, 255, nothing)
cv2.createTrackbar("V_min", "controls", 40, 255, nothing)
cv2.createTrackbar("V_max", "controls", 255, 255, nothing)

cv2.createTrackbar("warning_px", "controls", 120, 500, nothing)
cv2.createTrackbar("danger_px", "controls", 40, 500, nothing)
cv2.createTrackbar("blur", "controls", 7, 25, nothing)

# ------------------ CAMERA INIT ------------------
cap = cv2.VideoCapture(args.camera)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

obj_w_frac, obj_h_frac = 0.35, 0.20
font = cv2.FONT_HERSHEY_SIMPLEX

prev_time = time.time()
fps = 0

def compute_point_to_rect_distance(pt, rect):
    x, y = pt
    x1, y1, x2, y2 = rect
    if x1 <= x <= x2 and y1 <= y <= y2:
        return 0
    dx = max(x1 - x, 0, x - x2)
    dy = max(y1 - y, 0, y - y2)
    return (dx * dx + dy * dy) ** 0.5

def draw_state(frame, state):
    color = {"SAFE": (50,200,50), "WARNING": (0,180,255), "DANGER": (0,0,255)}[state]
    cv2.putText(frame, f"State: {state}", (10,30), font, 1.0, color, 2)
    if state == "DANGER":
        cv2.putText(frame, "DANGER DANGER", (30, frame.shape[0]//2),
                    font, 2.0, (0,0,255), 6)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (args.width, args.height))
    h, w = frame.shape[:2]

    # Trackbars
    H_min = cv2.getTrackbarPos("H_min", "controls")
    H_max = cv2.getTrackbarPos("H_max", "controls")
    S_min = cv2.getTrackbarPos("S_min", "controls")
    S_max = cv2.getTrackbarPos("S_max", "controls")
    V_min = cv2.getTrackbarPos("V_min", "controls")
    V_max = cv2.getTrackbarPos("V_max", "controls")
    warning_px = cv2.getTrackbarPos("warning_px", "controls")
    danger_px = cv2.getTrackbarPos("danger_px", "controls")
    blur_k = cv2.getTrackbarPos("blur", "controls")
    if blur_k % 2 == 0:
        blur_k += 1

    # Virtual rectangle
    obj_w = int(w * obj_w_frac)
    obj_h = int(h * obj_h_frac)
    obj_x1 = (w - obj_w) // 2
    obj_y1 = (h - obj_h) // 2
    obj_x2 = obj_x1 + obj_w
    obj_y2 = obj_y1 + obj_h
    rect = (obj_x1, obj_y1, obj_x2, obj_y2)

    # Preprocess
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([H_min, S_min, V_min]),
                            np.array([H_max, S_max, V_max]))

    # Kill random noise and background junk
    mask = cv2.medianBlur(mask, 7)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,9))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    fingertip = None
    min_dist = float('inf')
    hand = None

    # ---------------- FIX 1: Ignore small OR huge blobs ----------------
    filtered = []
    for c in contours:
        a = cv2.contourArea(c)
        if 3000 < a < 50000:     # kills table + wall blobs
            filtered.append(c)

    # ---------------- FIX 2: Choose highest contour (hand is highest) ----------------
    if filtered:
        filtered = sorted(filtered, key=lambda c: cv2.boundingRect(c)[1])
        hand = filtered[0]

    if hand is not None:
        cv2.drawContours(frame, [hand], -1, (80,255,80), 2)
        hull = cv2.convexHull(hand)
        hull_pts = hull.reshape(-1,2)
        cv2.polylines(frame, [hull_pts], True, (255,255,0), 2)

        # Find hull point closest to virtual object
        for (x,y) in hull_pts:
            d = compute_point_to_rect_distance((x,y), rect)
            if d < min_dist:
                min_dist = d
                fingertip = (x,y)

        if fingertip:
            cv2.circle(frame, fingertip, 8, (0,255,255), -1)

    # State logic
    state = "SAFE"
    if fingertip:
        if min_dist <= danger_px:
            state = "DANGER"
        elif min_dist <= warning_px:
            state = "WARNING"

    # Draw virtual boundary
    color = {"SAFE":(0,255,0), "WARNING":(0,180,255), "DANGER":(0,0,255)}[state]
    cv2.rectangle(frame, (obj_x1,obj_y1), (obj_x2,obj_y2), color, 3)
    cv2.putText(frame, "Virtual object", (obj_x1+5,obj_y1-10), font, 0.6, color, 2)

    draw_state(frame, state)

    # FPS
    now = time.time()
    fps = 0.9*fps + 0.1*(1/(now-prev_time+1e-6))
    prev_time = now
    cv2.putText(frame, f"FPS: {fps:.1f}", (w-120,30), font, 0.7, (200,200,200), 2)

    combined = np.hstack(
        (frame, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR))
    )
    cv2.imshow("hand_vs_object", combined)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
