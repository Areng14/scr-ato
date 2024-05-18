import pyautogui
import os
import PIL as image
import sys
from screeninfo import get_monitors

screen_width, screen_height = pyautogui.size()

screenshot = pyautogui.screenshot()

if os.path.basename(sys.executable) == "python.exe":
    path = __file__.replace(os.path.basename(__file__),"")
else:
    path = sys.executable.replace(os.path.basename(sys.executable),"")

def list_monitors():
    monitors = get_monitors()
    for i, monitor in enumerate(monitors):
        print(f"Monitor {i + 1}: {monitor.width}x{monitor.height}")

list_monitors()

print("Loaded libaries!")

monitors = get_monitors()
os.makedirs(os.path.join(path,"data"),exist_ok=True)

if not os.path.isfile(os.path.join(path,"data","screen.txt")):
    monitor_choice = int(input("Enter the monitor number to capture: "))
    selected_monitor = monitors[monitor_choice - 1]
    with open(os.path.join(path,"data","screen.txt"),"w") as file:
        file.write(str(monitor_choice))
else:
    with open(os.path.join(path,"data","screen.txt"),"r") as file:
        monitor_choice = int(file.read())
    selected_monitor = monitors[monitor_choice - 1]
print("Screen size:", selected_monitor.width, "x", selected_monitor.height)

screen_dimen = (selected_monitor.width,selected_monitor.height)