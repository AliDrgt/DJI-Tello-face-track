# DJI Tello Drone Face Tracking

A face tracking system using a DJI Tello drone, OpenCV, and the `djitellopy` library.

## Features

- Real-time video stream from DJI Tello drone
- Face detection and tracking using OpenCV
- Drone movement control to maintain face within the frame

## Files

- `haarFace.xml`: Haar cascade file for face detection
- `face_track.py`: Main script for running the face tracking

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/username/tello-face-tracking.git
    ```
2. Navigate to the project directory:
    ```sh
    cd tello-face-tracking
    ```
3. (Optional) Create a virtual environment and activate it:
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```
4. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

Run the face tracking script using the following command:
    ```sh
    python face_track.py
    ```

## How It Works

1. The script connects to the DJI Tello drone and starts the video stream.
2. It initializes the face detection using a Haar cascade classifier.
3. For each frame, it detects faces and calculates the area and center coordinates.
4. The drone adjusts its position based on the detected face to keep it centered in the frame.

## Acknowledgments

This project was created by Ali Durgut.


