import argparse
import collections
import numpy as np
import cv2

parser = argparse.ArgumentParser(description="Vehicle/Object Tracking with Speed and Direction")

parser.add_argument("--source", default="0", help="Webcam index or video file path")
parser.add_argument("--tracker", default="CSRT", choices=["CSRT", "KCF"], help="Tracking algorithm")
parser.add_argument("--output", default="vehicle_tracking_output.mp4", help="Output video file")
parser.add_argument("--max-points", type=int, default=60, help="Number of previous positions to store")
args = parser.parse_args()

if args.tracker == "CSRT":
    tracker = cv2.TrackerCSRT_create()
elif args.tracker == "KCF":
    tracker = cv2.TrackerKCF_create()
if args.source.isdigit():
    source = int(args.source)
else:
    source = args.source
cap = cv2.VideoCapture(source)
if not cap.isOpened():
    raise IOError(f"Cannot open source: {source}")
fps = cap.get(cv2.CAP_PROP_FPS)
if fps <= 0 or fps != fps:
    fps = 30.0
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
graph_width = 320
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(args.output, fourcc, fps, (width + graph_width, height))
if not out.isOpened():
    raise IOError("Could not create output video")
ok, first_frame = cap.read()
if not ok:
    raise IOError("Could not read first frame")
bbox = cv2.selectROI("Select Vehicle", first_frame, fromCenter=False, showCrosshair=True)
cv2.destroyWindow("Select Vehicle")
if bbox == (0, 0, 0, 0):
    cap.release()
    out.release()
    raise SystemExit("No vehicle selected")
tracker.init(first_frame, bbox)
previous_center = None
trajectory = collections.deque(maxlen=args.max_points)
x_history = collections.deque(maxlen=args.max_points)
y_history = collections.deque(maxlen=args.max_points)

while True:
    ok, frame = cap.read()
    if not ok:
        break
    tracking_ok, bbox = tracker.update(frame)
    if tracking_ok:
        bbox = tuple(int(value) for value in bbox)
        x, y, w, h = bbox
        center_x = int(x + w / 2)
        center_y = int(y + h / 2)
        speed = 0.0
        direction = "static"
        if previous_center is not None:
            dx = center_x - previous_center[0]
            dy = center_y - previous_center[1]
            distance = np.hypot(dx, dy)
            speed = distance * fps
            horizontal = ""
            vertical = ""
            if abs(dx) > 3:
                if dx > 0:
                    horizontal = "right"
                else:
                    horizontal = "left"
            if abs(dy) > 3:
                if dy > 0:
                    vertical = "down"
                else:
                    vertical = "up"
            if horizontal and vertical:
                direction = vertical + "-" + horizontal
            elif horizontal:
                direction = horizontal
            elif vertical:
                direction = vertical
            else:
                direction = "static"
        previous_center = (center_x, center_y)
        trajectory.append((center_x, center_y))
        x_history.append(center_x)
        y_history.append(center_y)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
        cv2.putText(frame, f"Center: ({center_x}, {center_y})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        cv2.putText(frame, f"Direction: {direction}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.putText(frame, f"Speed: {speed:.1f} px/s", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)
        cv2.putText(frame, f"Tracker: {args.tracker}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    else:
        cv2.putText(frame, "Tracking Lost!", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    for i in range(1, len(trajectory)):
        cv2.line(frame, trajectory[i - 1], trajectory[i], (255, 0, 255), 2)
        
        
    graph_height = height // 2
    x_graph = np.zeros((graph_height, graph_width, 3), dtype=np.uint8)
    cv2.putText(x_graph, "X Position", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.rectangle(x_graph, (10, 40), (graph_width - 10, graph_height - 20), (80, 80, 80), 1)
    if len(x_history)>=2:
        x_points = []
        for i, value in enumerate(x_history):
            px = 10 + int(i * (graph_width - 20) / (len(x_history) - 1))
            py = graph_height - 20 - int(value / max(width, 1) * (graph_height - 65))
            x_points.append((px, py))
        cv2.polylines(x_graph, [np.array(x_points, np.int32)], False, (0, 255, 0), 2)

    y_graph = np.zeros((graph_height, graph_width, 3), dtype=np.uint8)
    cv2.putText(y_graph, "Y Position", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.rectangle(y_graph, (10, 40), (graph_width - 10, graph_height - 20), (80, 80, 80), 1)
    if len(y_history) >= 2:
        y_points = []
        for i, value in enumerate(y_history):
            px = 10 + int(i * (graph_width - 20) / (len(y_history) - 1))
            py = graph_height - 20 - int(value / max(height, 1) * (graph_height - 65))
            y_points.append((px, py))
        cv2.polylines(y_graph, [np.array(y_points, np.int32)], False, (0, 255, 0), 2)


        
    graph_panel = np.vstack([x_graph, y_graph])
    dashboard = np.hstack([frame, graph_panel])
    out.write(dashboard)
    cv2.imshow("Vehicle Tracking Dashboard", dashboard)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
cap.release()
out.release()
cv2.destroyAllWindows()
