import cv2
import mediapipe as mp
import csv
import time
import math

# =====================
# FUNCTIONS
# =====================
def distance(p1, p2):
    """3D distance between two points"""
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)

def scale_measurement(raw_value, scale_factor):
    """Scale normalized MediaPipe value to real-world cm"""
    return raw_value * scale_factor

# =====================
# SETUP MEDIAPIPE
# =====================
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# =====================
# CAPTURE LANDMARKS
# =====================
cap = cv2.VideoCapture(0)
num_frames_to_capture = 10
frames_captured = 0
landmarks_list = []

print("Stand in front of the camera...")

while frames_captured < num_frames_to_capture:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        frame_landmarks = []
        for lm in results.pose_landmarks.landmark:
            frame_landmarks.append((lm.x, lm.y, lm.z))
        landmarks_list.append(frame_landmarks)
        frames_captured += 1
        print(f"Captured frame {frames_captured}/{num_frames_to_capture}")

    cv2.imshow('Pose Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(0.3)

cap.release()
cv2.destroyAllWindows()

if not landmarks_list:
    print("No landmarks detected. Exiting.")
    exit()

# =====================
# SAVE RAW LANDMARKS
# =====================
with open("body_landmarks.csv", "w", newline="") as f:
    writer = csv.writer(f)
    header = []
    for i in range(33):
        header.extend([f"x{i}", f"y{i}", f"z{i}"])
    writer.writerow(header)
    for lm_set in landmarks_list:
        row = []
        for lm in lm_set:
            row.extend(lm)
        writer.writerow(row)

print("Raw landmarks saved to body_landmarks.csv")

# =====================
# ASK REAL HEIGHT
# =====================
real_height_cm = float(input("Enter your real height in cm: "))

# =====================
# CALCULATE FINAL MEASUREMENTS
# =====================
final_measurements = []

for lm_set in landmarks_list:
    # Key points
    left_shoulder = lm_set[11]
    right_shoulder = lm_set[12]
    left_elbow = lm_set[13]
    right_elbow = lm_set[14]
    left_wrist = lm_set[15]
    right_wrist = lm_set[16]
    left_hip = lm_set[23]
    right_hip = lm_set[24]
    left_knee = lm_set[25]
    right_knee = lm_set[26]
    left_ankle = lm_set[27]
    right_ankle = lm_set[28]
    nose = lm_set[0]
    left_eye = lm_set[1]
    right_eye = lm_set[2]

    # Calculate raw body height from nose to ankles average
    raw_height = distance(nose, ((left_ankle[0]+right_ankle[0])/2,
                                 (left_ankle[1]+right_ankle[1])/2,
                                 (left_ankle[2]+right_ankle[2])/2))
    scale = real_height_cm / raw_height

    # Apply scale to all measurements
    measurements = {
        "shoulder_width": distance(left_shoulder, right_shoulder) * scale,
        "hip_width": distance(left_hip, right_hip) * scale,
        "left_arm_length": (distance(left_shoulder, left_elbow) + distance(left_elbow, left_wrist)) * scale,
        "right_arm_length": (distance(right_shoulder, right_elbow) + distance(right_elbow, right_wrist)) * scale,
        "left_leg_length": (distance(left_hip, left_knee) + distance(left_knee, left_ankle)) * scale,
        "right_leg_length": (distance(right_hip, right_knee) + distance(right_knee, right_ankle)) * scale,
        "body_height": raw_height * scale,
        "neck_width": distance(left_shoulder, right_shoulder) * 0.25 * scale,  # approximate
        "chest_circumference": distance(left_shoulder, right_shoulder) * 1.2 * scale,
        "waist_circumference": distance(left_hip, right_hip) * 1.1 * scale,
        "head_width": distance(left_eye, right_eye) * scale,
        "head_height": distance(nose, ((left_eye[0]+right_eye[0])/2,
                                       (left_eye[1]+right_eye[1])/2,
                                       (left_eye[2]+right_eye[2])/2)) * scale
    }
    final_measurements.append(measurements)

# =====================
# SAVE FINAL MEASUREMENTS
# =====================
with open("final_body_measurements.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=final_measurements[0].keys())
    writer.writeheader()
    for m in final_measurements:
        writer.writerow(m)

print("Final body measurements saved to final_body_measurements.csv!")
