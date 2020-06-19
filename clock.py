##############################################################################
# | File      	:	clock.py
# | Author      :   Iain Sprouting
# | Info        :	LSLABS Clock Gen Source Code
#----------------
# |	This version:   V1.0
# | Date        :   13/06/2020
# | Info        :   First Test
###############################################################################


import board
import busio
import adafruit_si5351
i2c = busio.I2C(board.SCL, board.SDA)
si5351 = adafruit_si5351.SI5351(i2c)
import SSD1306
from PIL import Image,ImageDraw,ImageFont
import RPi.GPIO as GPIO
import time


si5351.pll_a.configure_integer(20)
si5351.clock_0.configure_fractional(si5351.pll_a, 4, 1, 2)

print ("LSLABS CLOCK IS RUNNING ")
print('PLL A: {0} MHz'.format(si5351.pll_a.frequency/1000000))
print('Clock 0: {0} MHz'.format(si5351.clock_0.frequency/1000000))


#Okay now lets put this on the display on the unit :) 
show = SSD1306.SSD1306()

eos="|hz" #we will use this later to add on the end of the display

show.Init() #init the screen

image1 = Image.new('1', (show.width, show.height), "WHITE") #setup the first image
draw = ImageDraw.Draw(image1) #lets setup a basic draw

show.ClearBlack() #clear the screen

display_string = str(si5351.clock_0.frequency/1000000)  #take the float and convert it into a string so we can push it to the display
output = display_string[:3] + eos #the final output is the first three char of the string + the end of display we set above.


#using the draw we setup we can  draw the text using the font from the OUTPUT var we made above.
draw.text((20,0), (output), font = ImageFont.truetype('Font.tff',25), fill = 0) 

#now we can show this on the console log and push it to the screen.
print ("PUSHING CLOCK OUT TO SCREEN")
show.ShowImage(show.getbuffer(image1))


##################################################################################
# FRONT PANEL 
#
##################################################################################





#Lets setup our callbacks for our buttons 
def button_up_callback(channel):
    print("Button UP was pushed!")
    time.sleep(1)
def button_down_callback(channel):
    print("Button DOWN was pushed!")
    time.sleep(1)


#Lets setup all of our pins for buttons 
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN,pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(20,GPIO.RISING,callback=button_up_callback) # Setup event on pin 20 rising edge
GPIO.add_event_detect(21,GPIO.RISING,callback=button_down_callback) # Setup event on pin 21 rising edge

message = input("PUSH ANY KEY TO END\n\n") # Run until someone presses enter
