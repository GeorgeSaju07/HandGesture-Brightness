"""
Hand Gesture-Based Brightness Control

This Python script dynamically adjusts screen brightness based on hand gestures
using a webcam. It leverages OpenCV for video processing, Mediapipe for real-time
hand tracking, and Screen Brightness Control (SBC) to modify screen brightness.
By measuring the distance between the thumb and index finger, the script interpolates
brightness levels, allowing intuitive, touch-free control. Move your fingers closer
to decrease brightness and farther apart to increase it. Press 'q' to exit the program.

Author: George Saju
Date: 05/03/2025
"""


import cv2
import mediapipe as mp
import numpy as np
from math import hypot
import screen_brightness_control as sbc

# Initialize Mediapipe Hand module
mp_hands = mp.solutions.hands  # Loads the hand detection model
mp_draw = mp.solutions.drawing_utils  # Utility to draw hand landmarks


def get_hand_landmarks(image, hands):
    """
    Detect hand landmarks in the given image using Mediapipe.

    Args:
        image: The input image from the webcam.
        hands: Mediapipe Hands object for processing.

    Returns:
        landmarks_list: A list of (id, x, y) for detected hand landmarks.
    """
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR (OpenCV) to RGB (Mediapipe format)
    results = hands.process(image_rgb)  # Process the image to detect hands

    # Store hand landmark positions
    landmarks_list = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for id, lm in enumerate(hand_landmarks.landmark):
                # Get image dimensions
                h, w, _ = image.shape
                # Convert normalized coordinates to pixel values
                cx, cy = int(lm.x * w), int(lm.y * h)

                # Append landmark ID and coordinates
                landmarks_list.append((id, cx, cy))
            # Draw landmarks on the image
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Return the list of detected hand landmarks
    return landmarks_list


def calculate_brightness(thumb, index_finger):
    """
    Calculate brightness level based on the distance between thumb and index finger.

    Args:
        thumb: (x, y) coordinate of the thumb tip.
        index_finger: (x, y) coordinate of the index finger tip.

    Returns:
        brightness: Brightness value (0-100%).
        distance: Distance between the thumb and index finger.
    """

    # Thumb tip coordinates
    x1, y1 = thumb
    # Index finger tip coordinates
    x2, y2 = index_finger
    # Compute Euclidean distance between two points
    distance = hypot(x2 - x1, y2 - y1)

    # Map the distance range (15-220) to brightness levels (0-100)
    brightness = np.interp(distance, [15, 220], [0, 100])

    # Return brightness percentage and distance
    return int(brightness), distance


def main():
    """
    Main function to capture video from webcam, detect hand gestures, and control brightness.
    """
    # Open the default webcam
    cap = cv2.VideoCapture(0)
    # Initialize Mediapipe Hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

    while cap.isOpened():
        # Capture a frame from the webcam
        success, frame = cap.read()
        # If frame capture fails, exit the loop
        if not success:
            print("Failed to capture frame. Exiting...")
            break

        landmarks = get_hand_landmarks(frame, hands)  # Detect hand landmarks

        # Ensure at least 9 landmarks are detected
        if landmarks and len(landmarks) >= 9:
            # Extract thumb tip (x, y) coordinates
            thumb_tip = landmarks[4][1:3]
            # Extract index finger tip (x, y) coordinates
            index_tip = landmarks[8][1:3]

            # Compute brightness based on distance
            brightness, distance = calculate_brightness(thumb_tip, index_tip)
            # Display brightness level in console
            print(f"Brightness: {brightness}%, Distance: {distance:.2f}")

            sbc.set_brightness(brightness)  # Apply brightness to the screen

            # Draw UI elements for visualization
            cv2.circle(frame, thumb_tip, 6, (255, 0, 0), cv2.FILLED)  # Draw a blue circle at the thumb tip
            cv2.circle(frame, index_tip, 6, (255, 0, 0), cv2.FILLED)  # Draw a blue circle at the index finger tip
            cv2.line(frame, thumb_tip, index_tip, (255, 0, 0), 3)  # Draw a line between the fingers

        # Display the output video with hand tracking
        cv2.imshow("Hand Gesture Brightness Control", frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release resources and close the webcam window
    cap.release()
    cv2.destroyAllWindows()


# Run the main function only if the script is executed directly
if __name__ == "__main__":
    main()
