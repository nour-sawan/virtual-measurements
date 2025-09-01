# Virtual Body Measurements

This project is a **Virtual Measurements** system that uses **MediaPipe** and **OpenCV** to capture 3D body landmarks from a person standing in front of a camera and calculate precise body measurements. The purpose is to demonstrate a **non-contact, automated body measurement solution** for virtual fitting, health tracking, or research purposes.

---

## Overview
- The user stands in front of the camera.
- The system captures **body landmarks** in 3D space using **MediaPipe Pose**.
- After capturing a few frames, the program requests the **real height** of the person to scale measurements accurately.
- The program then calculates key body measurements such as:
  - Shoulder width
  - Hip width
  - Arm lengths
  - Leg lengths
  - Neck width
  - Chest and waist circumference
  - Head width and height
  - Total body height
- Measurements are saved in **CSV files** for further analysis or use.

---

## Components of the Project
- **MediaPipe Pose** – Detects 33 key body landmarks in 3D space.
- **OpenCV** – Captures live video from the webcam and overlays landmarks.
- **CSV Export** – Stores raw landmark data and calculated measurements for analysis.

---

## Project Workflow
1. Stand in front of the camera.
2. The system captures several frames of body landmarks.
3. User inputs their real height to scale measurements accurately.
4. The system calculates measurements and saves them in CSV files.

---

## Use Cases
- Virtual fitting rooms and e-commerce.
- Fitness and health monitoring.
- Anthropometric studies and research.

---

## Tech Stack
- Python
- OpenCV
- MediaPipe
- CSV for data storage

---

## Notes
- The project was developed and tested inside a **Python virtual environment** to maintain clean dependencies.
- Screenshots included demonstrate the detection process using a placeholder image instead of a real person.

## Screenshots









