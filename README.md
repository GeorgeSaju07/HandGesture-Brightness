# HandGesture-Brightness
A Python-based hand gesture recognition system that dynamically controls screen brightness using OpenCV, Mediapipe, and Screen Brightness Control (SBC). The script detects the distance between the thumb and index finger to adjust brightness levels intuitively.

🚀 Features

🎥 Real-time hand tracking using Mediapipe

🖐️ Gesture-based brightness adjustment

🔄 Smooth and dynamic brightness control using interpolation

🖥️ Works on Windows, macOS, and Linux

⏹️ Simple & intuitive UI with visual markers

📌 How It Works

The script captures live video from the webcam.

It detects and tracks the thumb tip and index finger tip.

The distance between these two points determines screen brightness:

Closer fingers → Lower brightness

Farther fingers → Higher brightness

The brightness is dynamically updated in real-time.

Press 'q' to exit the program.

📦 Installation

🔹 Prerequisites

Ensure you have Python 3.7+ installed. Then, install the required dependencies:

pip install opencv-python mediapipe numpy screen-brightness-control

▶️ Usage

Run the script with the following command:

python hand_brightness_control.py

Now, control your screen brightness using your hand gestures! ✋💡

🛠️ Project Structure
📂 HandGesture-Brightness
│── hand_brightness_control.py   # Main script
│── README.md                    # Project documentation

🏗️ Future Enhancements

✅ Support for multi-hand detection

✅ Implement gesture-based volume control

✅ Add an on-screen brightness indicator

📜 License

This project is licensed under the MIT License.
