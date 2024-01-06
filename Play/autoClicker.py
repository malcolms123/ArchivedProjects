# code written by chatgpt

import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

# The key that will start and stop the autoclicker
toggle_key = KeyCode(char='u')

# The mouse controller for clicking
mouse = Controller()

# The delay between clicks
delay = 0.01

# Indicates whether the autoclicker is running
running = False

def click_mouse():
    """The function for the thread to continuously click the mouse."""
    while True:
        if running:  # Only click if the autoclicker is running
            mouse.click(Button.left, 1)
        time.sleep(delay)  # Wait for the specified delay before the next click

def on_press(key):
    """Defines what to do when the toggle key is pressed."""
    global running
    if key == toggle_key:  # If the toggle key is pressed, change the running state
        running = not running

# Set up and start the clicker thread
click_thread = threading.Thread(target=click_mouse)
click_thread.start()

# Listen for the toggle key press to start/stop autoclicker
with Listener(on_press=on_press) as listener:
    listener.join()
