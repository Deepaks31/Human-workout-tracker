import cv2
import numpy as np
import streamlit as st
import mediapipe as mp

# Function to calculate angle
def calculate_angle(a, b, c):
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# Streamlit app
def main():
    st.title("Exercise Reps Counter")

    # Create a placeholder for the webcam feed
    placeholder = st.empty()

    # Create separate buttons for start and stop
    start_button = st.button("Start Capture")
    stop_button = st.button("Stop Capture")

    # OpenCV video capture
    cap = cv2.VideoCapture(0)

    counter = 0
    stage_left = None
    stage_right = None
    repetition_detected = False

    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    # Check if the start button is pressed
    if start_button:
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while stop_button is False:
                ret, frame = cap.read()

                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                results = pose.process(image)

                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                try:
                    landmarks = results.pose_landmarks.landmark

                    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                    angle_left = calculate_angle(left_shoulder, left_elbow, left_wrist)
                    angle_right = calculate_angle(right_shoulder, right_elbow, right_wrist)

                    st.write(f"Left Angle: {angle_left}")
                    st.write(f"Right Angle: {angle_right}")

                    if angle_left > 160:
                        stage_left = "down"
                    if angle_left < 30 and stage_left == 'down' and not repetition_detected:
                        stage_left = "up"
                        counter += 1
                        repetition_detected = True

                    if angle_right > 160:
                        stage_right = "down"
                    if angle_right < 30 and stage_right == 'down' and not repetition_detected:
                        stage_right = "up"
                        counter += 1
                        repetition_detected = True

                    if angle_left > 30:
                        repetition_detected = False
                    if angle_right > 30:
                        repetition_detected = False

                except:
                    pass

                cv2.rectangle(image, (0, 0), (455, 73), (245, 117, 16), -1)

                cv2.putText(image, 'REPS', (15, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

                cv2.putText(image, f'{counter}', (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

                cv2.putText(image, 'LEFT STAGE', (120, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, f'{stage_left}', (100, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

                cv2.putText(image, 'RIGHT STAGE', (320, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, f'{stage_right}', (300, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)


                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

                # Display the image in the Streamlit app
                placeholder.image(image, channels="BGR")

        # Release the video capture when the loop exits
        cap.release()

if __name__ == "__main__":
    main()
