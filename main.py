import keyboard
import time
import winsound
import ctypes
import pygetwindow as gw

toggled = False
ACTIVATE_FREQ = 880
DEACTIVATE_FREQ = 440
DURATION = 200

TARGET_WINDOW_HANDLE = None

print("Press RIGHT SHIFT to search for an 'Eden' window and toggle HOLDING 's' ON/OFF (works in background).")
print("Press ESC to exit.")

user32 = ctypes.windll.user32

WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
VK_S = 0x53  # Virtual key code for 's'

def find_eden_window():
    windows = gw.getWindowsWithTitle("Eden")
    if windows:
        return windows[0]._hWnd
    else:
        print("No window with 'Eden' in the title found!")
        return None

def send_key_to_window(hwnd, action):
    if action == "press":
        user32.SendMessageA(hwnd, WM_KEYDOWN, VK_S, 0)
    elif action == "release":
        user32.SendMessageA(hwnd, WM_KEYUP, VK_S, 0)

while True:
    if keyboard.is_pressed('esc'):
        if toggled and TARGET_WINDOW_HANDLE:
            send_key_to_window(TARGET_WINDOW_HANDLE, "release")
        print("ESC pressed. Exiting...")
        break

    if keyboard.is_pressed('right shift'):
        time.sleep(0.2)  # Debounce

        if TARGET_WINDOW_HANDLE is None:
            TARGET_WINDOW_HANDLE = find_eden_window()
            if TARGET_WINDOW_HANDLE:
                print("Target window handle set.")
            else:
                print("Could not find an 'Eden' window. Make sure it is open.")
                while keyboard.is_pressed('right shift'):
                    time.sleep(0.1)
                continue

        toggled = not toggled
        if toggled:
            send_key_to_window(TARGET_WINDOW_HANDLE, "press")
            print("Holding 's' down in Eden window (background)!")
            winsound.Beep(ACTIVATE_FREQ, DURATION)
        else:
            send_key_to_window(TARGET_WINDOW_HANDLE, "release")
            print("Released 's' in Eden window (background)!")
            winsound.Beep(DEACTIVATE_FREQ, DURATION)

        while keyboard.is_pressed('right shift'):
            time.sleep(0.1)

    time.sleep(0.5)
