# Import required libraries
import RPi.GPIO as GPIO
import time
import uinput  # For keyboard input emulation

# Define GPIO pins connected to the keypad
L1, L2, L3, L4 = 6, 13, 19, 26  # Row pins
C1, C2, C3, C4 = 12, 16, 20, 21  # Column pins

# Initialize the GPIO pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Setup row pins as output
GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

# Setup column pins as input with internal pull-down resistors
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Setup uinput device with key mappings for each button
device = uinput.Device([
    uinput.KEY_1, uinput.KEY_2, uinput.KEY_3, uinput.KEY_UP,
    uinput.KEY_4, uinput.KEY_5, uinput.KEY_6, uinput.KEY_DOWN,
    uinput.KEY_7, uinput.KEY_8, uinput.KEY_9, uinput.KEY_TAB,
    uinput.KEY_ENTER, uinput.KEY_0, uinput.KEY_BACKSPACE, uinput.KEY_D
])

# Dictionary to map keypad characters to uinput keys
key_map = {
    "1": uinput.KEY_1, "2": uinput.KEY_2, "3": uinput.KEY_3, "A": uinput.KEY_UP,
    "4": uinput.KEY_4, "5": uinput.KEY_5, "6": uinput.KEY_6, "B": uinput.KEY_DOWN,
    "7": uinput.KEY_7, "8": uinput.KEY_8, "9": uinput.KEY_9, "C": uinput.KEY_TAB,
    "*": uinput.KEY_ENTER, "0": uinput.KEY_0, "#": uinput.KEY_BACKSPACE, "D": uinput.KEY_D
}

# Track the key state to prevent repeated triggers
key_state = {key: False for key in key_map.keys()}

# Function to read each line and send the keypress if a key is detected
def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)  # Set the current row high
    for i, char in enumerate(characters):
        if GPIO.input([C1, C2, C3, C4][i]) == 1:  # If a key press is detected in this column
            if not key_state[char]:  # If the key was previously unpressed
                device.emit_click(key_map[char])  # Send the key press
                key_state[char] = True  # Mark the key as pressed
        else:
            key_state[char] = False  # Reset the key state when key is released
    GPIO.output(line, GPIO.LOW)  # Set the current row low

try:
    while True:
        # Call readLine for each row with corresponding characters
        readLine(L1, ["1", "2", "3", "A"])
        readLine(L2, ["4", "5", "6", "B"])
        readLine(L3, ["7", "8", "9", "C"])
        readLine(L4, ["*", "0", "#", "D"])
        time.sleep(0.1)  # Small delay to prevent rapid polling
except KeyboardInterrupt:
    print("\nApplication stopped!")
finally:
    GPIO.cleanup()  # Reset GPIO settings on exit
