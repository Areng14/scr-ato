print("Initialising...")
print("Loading libaries...")

#Config!
#The code is below this commented area.
#Selected train speed limit.
#Used to calculate the target speed
max_speed = 90

#Stations
valid_station_names = [
    "Terminal 1", "Terminal 2", "Airport Terminal 3", "Airport West", "Airport Central",
    "Angel Pass", "Ashlan Park", "Beaulieu Park", "Beechley", "Benton", "Benton Bridge",
    "Berrily", "Berrily Denton Road", "Bodin", "Cambridge Street Parkway", "City Hospital",
    "Connolly", "Coxly", "Coxly Newtown", "East Berrily", "Eden Quay", "Edgemead",
    "Elsemere Junction", "Elsemere Pond", "Esterfield", "Faraday Road", "Farleigh",
    "Faymere", "Financial Quarter", "Greenslade", "Hallam Square", "Hampton Hargate",
    "Hemdon Park", "Houghton Rake", "James Street", "Leighton City", "Leighton Stepford Road",
    "Leighton West", "Llyn-by-the-Sea", "Millcastle", "Millcastle Racecourse", "Morganstown",
    "Morganstown Docks", "New Harrow", "Newry", "Newry Harbour", "Northshore", "Old Harrow",
    "Port Benton", "Robinson Way", "Rocket Parade", "Rosedale Village", "St Helens Bridge",
    "St Helens Park", "St Helens South", "Starryloch", "Stepford Airport Central", "Stepford Airport Parkway",
    "Stepford Central", "Stepford East", "Stepford High Street", "Stepford Southgate",
    "Stepford United Football Club", "Stepford Victoria", "University", "Upper Staploe",
    "Water Newton", "West Benton", "West Berrily", "Westercoast",
    "Westwyvern", "Whitefield", "Whitefield Lido", "Whitney Green", "Willowfield"
]


import init
import pyautogui
import os
import re
import sys
import atexit
import timings
import numpy as np
import pytesseract
import keyboard
from statistics import mean
from PIL import Image, ImageEnhance, ImageFilter
import time
from screeninfo import get_monitors

if os.path.basename(sys.executable) == "python.exe":
    path = __file__.replace(os.path.basename(__file__),"")
else:
    path = sys.executable.replace(os.path.basename(sys.executable),"")

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

screen_dimen = init.screen_dimen

print()

def improveOCR(image, threshold = 140):

    contrast_enhancer = ImageEnhance.Contrast(image)
    enhanced_contrast_image = contrast_enhancer.enhance(4.0)
    brightness_enhancer = ImageEnhance.Brightness(enhanced_contrast_image)
    enhanced_brightness_image = brightness_enhancer.enhance(0.75)
    sharpness_enhancer = ImageEnhance.Sharpness(enhanced_brightness_image)
    enhanced_sharpness_image = sharpness_enhancer.enhance(2.0)
    grayscale_image = enhanced_sharpness_image.convert("L")
    noise_reduced_image = grayscale_image.filter(ImageFilter.MedianFilter(size=3))
    binarized_image = noise_reduced_image.point(lambda x: 0 if x < threshold else 255, '1')

    return binarized_image

def getbar():
    bar_region = (0, screen_dimen[1] * 15 / 16, screen_dimen[0], screen_dimen[1] / 16)
    screenshot = pyautogui.screenshot(region=bar_region)
    w, h = screenshot.size
    crop_region = (w / 3, 0, w * 2 / 3, h)
    menubar = screenshot.crop(crop_region)
    return menubar

class Speed:
    def __init__(self, screen_dimen, train_max):
        self.screen_dimen = screen_dimen
        self.full_acceleration_time = 0
        self.last_speed = 0
        self.train_max = train_max

    def calibrate(self):
        print(">--- CALIBRATION")
        def get_green_height():
            # Get the image bar from some source
            bar = getbar()  
            w, h = bar.size
            crop_width = 5
            left = ((w - crop_width) / 2) - (w * 0.035)
            top = h * 0.15
            bottom = h - (h * 0.1)
            right = left + crop_width
            throttle_bar = bar.crop((left, top, right, bottom))

            # Convert to RGB if not already
            throttle_bar_rgb = throttle_bar.convert("RGB")

            # Analyzing the image to find green pixels
            max_height = 0
            current_height = 0
            for y in range(throttle_bar_rgb.height):
                is_green = False
                for x in range(throttle_bar_rgb.width):
                    r, g, b = throttle_bar_rgb.getpixel((x, y))
                    if g > r and g > b:  # Simple check for green dominance
                        is_green = True
                        break
                if is_green:
                    current_height += 1
                else:
                    if current_height > max_height:
                        max_height = current_height
                    current_height = 0

            # Check last segment
            if current_height > max_height:
                max_height = current_height

            return max_height
        
        times = []

        keyboard.press("s")
        time.sleep(4)
        keyboard.release("s")
        for x in range(4):
            bar = getbar()
            w, h = bar.size
            crop_width = 5
            left = ((w - crop_width) / 2) - (w * 0.035)
            top = h * 0.15
            bottom = h - (h * 0.1)
            right = left + crop_width
            maxheight = bar.crop((left, top, right, bottom)).size[1]
            start_time = time.time()
            keyboard.press("w")

            while True:
                green = get_green_height()
                if green >= maxheight:
                    break
            
            keyboard.release("w")
            end_time = time.time()
            keyboard.press("s")
            time.sleep(4)
            keyboard.release("s")

            # Adjusted time based on your logic
            adjusted_time = end_time - start_time
            times.append(adjusted_time)  # Store the time
            print(f">- Round {x}: {adjusted_time}")

        average = min(times)

        print(">--- END OF CALIBRATION")
        self.full_acceleration_time = average
        return average
    
    def settime(self,time):
        self.full_acceleration_time = time

    def gotospeed(self, speed):
        if self.last_speed:
            last_time = (self.full_acceleration_time / self.train_max) * self.last_speed
        else:
            last_time = 0

        if speed > max_speed:
            speed = max_speed

        target_time = (self.full_acceleration_time / self.train_max) * speed
        time_difference = abs(target_time - last_time)

        if speed > self.last_speed:
            keyboard.press("w")
            time.sleep(time_difference)
            keyboard.release("w")
        elif speed < self.last_speed:
            keyboard.press("s")
            time.sleep(time_difference)
            keyboard.release("s")

        self.last_speed = speed

    def train_stop(self,force_shutdown=False):
        #Since adjusting the throttle with time can lead to misspeeds
        #force_shutdown will be called at stations to fix it.
        if self.last_speed or force_shutdown:
            target_time = (self.full_acceleration_time / self.train_max) * self.last_speed + 0.25
        else:
            target_time = 4
        keyboard.press("s")
        time.sleep(target_time)
        keyboard.release("s")
        self.last_speed = 0

    def get_speedlimit(self):
        bar = getbar()
        w, h = bar.size
        bar = bar.resize((w * 4, h * 4), Image.LANCZOS) 
        left = w * 0.48 * 4
        upper = h * 0.45 * 4
        right = w * 0.525 * 4
        lower = h * 0.7 * 4
        speedimg = bar.crop((left, upper, right, lower))
        speedimg = improveOCR(speedimg, 50) 
        custom_config = r'--oem 3 --psm 6 outputbase digits'
        speedlimit = pytesseract.image_to_string(speedimg, config=custom_config)
        speedlimit = re.sub(r'\D', '', speedlimit)
        if speedlimit:
            return int(speedlimit)
        else:
            return self.last_speed

#Aquire next station
class Info:
    def __init__(self, screen_dimen):
        self.screen_dimen = screen_dimen
        self.next_station = None
        self.distance = None
        self.headcode = None
        self.lateness = None

    def getinfo(self):
        bar = getbar()
        w, h = bar.size
        left = w * 0.15
        upper = h * 0.05
        right = w * 0.45
        lower = h

        return bar.crop((left, upper, right, lower))

    def get_next(self):
        nextimg = self.getinfo()
        w, h = nextimg.size
        left = w * 0.025
        upper = h * 0.35
        right = w * 0.975
        lower = h * 0.7
        nextimg = nextimg.crop((left, upper, right, lower))
        
        nextstation_raw = pytesseract.image_to_string(nextimg, lang="eng")
        nextstation = re.sub("[^a-zA-Z0-9\s]", "", nextstation_raw)
        self.next_station = nextstation
        return nextstation

    def getdistance(self):
        distimg = self.getinfo()
        w, h = distimg.size
        left = w * 0.025
        upper = h * 0.7
        right = w * 0.6
        lower = h * 0.925
        distimg = distimg.crop((left, upper, right, lower))
        distance = pytesseract.image_to_string(distimg,"eng").split(" ")[3]
        distance = distance.replace("miles","").replace("\n","")
        if distance:
            self.distance = distance
            return float(distance)
        else:
            return self.distance

    def gethead(self):
        headimg = self.getinfo()
        w, h = headimg.size
        headimg = headimg.resize((w * 2, h * 2), Image.LANCZOS) 
        left = w * 0.4 * 2
        upper = h * 0.127 * 2
        right = w * 0.6 * 2
        lower = h * 0.3 * 2
        headimg = headimg.crop((left, upper, right, lower))
        headimg = improveOCR(headimg, 25) 
        headcode = pytesseract.image_to_string(headimg)
        self.headcode = headcode
        return headcode
    
class signal:
    def __init__(self, screen_dimen):
        self.screen_dimen = screen_dimen
        self.next_station = None
        self.sig_type = None
        self.sig_code = None
        self.last_sig_code = None

    def getsigcode(self):
        if self.sig_code:
            self.last_sig_code = self.sig_code
        bar = getbar()
        w, h = bar.size

        bar = bar.resize((w * 2, h * 2), Image.LANCZOS)
        left = w * 0.805 * 2
        upper = h * 0.1 * 2
        right = w * 0.895 * 2
        lower = h * 0.95 * 2
        bar = bar.crop((left, upper, right, lower))
        w, h = bar.size
        bar = bar.resize((w * 4, h * 4), Image.LANCZOS)
        left = w * 0.15 * 4
        upper = 0
        right = w * 0.9 * 4
        lower = h * 0.3 * 4
        bar = bar.crop((left, upper, right, lower))
        enhancer = ImageEnhance.Contrast(bar)
        bar = enhancer.enhance(2)
        bar = bar.convert('L')
        bar = bar.filter(ImageFilter.MedianFilter(size=3))
        bar = bar.point(lambda p: 255 if p > 75 else 0)
        custom_config = r'--oem 1 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        code = pytesseract.image_to_string(bar, config=custom_config)
        code = code.replace("o", "0").replace("\n","").upper().replace("S","").replace("L","").replace("C","").replace("W","").replace("A","").strip().replace(" ","")[-3:]
        self.sig_code = code
        pattern = r'^[0-9]{3}$'
        if re.match(pattern, code):
            return code
        else:
            return
    
    def getsig(self):
        bar = getbar()
        w, h = bar.size
        bar = bar.resize((w * 2, h * 2), Image.LANCZOS)
        bar = bar.crop((w * 0.805 * 2, h * 0.1 * 2, w * 0.895 * 2, h * 0.95 * 2))
        w, h = bar.size
        bar = bar.resize((w * 2, h * 2), Image.LANCZOS)
        left = w * 0.1 * 2
        upper = h * 0.1 * 2
        right = w * 0.4 * 2
        lower = h * 0.95 * 2
        bar = bar.crop((left, upper, right, lower))
        w, h = bar.size
        signal_aspects = []
        regions = [(0.5, 0.05, 0.6, 0.15),
                (0.5, 0.3, 0.6, 0.4),
                (0.5, 0.6, 0.6, 0.7),
                (0.5, 0.8, 0.6, 0.9)]

        def get_dominant_color(image):
            # Convert image to numpy array
            data = np.array(image)
            # Reshape data to be list of RGB values
            data = data.reshape((-1, 3))
            # Find the color that occurs most often
            unique_colors, counts = np.unique(data, axis=0, return_counts=True)
            dominant_color = unique_colors[np.argmax(counts)]
            return dominant_color

        for left, upper, right, lower in regions:
            region = (w * left, h * upper, w * right, h * lower)
            cropped_image = bar.crop(region)
            dominant_color = get_dominant_color(cropped_image)

            # Thresholds for color detection (RGB values), adjust as needed
            if np.allclose(dominant_color, [0, 255, 0], atol=50):  # Green
                signal_aspects.append(1)
            elif np.allclose(dominant_color, [255, 190, 0], atol=50):  # Yellow
                signal_aspects.append(1)
            elif np.allclose(dominant_color, [255, 0, 0], atol=50):  # Red
                signal_aspects.append(1)
            else:
                signal_aspects.append(0)  # None or unrecognized

        if signal_aspects == [0,1,0,0]:
            return 1 #green
        elif signal_aspects == [1,0,1,0]:
            return 2 #pre yellow
        elif signal_aspects == [0,0,1,0]:
            return 3 #yellow
        elif signal_aspects == [0,0,0,3]:
            return 4 #red
        else:
            return 1

#Todo:
#SIGNALS

infoman = Info(screen_dimen)
signalman = signal(screen_dimen)

lastlimt = -1
GoA_level = 2

if GoA_level == 0:
    print("Mode: GoA0\nThis GoA level is not supported! AWS and ATP exist in SCR.\nExiting...")
    sys.exit(1)
elif GoA_level == 1:
    print("Mode: GoA1\nManual operation. Driver controls the train.\nExiting...")
    sys.exit(1)
elif GoA_level == 2:
    print("Mode: GoA2\nSemi-automated driving. Train controls starting and stopping, driver handles doors and emergencies.")
elif GoA_level == 3:
    print("Mode: GoA3\nDriverless operation. Auto Pilot mode.\nYou control doors.")
elif GoA_level == 4:
    print("Mode: GoA4\nFull automation. Auto Pilot mode.\nDo not touch the keyboard from now.")

nextstation = None
lastsig = 0

def cleanup():
    print("\n\nCleaning up...")
    print("Stopping train.")
    Speedcontroller.train_stop(True)

print(f"Train max speed is: {max_speed}")

keyboard.wait("p")
print("starting")
Speedcontroller = Speed(screen_dimen,max_speed)

time.sleep(0.5)

#Calibrate IF FILE DOESNT EXIST or if C held
if not os.path.isfile(os.path.join(path,"data","time.txt")) or keyboard.is_pressed("c"):
    print("Calibrating...")
    fullthrottletime = Speedcontroller.calibrate()
    with open(os.path.join(path,"data","time.txt"),"w") as file:
        file.write(str(fullthrottletime))
else:
    with open(os.path.join(path,"data","time.txt"),"r") as file:
        content =  file.read()
    if content:
        Speedcontroller.settime(float(content))
    else:
        print("Calibrating...")
        fullthrottletime = Speedcontroller.calibrate()
        with open(os.path.join(path,"data","time.txt"),"w") as file:
            file.write(str(fullthrottletime))

print(f"Sucesfully calibrated train. TFS: {Speedcontroller.full_acceleration_time}s")

atexit.register(cleanup)

while True:
    if not nextstation:
        for x in range(100):
            nextstation = infoman.get_next().strip()
            if nextstation:
                if nextstation.replace("  "," ").replace("_","").strip().title() in valid_station_names:
                    print(nextstation)
                    break
            else:
                pass
            
        if not nextstation:
            print("Failed to read next station.")
            nextstation = input("Type in the next station:\n")
            while nextstation not in valid_station_names:
                print("Not a valid statation.")
                nextstation = input("Type in the next station:\n")
    limit = Speedcontroller.get_speedlimit()
    #If last recorded limit is not the same update it
    signalread = signalman.getsig()
    if lastlimt != limit and signalread == 1:
        Speedcontroller.gotospeed(limit)
        lastlimt = limit
        lastsig = signalread
    if signalread == 2:
        if GoA_level > 2 or 1==1:
            keyboard.press_and_release("q")
        else:
            pass
    if signalread == 3:
        Speedcontroller.gotospeed(45)
        if GoA_level > 2 or 1==1:
            keyboard.press_and_release("q")
        else:
            pass
    if signalread == 4:
        Speedcontroller.gotospeed(15)
        time.sleep(7)
        Speedcontroller.train_stop()
        lastsig = signalread
    #If station is within 0.25 miles. Slow down and stop.
    if infoman.getdistance() < 0.25:
        Speedcontroller.train_stop()
        Speedcontroller.gotospeed(timings.getspeed(nextstation))
        passed = []
        while infoman.getdistance() > 0.00:
            code = signalman.getsigcode()
            if code:
                passed.append(code)
                
            keyboard.press_and_release("q")
        passed = list(set(passed))
        got = None
        if passed:
            got = timings.gettime(nextstation,passed[-1])
        if got != None:
            time.sleep(got)
        else:
            nexttime = timings.gettimen(nextstation)
            time.sleep(nexttime)
        if passed:
            stringyes = '- ' + '\n- '.join(passed)
            print(f"DEBUG - PASS\nNS: {nextstation}\nLP: {passed[-1]}\nPS: \n{stringyes}\n---")
        if got != None:
            print(f"Signal Stop:\nNS: {nextstation}\nSL: {got}\nSG: {passed[-1]}\n---")
        else:
            print(f"Station Stop:\nNS: {nextstation}\nSL: {nexttime}\n---")
        print("\n\n")
        if GoA_level < 3:
            Speedcontroller.train_stop(True)
            time.sleep(5)
            keyboard.wait("p")
            lastlimt = -1
        else:
            pass
            #implement auto doors

        nextstation = None
        lastsig = 0