'''
Display V0
Displays two pages and switches between them with buttons
-- Use on MDL
'''

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from enum import Enum
import struct
import selectors
import time

#Run parameters
# How many seconds before we go back to sleep
sleepSeconds = 10

sensorname = 'TPH-1'
sensordata = {'T':20.5667,'RH':34.223,'BP':867.2}
timestamp = '2020-05-06 12:00'
units = {'T':'C','RH':'%','BP':'mb'}
mdlfont = ImageFont.load_default()

def clearDisplay():
    '''
    Create an all 0 image to clear display
    '''
    im = Image.new('1',(128,64),color=0)
    return im.tobytes()


def displaySys():
    '''
    Create a system display
    Output - Numpy array of image
    '''
    #Get time
    dt = datetime.now()
    timestr = dt.strftime('%H:%M:%S')

    #Create image
    im = Image.new('1',(128,64),color=0)
    d = ImageDraw.Draw(im)

    #Display content
    headerstr = ('MDL-700     {}\n'
                 'Status\n'.format(timestr))

    statstr = ('DataBear: Running\n'
               'Battery:  12.35V\n'
               'No problems detected')

    d.multiline_text(
            (5,0),
            headerstr,
            font=mdlfont,
            fill=255,
            spacing=2)

    d.multiline_text(
            (5,25),
            statstr,
            font=mdlfont,
            fill=255,
            spacing=2)
    d.line([(5,24),(40,24)],width=1,fill=255)

    return im.tobytes()


def displayData(sensor,dt,data,unit):
    '''
    Display sensor data
    inputs
        - sensor - sensor name
        - dt - timestamp (string)
        - data - dictionary of sensor data
        - unit - dictionary of units
    '''
    #Create image
    im = Image.new('1',(128,64),color=0)
    d = ImageDraw.Draw(im)

    #Display content
    headstr = 'TPH-1   11:55:20'
    datastr = ('T:  25.2 C\n'
               'RH:  36 %\n'
               'BP:  890 mb\n')

    d.text((0,0),headstr,font=mdlfont,fill=255)
    d.multiline_text(
            (20,20),
            datastr,
            font=mdlfont,
            fill=255,
            spacing=2)

    #Draw a rectangle to indicate more data
    d.polygon([(50,110),(50,120),(55,105)],fill=255)

    return im.tobytes()


#Main Loop
'''
Main Loop
1. Check page setting: system vs data
2. Display page 
    - if system, display system page
    - if data, display data page
3. Check for button press
    - switch page setting to display if down arrow
    - switch page setting to system if up arrow
4. Break loop if Ctl-C
'''

# Add any pages we want to switch between here for easy selecting between later
class Page(Enum):
    System = 0
    Data = 1

# Initialize currentPage to default page to show
currentPage = Page.System

# Default to sleeping until a button is pressed to wake the display
sleeping = True
# Also initialize last button press time float
lastButtonTime = 0.0

btnObj = open('/dev/input/event0','rb')
btntype = {28:'Select',1:'Cancel',103:'Up',108:'Down'}

#Create a selector object and register button
sel = selectors.DefaultSelector()
sel.register(btnObj,selectors.EVENT_READ)

while True:

    # Generate image but only if awake
    if not sleeping:
        if currentPage == Page.System:
            imbytes = displaySys()
        elif currentPage == Page.Data:
            imbytes = displayData(0,0,0,0)
    
        with open('/dev/fb0','wb') as f:
            f.write(imbytes)

    #Check for input
    event = sel.select(timeout=0)
    if event:
        print('Event Detected')
        print(event)
        
        #Read in button press
        data = btnObj.read(16)
        button = struct.unpack('2IHHI',data)
        print(button)

        #Read remaining content from buffer
        #SYN followed by button release followed by SYN
        #data = btnObj.read(48)

        #Interpret button press
        if (button[3] in [28,1,103,108]) and (button[4]==0):
            # Any key release turns off sleeping and sets last event time
            sleeping = False
            lastButtonTime = time.time()
            if btntype[button[3]]=='Up':
                print('Up released')
                currentPage = Page.System
            elif btntype[button[3]]=='Down':
                print('Down released')
                currentPage = Page.Data
            else:
                pass
    
    # If the last button press was more than sleepSeconds seconds ago, go back to sleep
    if not sleeping and time.time() - lastButtonTime > sleepSeconds:
        print('No button press for over ' + str(sleepSeconds) + ' seconds, clearing display')
        sleeping = True

        imbytes = clearDisplay()

        with open('/dev/fb0','wb') as f:
            f.write(imbytes)

    #Sleep 0.1s because there is nothing to update
    #time.sleep(0.1)







