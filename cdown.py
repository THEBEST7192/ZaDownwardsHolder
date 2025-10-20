import time
import winsound
import ctypes
import pygetwindow as gw
import keyboard

ACTIVATE_FREQ = 880
DEACTIVATE_FREQ = 440
DURATION = 200

TARGET_WINDOW_HANDLE = None

print("Press RIGHT SHIFT to find Eden and start the S/C loop.")
print("Press ESC to exit.")

user32 = ctypes.windll.user32
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
VK_S = 0x53
VK_C = 0x43
MAPVK_VK_TO_VSC = 0

def find_eden_window():
    windows = gw.getWindowsWithTitle("Eden")
    if windows:
        return windows[0]._hWnd
    else:
        print("No window with 'Eden' in the title found!")
        return None

def make_lparam(vk, keyup=False):
    scan_code = user32.MapVirtualKeyA(vk, MAPVK_VK_TO_VSC) & 0xFF
    lparam = 1 | (scan_code << 16)
    if keyup:
        lparam |= (1 << 30) | (1 << 31)
    return lparam

def send_key(hwnd, vk, action):
    if action == "press":
        user32.SendMessageA(hwnd, WM_KEYDOWN, vk, make_lparam(vk))
    elif action == "release":
        user32.SendMessageA(hwnd, WM_KEYUP, vk, make_lparam(vk, keyup=True))

toggled = False

while True:
    if keyboard.is_pressed('esc'):
        print("ESC pressed. Exiting...")
        break

    if keyboard.is_pressed('right shift'):
        time.sleep(0.2)
        if TARGET_WINDOW_HANDLE is None:
            TARGET_WINDOW_HANDLE = find_eden_window()
            if TARGET_WINDOW_HANDLE:
                print("Target window handle set.")
            else:
                print("Could not find Eden window.")
                while keyboard.is_pressed('right shift'):
                    time.sleep(0.1)
                continue

        toggled = not toggled
        if toggled:
            print("Loop started: S 1s -> C x5 (2s interval) -> wait 15s")
            winsound.Beep(ACTIVATE_FREQ, DURATION)
        else:
            send_key(TARGET_WINDOW_HANDLE, VK_S, "release")
            print("Loop stopped!")
            winsound.Beep(DEACTIVATE_FREQ, DURATION)

        while keyboard.is_pressed('right shift'):
            time.sleep(0.1)

    if toggled and TARGET_WINDOW_HANDLE:
        # Phase 1: Hold S for 1 second
        send_key(TARGET_WINDOW_HANDLE, VK_S, "press")
        time.sleep(1)
        send_key(TARGET_WINDOW_HANDLE, VK_S, "release")

        # Phase 2: Press C four times, 2 seconds apart
        for _ in range(5):
            send_key(TARGET_WINDOW_HANDLE, VK_C, "press")
            time.sleep(0.03)  # hold C for 30ms
            send_key(TARGET_WINDOW_HANDLE, VK_C, "release")
            time.sleep(3)  # wait 2 seconds between presses

        # Phase 3: Wait 15 seconds before repeating
        print("Cycle completed, waiting 15 seconds...")
        time.sleep(15)
