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
# import pyqrcode
# import png
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
# disp = st7789.ST7789(spi, rotation=90,							# 2.0" ST7789
# disp = st7789.ST7789(spi, rotation=90, width=135, height=240, x_offset=53, y_offset=40, # 1.14" ST7789
disp = st7789.ST7789(spi, rotation=180, height=240, y_offset=80,	# 1.3", 1.54" ST7789
# disp = ili9341.ILI9341(spi, rotation=90,						  # 2.2", 2.4", 2.8", 3.2" ILI9341
# disp = hx8357.HX8357(spi, rotation=180,						   # 3.5" HX8357
# disp = st7735.ST7735R(spi, rotation=90,						   # 1.8" ST7735R
# disp = st7735.ST7735R(spi, rotation=270, height=128, x_offset=2, y_offset=3,   # 1.44" ST7735R
# disp = st7735.ST7735R(spi, rotation=90, bgr=True,				 # 0.96" MiniTFT ST7735R
# disp = ssd1351.SSD1351(spi, rotation=180,						 # 1.5" SSD1351
# disp = ssd1351.SSD1351(spi, height=96, y_offset=32, rotation=180, # 1.27" SSD1351
# disp = ssd1331.SSD1331(spi, rotation=180,						 # 0.96" SSD1331
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

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
if disp.rotation % 180 == 90:
	height = disp.width  # we swap height/width to rotate it to landscape!
	width = disp.height
else:
	width = disp.width  # we swap height/width to rotate it to landscape!
	height = disp.height
 
# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)

# Get drawing object to draw on image.
image = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(image)

#QR Code Generation
qr = qrcode.QRCode(box_size=10)
qr.add_data('testcode')
qr.make()
img_qr = qr.make_image().convert('RGB')

# Scale the image to the smaller screen dimension
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

button_fill = "#FF00FF"
button_outline = "#FFFFFF"

fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)

while True:
	# Draw a black filled box to clear the image.
	draw.rectangle((0, 0, width, height), outline=0, fill=(0,0,0))

	if not button_U.value:  # up pressed
		cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf \"CPU Temp: %.1f C\", $(NF-0) / 1000}'"  # pylint: disable=line-too-long
		Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")
	else:
		Temp = ""  # up

	if not button_D.value:  # down pressed
		cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
		CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
	else:
		CPU = ""  # down

	if not button_L.value:  # left pressed
		cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
		MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
	else:
		MemUsage = ""  # left

	if not button_R.value:  # right pressed
		cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
		Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
	else:
		Disk = ""  # right

	while not button_C.value:  # center pressed
		#Show QR Code for Test Address
		disp.image(img_qr) #center

	A_fill = 0
	if not button_A.value:  # A button pressed
		A_fill = button_fill
	draw.ellipse((140, 80, 180, 120), outline=button_outline, fill=A_fill)  # A button

	if not button_B.value:  # B button pressed
		backlight.value = False
		quit() # B button

	# Write four lines of text starting at x,y
	x = 10
	y = 122
	# Display IP Address
	cmd = "hostname -I | cut -d' ' -f1"
	IP = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
	draw.text((x, y), IP, font=font, fill="#FFFFFF")
	y += font.getsize(IP)[1]
	# Display CPU Load
	draw.text((x, y), CPU, font=font, fill="#FFFF00")
	y += font.getsize(CPU)[1]
	# Display Memory Usage
	draw.text((x, y), MemUsage, font=font, fill="#00FF00")
	y += font.getsize(MemUsage)[1]
	# Display Disk Usage
	draw.text((x, y), Disk, font=font, fill="#0000FF")
	y += font.getsize(Disk)[1]
	# Display System Temp
	draw.text((x, y), Temp, font=font, fill="#FF00FF")

	# Display the Image
	disp.image(image)

	time.sleep(0.01)
