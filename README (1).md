# 🚗 Vehicle Tracking Dashboard Using OpenCV

A beginner-friendly Python application that tracks a manually selected vehicle or object in a webcam stream or video file using OpenCV's **CSRT** or **KCF** trackers, and displays the results in a live tracking dashboard.

> **Note:** This is my first Computer Vision project, built while learning OpenCV through hands-on practice.

---

## 📖 My Learning Journey

I am learning Computer Vision with OpenCV (`cv2`) one day at a time, and I am documenting that progress through small, practical projects rather than learning only through theory. Reading about concepts is useful, but writing code, running it, breaking it, and fixing it has helped me understand things much better.

**This is my first Computer Vision project.** It is my first step toward understanding how computer vision is used in real-world applications such as object tracking and motion analysis.

This repository is a record of that learning process: the code works, but it is also a learning exercise, so you may find areas that can be improved. I have been honest about those in the [Current Limitations](#-current-limitations) section.

**This project is not the end of my learning. It is the beginning.** I plan to keep building Computer Vision projects, learning new concepts, improving my code, and documenting my progress here on GitHub.

---

## 🔍 Project Overview

The **Vehicle Tracking Dashboard** lets a user select an object (for example, a vehicle) by drawing a bounding box on the first frame of a video or webcam stream. The program then tracks that object frame by frame and shows useful information about its motion:

- Where the object is (center coordinates)
- Which way it is moving (direction)
- How fast it is moving in the image (pixels per second)
- The path it has travelled (trajectory)
- How its X and Y positions change over time (live graphs)

The video feed and the graphs are combined into a single dashboard, which can also be saved as an MP4 video.

---

## ✨ Features

- Select an object manually using a bounding box
- Track the selected object across video frames
- Display the object's center coordinates
- Estimate movement direction: left, right, up, down, and diagonal directions
- Estimate speed in **pixels per second**
- Visualize the object's trajectory
- Display live **X-position** and **Y-position** graphs
- Combine the video feed and graphs into one tracking dashboard
- Save the dashboard as an output MP4 video
- Configure the video source, tracker algorithm, output filename, and trajectory history using command-line arguments

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python** | Main programming language |
| **OpenCV (`cv2`)** | Video input/output, object tracking, drawing, and display |
| **NumPy** | Array and numerical operations |
| **argparse** | Command-line arguments |
| **collections** | Storing recent position history (trajectory) |

---

## 📁 Project Folder Structure

<!-- Update this section so it matches your actual repository. -->

```text
vehicle-tracking-dashboard/
│
├── vehicle_tracking.py     # Main tracking script
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── screenshots/            # Screenshots used in this README
│   └── (add your images here)
│
└── input_video.mp4         # Example input video (optional, add your own)
```

---

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repository-name>.git
cd <your-repository-name>
```

### 2. (Optional) Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install the dependencies

```bash
pip install opencv-contrib-python numpy
```

> **Why `opencv-contrib-python`?**
> The CSRT and KCF trackers are included in the OpenCV *contrib* package. If you only have `opencv-python` installed, these trackers may not be available. In some OpenCV versions, they are located under `cv2.legacy`.

---

## ▶️ How to Run the Project

### Using a webcam

```bash
python vehicle_tracking.py --source 0 --tracker CSRT
```

### Using a video file

```bash
python vehicle_tracking.py --source "input_video.mp4" --tracker KCF
```

### Command-line arguments

<!-- Make sure these flag names match the ones in your script. -->

| Argument | Description | Example |
|----------|-------------|---------|
| `--source` | Webcam index (e.g. `0`) or path to a video file | `--source 0` |
| `--tracker` | Tracking algorithm: `CSRT` or `KCF` | `--tracker CSRT` |
| `--output` | Name of the saved dashboard video | `--output dashboard.mp4` |
| `--history` | Number of past positions kept for the trajectory | `--history 64` |

### Basic usage

1. Run one of the commands above.
2. The first frame appears. **Draw a box** around the vehicle or object you want to track.
3. Confirm the selection (in OpenCV's selector this is usually **Enter** or **Space**).
4. The dashboard opens and tracking begins.
5. Press the quit key defined in the script (commonly **Q** or **Esc**) to stop. The output video is saved.

---

## 🧠 How the Tracking System Works

1. **Open the video source.** The script reads frames from a webcam or a video file using `cv2.VideoCapture`.
2. **Select the object.** The user draws a bounding box on the first frame. This is the starting point for the tracker.
3. **Initialize the tracker.** The chosen tracker (CSRT or KCF) learns what the selected object looks like.
4. **Update on every frame.** For each new frame, the tracker estimates the object's new bounding box.
5. **Compute the center point.** The center of the box is calculated from its position and size:
   ```text
   center_x = x + width / 2
   center_y = y + height / 2
   ```
6. **Estimate direction.** The center in the current frame is compared with the previous one. The change in position (`dx`, `dy`) is used to decide whether the object is moving left, right, up, down, or diagonally.
   > In image coordinates, the **Y-axis points downward**, so a decreasing Y value means the object is moving *up* on the screen.
7. **Estimate speed.** The distance moved between frames is divided by the time between them (see the next section).
8. **Store the trajectory.** Recent center points are kept in a fixed-length history (using `collections`) and drawn as a path on the video.
9. **Build the dashboard.** The video frame and the live X/Y graphs are combined into one image.
10. **Save the output.** Each dashboard frame is written to an MP4 file using `cv2.VideoWriter`.

### CSRT vs. KCF

| Tracker | General characteristics |
|---------|-------------------------|
| **CSRT** | Generally more accurate, but slower |
| **KCF** | Generally faster, but may be less accurate |

These are general descriptions of the algorithms. I have not run formal benchmarks, so I do not claim specific performance numbers.

---

## 📐 Speed Estimation Formula and Its Limitations

### Formula

The speed is estimated from how far the object's center moves between frames:

```text
distance (pixels) = sqrt( (x₂ − x₁)² + (y₂ − y₁)² )

speed (pixels/second) = distance / time_between_frames
```

If the video's frame rate (FPS) is known, the time between frames is approximately `1 / FPS`.

### ⚠️ Important: this is NOT km/h

The speed shown by this project is in **pixels per second**, **not real-world units** such as km/h or m/s. Camera calibration has **not** been implemented, so the program has no way of knowing how many pixels correspond to a real distance.

### Limitations of the speed estimate

- **No real-world scale.** One pixel does not represent a fixed distance in meters.
- **Perspective effects.** Objects closer to the camera appear to move more pixels than distant objects moving at the same real speed.
- **Camera movement.** If the camera moves, the pixel movement includes the camera's motion.
- **Frame-rate dependence.** Dropped frames or an inaccurate FPS value affect the time calculation.
- **Tracking noise.** Small jitter in the bounding box can cause fluctuations in the estimated speed.

To convert to real-world speed, future versions would need camera calibration or a known reference distance in the scene.

---

## 🖼️ Screenshots

> Replace the placeholders below with your own screenshots from running the project.

### Object selection
![Object selection](screenshots/object_selection.png)

### Tracking dashboard
![Tracking dashboard](screenshots/dashboard.png)

### Trajectory visualization
![Trajectory visualization](screenshots/trajectory.png)

### X and Y position graphs
![Position graphs](screenshots/position_graphs.png)

---

## 💡 Challenges and What I Learned

<!-- Edit this section so it reflects your real experience. The points below are suggestions based on the project's topics. -->

Building this project helped me practice and understand:

- How to read frames from a webcam and from a video file using OpenCV
- How object tracking differs from object detection (the tracker follows an object I select; it does not find objects on its own)
- How image coordinates work, including why the Y-axis points downward
- How to turn changes in position into direction and speed estimates
- How to use `argparse` to make a script configurable from the command line
- How to use a fixed-length history to draw a trajectory
- How to combine multiple visual elements into one dashboard frame
- How to save processed frames as a video file

Some of the challenges I worked through:

- Understanding the order of operations: read frame → update tracker → compute values → draw → display → save
- Making sure the dashboard layout and the output video size matched correctly
- Interpreting the speed value correctly, and being clear that it is in pixels per second, not km/h

---

## ⚠️ Current Limitations

- The object must be **selected manually**; there is no automatic vehicle detection.
- Only **one object** is tracked at a time.
- The tracker can **lose the object** if it is occluded, changes size quickly, moves very fast, or leaves the frame. There is no automatic recovery.
- Speed is in **pixels per second**, with no real-world calibration.
- Direction and speed estimates may be **noisy** because they depend on small frame-to-frame changes in the bounding box.
- Results depend on video quality, lighting, and the chosen tracker.
- The project has not been formally tested or benchmarked.

---

## 🚀 Future Improvements

- Add camera calibration to estimate real-world speed (e.g., km/h)
- Smooth speed and direction values to reduce noise
- Detect vehicles automatically instead of selecting them manually
- Track multiple objects at the same time
- Add a way to re-select the object when tracking is lost
- Export tracking data (positions, speed, direction) to a CSV file
- Add a simple user interface for choosing the video source and tracker
- Compare more tracking algorithms
- Write cleaner, more modular code with functions and tests

---

## 👤 Author

**Name:** `<Your Name>`
**GitHub:** [`<your-username>`](https://github.com/<your-username>)

I am learning Computer Vision step by step and sharing my progress through hands-on projects. Feedback, suggestions, and advice from more experienced developers are always welcome. Feel free to open an issue or reach out.

⭐ If you find this project useful or interesting, consider giving it a star. Thank you for visiting!
