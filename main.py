import keyboard
import time
import winsound

toggled = False

ACTIVATE_FREQ = 880
DEACTIVATE_FREQ = 440
DURATION = 200

print("Press RIGHT SHIFT to toggle HOLDING S ON/OFF.")
print("Press ESC to exit.")

while True:
    if keyboard.is_pressed('esc'):
        if toggled:
            keyboard.release('s')  # Release if holding
        print("ESC pressed. Exiting...")
        break

    if keyboard.is_pressed('right shift'):
        time.sleep(0.2)  # Debounce

        toggled = not toggled

        if toggled:
            keyboard.press('s')  # HOLD S down
            print("Holding S down!")
            winsound.Beep(ACTIVATE_FREQ, DURATION)
        else:
            keyboard.release('s')  # RELEASE S
            print("Released S!")
            winsound.Beep(DEACTIVATE_FREQ, DURATION)

        while keyboard.is_pressed('right shift'):
            time.sleep(0.1)  # Wait until the key is released to avoid toggling again immediately
    time.sleep(0.5)  # Prevent high CPU usage