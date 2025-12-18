Hand Signal Password System with Arduino & Python
Overview

This project is a real-time hand gesture recognition system that allows users to enter a multi-step password using their fingers. The system uses a webcam with OpenCV and CVZone to track hand gestures and communicates with an Arduino to control LEDs and a buzzer.

Correct finger sequence → all LEDs light up + success melody plays.

Incorrect finger → short buzzer beep.

Maximum wrong attempts → critical buzzer alert for 2 seconds.

On-screen feedback includes finger count, countdowns, and success messages.

Features

Real-time hand tracking using OpenCV and CVZone.

Step-by-step finger input with 1.5-second delay per step for accurate input.

5-second ready timer before starting the password input.

Visual feedback on the camera: current finger count and success message.

Hardware feedback via Arduino-controlled LEDs and buzzer.

Emergency alert after too many wrong attempts.

Hardware Required

Arduino board (e.g., Uno, Nano)

4 LEDs connected to pins 8, 9, 10, 11

Buzzer connected to pin 2

USB connection to your computer

Software Requirements

Python 3.x

OpenCV (opencv-python)

CVZone (cvzone)

PySerial (pyserial)

Install dependencies with:

pip install opencv-python cvzone pyserial

Arduino Setup

Upload the provided Arduino code (.ino) to your Arduino board. The Arduino code listens for serial commands from Python:

FINGERS: → receives LED states (e.g., FINGERS:1100).

BUZZER_WRONG → short beep for wrong input.

BUZZER_SUCCESS → plays success melody.

BUZZER_CRITICAL → continuous critical beep for 2 seconds.

Python Scripts
hello.py

Main script that opens the webcam, detects fingers, checks the password sequence, and communicates with Arduino.

Provides visual feedback and timers for step-by-step input.

Shows a “SUCCESS!” message when the password is correct.

controller.py

Handles serial communication with Arduino.

Functions:

send_fingers(finger_list) → lights LEDs according to finger input.

buzzer_wrong() → short beep.

buzzer_success() → success melody.

buzzer_critical() → critical 2-second beep.

cameraopener.py (optional)

Script to initialize and open the webcam feed (used by hello.py).

Usage

Connect the Arduino with LEDs and buzzer as described.

Upload the Arduino .ino code.

Open Python and run hello.py:

python hello.py


Wait for the 5-second ready timer, then enter the finger sequence.

LEDs and buzzer will provide real-time feedback:

Correct sequence → all LEDs ON + success melody.

Wrong input → short beep.

Maximum wrong attempts → critical 2-second beep.

Project Flow

Ready countdown (5 seconds) before starting.

Step-by-step finger input with 1.5-second gap per finger.

Correct sequence: success message on camera + all LEDs ON + buzzer melody.

Wrong input: buzzer beep.

Too many wrong attempts: critical buzzer for 2 seconds.

5-second refresh before allowing a new attempt.

Notes

Make sure the camera has good lighting for accurate finger detection.

Keep your hand within the camera frame for best performance.

Adjust the password array in hello.py to change the finger sequence.


Sample videos for the Project:



https://github.com/user-attachments/assets/bfdfe45c-7e5d-42a1-83ba-6947e1107f54



https://github.com/user-attachments/assets/019cd112-9683-4c09-be51-ff938af68b26


