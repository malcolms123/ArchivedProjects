from pynput.keyboard import Key, Controller
import time

time.sleep(5)

keyboard = Controller()

s = "y"

for char in s:
	keyboard.press(char)
	time.sleep(0.1)
	keyboard.release(char)
