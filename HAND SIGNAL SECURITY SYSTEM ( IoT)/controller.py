import serial
import time

ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

def send_fingers(finger_list):
    """Send finger pattern to Arduino (1=LED on, 0=off)."""
    data = ''.join(str(f) for f in finger_list)
    ser.write(f"FINGERS:{data}\n".encode())

def buzzer_wrong():
    ser.write(b'BUZZER_WRONG\n')  # short beep

def buzzer_success():
    """Play success melody on buzzer."""
    ser.write(b'BUZZER_SUCCESS\n')

def buzzer_critical():
    """Play critical beep for 2 seconds"""
    ser.write(b'BUZZER_CRITICAL\n')
