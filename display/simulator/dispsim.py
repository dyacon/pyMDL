'''
Display simulator
Emulates MDL display and interactivity
'''
#%%
#Pillow components
from PIL import Image, ImageDraw, ImageFont

#Simulation components
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

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

    return np.asarray(im)

def displayData(sensor,dt,data,unit):
    '''
    Display sensor data
    inputs
        - sensor - sensor name
        - dt - timestamp (string)
        - data - dictionary of sensor data
        - unit - dictionary of units
    '''
    pass

#%%
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
while True:
    try:
        # Generate image
        if page == 'system':
            imarray = displaySys()
        elif page == 'data':
            imarray = displayData(0,0,0,0)
        
        # Display image
        plt.imshow(imarray,cmap='gray')

        #Check for button press
        #TBD

    #Break if Ctl-C
    except KeyboardInterrupt:
        break





'''
Algorithm

function displaySys
    - Get clock time
    - Generate image
    - Output array for system display

function displayData(sensor,measurements)
    - Generate image from sensor data
    - Output array of image



'''

# %%
