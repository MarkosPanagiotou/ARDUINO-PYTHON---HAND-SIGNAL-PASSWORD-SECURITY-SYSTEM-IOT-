import pyfirmata2
import time

board = pyfirmata2.Arduino('COM3')

led_1 = board.get_pin('d:8:o')
led_2 = board.get_pin('d:9:o')
led_3 = board.get_pin('d:10:o')
led_4 = board.get_pin('d:11:o')

while True:
    led_1.write(1)
    time.sleep(1)
    led_1.write(0)

    led_2.write(1)
    time.sleep(1)
    led_2.write(0)

    led_3.write(1)
    time.sleep(1)
    led_3.write(0)

    led_4.write(1)
    time.sleep(1)
    led_4.write(0)
