'''
Display test with buttons
Use on MDL
'''

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import struct

#Run parameters
sensorname = 'TPH-1'
sensordata = {'T':20.5667,'RH':34.223,'BP':867.2}
timestamp = '2020-05-06 12:00'
units = {'T':'C','RH':'%','BP':'mb'}
mdlfont = ImageFont.load_default()

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
page = 'system'
devf = open('/dev/input/event0','rb')
btntype = {28:'Select',1:'Cancel',103:'Up',108:'Down'}

while True:
    try:
        # Generate image
        if page == 'system':
            imbytes = displaySys()
        elif page == 'data':
            imbytes = displayData(0,0,0,0)
        
        with open('/dev/fb0','wb') as f:
            f.write(imbytes)

        #Read in button press
        data = devf.read(16)
        button = struct.unpack('2IHHI',data)

        #Interpret button press
        if (button[3] in [28,1,103,108]) and (button[4]==0):
            if btntype[button[3]]=='Up':
                page = 'system'
            elif btntype[button[3]]=='Down':
                page = 'data'
            else:
                pass

    #Break if Ctl-C
    except KeyboardInterrupt:
        break






