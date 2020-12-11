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
import socket
import time
import json

#Run parameters
# How many seconds before we go back to sleep
sleepSeconds = 10
mdlfont = ImageFont.load_default()

#Sensor details - eventually pull from SQLite?
sensors = ['tph1']
measurements = {'tph1':['T','RH','BP']}
units = {'tph1':{'T':'C','RH':'%','BP':'mb'}}

#Set up connection to databear
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.settimeout(5)

def clearDisplay():
    '''
    Create an all 0 image to clear display
    '''
    im = Image.new('1',(128,64),color=0)
    return im.tobytes()

def getdata(sensorname):
    '''
    Get data for a particular sensor from databear
    Inputs
    - sensorname
    Return
    - data: {'dt':<datetime string>,'measure1':<value>,...}
    '''
    msg = {'command':'getdata','arg':sensorname}
    sock.sendto(json.dumps(msg).encode('utf-8'),('localhost',62000))
    response = sock.recv(1024)

    #Parse response
    respdict = json.loads(response)
    data = {}
    data['dt'] = respdict['data']['air_temperature'][0][-5:]
    data['T'] = respdict['data']['air_temperature'][1]
    data['RH'] = respdict['data']['relative_humidity'][1]
    data['BP'] = respdict['data']['barometric_pressure'][1]

    return data


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

    return im

def displayData(sensorname,dt,measurements,data,units):
    '''
    Display sensor data
    inputs
        - sensor - sensor name
        - dt - 'HH:mm:s'
        - measurements - a list of measurement names
        - data - dictionary of data for each measurement
        - unit - dictionary of units for each measurement
    Returns
        - PIL image (not bytes) so that function can be unit tested.
    '''
    #Create image
    im = Image.new('1',(128,64),color=0)
    d = ImageDraw.Draw(im)

    #Display content
    headstr = '{}      {}'.format(sensorname,dt)
    datastr = ''
    for m in measurements:
        datastr = datastr + '{}:   {} {}\n'.format(m,data[m],units[m])

    d.text((0,0),headstr,font=mdlfont,fill=255)
    d.multiline_text(
            (20,20),
            datastr,
            font=mdlfont,
            fill=255,
            spacing=2)

    #Draw a rectangle to indicate more data
    d.polygon([(50,110),(50,120),(55,105)],fill=255)

    return im

def run():
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
                img = displaySys()
            elif currentPage == Page.Data:
                data = getdata(sensors[0])
                img = displayData(
                    sensors[0],
                    data['dt'],
                    measurements[sensors[0]],
                    data,
                    units[sensors[0]]
                )
                
        
            with open('/dev/fb0','wb') as f:
                f.write(img.tobytes())

        #Check for input
        event = sel.select(timeout=0)
        if event:
            print('Event Detected')
            print(event)
            
            #Read in button press
            data = btnObj.read(16)
            button = struct.unpack('2IHHI',data)
            #print(button)

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
        time.sleep(0.1)

if __name__ == "__main__":
    run()





