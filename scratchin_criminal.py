#!/usr/bin/env python3

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# This example is for use on Raspberry Pi computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

import time
import subprocess
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
import qrcode
import adafruit_rgb_display.st7789 as st7789
# import adafruit_rgb_display.ili9341 as ili9341
# import adafruit_rgb_display.hx8357 as hx8357
# import adafruit_rgb_display.st7735 as st7735
# import adafruit_rgb_display.ssd1351 as ssd1351
# import adafruit_rgb_display.ssd1331 as ssd1331

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = DigitalInOut(board.CE0)
dc_pin = DigitalInOut(board.D25)
reset_pin = DigitalInOut(board.D24)
 
# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the display:
# disp = ssd1331.SSD1331(spi,                   # 0.96" SSD1331
    # rotation=180,
# disp = st7735.ST7735R(spi,                    # 0.96" MiniTFT ST7735R
    # rotation=90,
    # bgr=True,
# disp = st7789.ST7789(spi,                     # 1.14" ST7789
    # rotation=90,
    # width=135,
    # height=240,
    # x_offset=53,
    # y_offset=40,
# disp = ssd1351.SSD1351(spi,                   # 1.27" SSD1351
    # height=96,
    # y_offset=32,
    # rotation=180,
disp = st7789.ST7789(spi,                     # 1.3", 1.54" ST7789
    rotation=180,
    height=240,
    y_offset=80,
# disp = st7735.ST7735R(spi,                    # 1.44" ST7735R
    # rotation=270,
    # height=128,
    # x_offset=2,
    # y_offset=3,
# disp = ssd1351.SSD1351(spi,                   # 1.5" SSD1351
    # rotation=180,
# disp = st7735.ST7735R(spi,                    # 1.8" ST7735R
    # rotation=90,
# disp = st7789.ST7789(spi,                     # 2.0" ST7789
    # rotation=90,
# disp = ili9341.ILI9341(spi,                   # 2.2", 2.4", 2.8", 3.2" ILI9341
    # rotation=90,
# disp = hx8357.HX8357(spi,                     # 3.5" HX8357
    # rotation=180,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

# Input pins:
button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT

button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT

button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT

button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT

button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT

button_C = DigitalInOut(board.D4)
button_C.direction = Direction.INPUT

# Turn on the Backlight
backlight = DigitalInOut(board.D26)
backlight.switch_to_output()
backlight.value = True

# Create RGB blank image for full color drawing.
if disp.rotation % 180 == 90: # if in portrait mode
    height = disp.width  # swap height/width to rotate it to landscape
    width = disp.height
else:
    width = disp.width
    height = disp.height
image = Image.new("RGB", (width, height))

# QR Code Generation
qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=4,
)
qr.add_data('testcode')
qr.make()
img_qr = qr.make_image().convert('RGB')

# Scale the QR image to screen dimension
image_ratio = img_qr.width / img_qr.height
screen_ratio = width / height
if screen_ratio < image_ratio:
    scaled_width = img_qr.width * height // img_qr.height
    scaled_height = height
else:
    scaled_width = width
    scaled_height = img_qr.height * width // img_qr.width
img_qr = img_qr.resize((scaled_width, scaled_height), Image.BICUBIC)

# Crop and center the image
x = scaled_width // 2 - width // 2
y = scaled_height // 2 - height // 2
img_qr = img_qr.crop((x, y, x + width, y + height))

# IP Address
cmd = "hostname -I | cut -d' ' -f1"
IP = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")

# Disk Usage 
cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")

# Make sure the .ttf font file is in the same directory as script.
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

while True:
    # Draw a black filled box to clear the screen.
    draw.rectangle((0, 0, width, height), outline=0, fill=(0,0,0))

    # if not button_U.value:  # up pressed
        # doSomething()
    # else:
        # doSomethingElse() # up

    # if not button_D.value:  # down pressed
        # doSomething()
    # else:
        # doSomethingElse() # down

    # if not button_L.value:  # left pressed
        # doSomething()
    # else:
        # doSomethingElse() # left

    # if not button_R.value:  # right pressed
        # doSomething()
    # else:
        # doSomethingElse() # right

    while not button_C.value:  # center pressed
        # Show QR Code for Test Address
        disp.image(img_qr)  # center

    QuitText = ""
    A_fill = 0
    if not button_A.value:  # A button pressed
        A_fill = "#FF0000"
        QuitText = "Hold A and B together to quit."
        
    draw.ellipse((140, 190, 180, 230), outline="#FFFFFF", fill=A_fill)  # A

    B_fill = 0
    if not button_B.value:  # B button pressed
        B_fill = "#FF0000"
        QuitText = "Hold A and B together to quit."
    draw.ellipse((190, 175, 230, 215), outline="#FFFFFF", fill=B_fill)  # B

    # Quit
    if not (button_A.value or button_B.value):  # A and B buttons held together
        # Draw a red filled box as the background
        draw.rectangle((0, 0, width, height), fill=(204,0,0))

        # Draw a smaller inner darker shade rectangle
        draw.rectangle((20, 20, width-20, height-20), fill=(102, 0, 0))
        
        # Draw Some Text
        text = "Quitting in 3s"
        (font_width, font_height) = font.getsize(text)
        draw.text(
            (width // 2 - font_width // 2, height // 2 - font_height // 2),
            text,
            font=font,
            fill=(255, 255, 255),
        )

        # Display the Image
        disp.image(image)

        # Wait 3 seconds
        time.sleep(3.0)
        
        # Turn off display
        backlight.value = False
        
        # Quit the program
        quit()

    # System Temp
    cmd = "cat /sys/class/thermal/thermal_zone0/temp | awk '{printf \"CPU \
          Temp: %.1f C\", $(NF-0) / 1000}'" # pylint: disable=line-too-long
    Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")
    # CPU Load
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
    # Memory Usage
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", \
          $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")

    # Write text starting at x,y
    x = 10
    y = 10
    # Display IP Address
    draw.text((x, y), IP, font=font, fill="#FFFFFF")
    y += font.getsize(IP)[1]
    # Display CPU Load
    draw.text((x, y), CPU, font=font, fill="#FFFFFF")
    y += font.getsize(CPU)[1]
    # Display Memory Usage
    draw.text((x, y), MemUsage, font=font, fill="#FFFFFF")
    y += font.getsize(MemUsage)[1]
    # Display Disk Usage
    draw.text((x, y), Disk, font=font, fill="#FFFFFF")
    y += font.getsize(Disk)[1]
    # Display System Temp
    draw.text((x, y), Temp, font=font, fill="#FFFFFF")
    y += font.getsize(Disk)[1]
    # Display Quit Text
    draw.text((x, y), QuitText, font=font, fill="#FF0000")

    # Display the Image
    disp.image(image)

    time.sleep(0.05)
