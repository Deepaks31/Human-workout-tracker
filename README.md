# 💪 Human Workout Tracker

A real-time workout tracking app that uses your webcam to detect and count **bicep curls** (or other arm exercises) using computer vision and pose estimation. Built with **Python**, **OpenCV**, **Mediapipe**, and **Streamlit**.

---

## 🚀 Features

- Live webcam feed integrated with pose detection
- Real-time elbow angle calculation
- Repetition counter for both left and right arms
- Displays:
  - Total repetitions
  - Elbow angle
  - Arm stage (`up` / `down`)
- Interactive buttons to start and stop tracking in Streamlit

---

## 📂 Project Structure

├── app.py # Streamlit-based main application
├── bicep_workout_tracker.py.ipynb # Development / research notebook (optional)
├── README.md # Project documentation


---

## 🛠️ Technologies Used

- **Python**
- **OpenCV** – For capturing and displaying webcam feed
- **Mediapipe** – For real-time human pose landmark detection
- **NumPy** – For calculating angles between joints
- **Streamlit** – For building the interactive web UI

---

## 📸 How It Works

1. Streamlit launches a web interface to control webcam tracking.
2. Mediapipe detects key human body landmarks (shoulder, elbow, wrist).
3. OpenCV captures frames from webcam and overlays tracking data.
4. Angles are calculated to determine arm movement direction.
5. Reps are counted when full up-down motion is detected.

---

## ▶️ Getting Started

git clone https://github.com/your-username/human-workout-tracker.git

cd human-workout-tracker

pip install streamlit opencv-python mediapipe numpy

streamlit run app.py
