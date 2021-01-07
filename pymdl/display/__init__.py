'''
MDL Display App
Displays status and data from databear.
- Must test on MDL
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
sleepSeconds = 10
mdlfont = ImageFont.load_default()  #Font to use

#Set up connection to databear
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.settimeout(1)
HOST = 'localhost'
PORT = 62000

class system_display:
    '''
    A class that describes the system
    page
    '''
    font = mdlfont
    def __init__(self):
        self.dbstatus = 'Not running'
        self.sensors = []
        self.getstatus()

    def getstatus(self):
        '''
        Get status of databear
        '''
        cmd = json.dumps({'command':'status'})
        #Try to connect and send
        try:
            sock.sendto(cmd.encode('utf-8'),(HOST,PORT))
            response = sock.recv(1024)
        except socket.timeout:
            return

        #Send command
        status = json.loads(response.decode('utf-8'))
        self.dbstatus = status['status']
        self.sensors = status['sensors']
        
    def renderPage(self):
        '''
        Generate a PIL image of the system status page
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

        statstr = ('DataBear: {}\n'
                   'Battery:  XXV\n'
                   'No problems detected'.format(self.dbstatus))

        d.multiline_text(
                (0,0),
                headerstr,
                font=self.font,
                fill=255,
                spacing=2)

        d.multiline_text(
                (0,25),
                statstr,
                font=self.font,
                fill=255,
                spacing=2)
        d.line([(5,24),(40,24)],width=1,fill=255)

        return im

class sensor_display:
    '''
    A class that describes a sensor display
    '''
    font = mdlfont
    def __init__(self,sensorname):
        self.name = sensorname
        self.measurements = []
        self.units = {}
        self.data = {}
        self.getmeta()

    def getmeta(self):
        '''
        Get sensor metadata
        '''
        cmd = json.dumps({'command':'getsensor','arg':self.name})
        #Try to connect and send
        try:
            sock.sendto(cmd.encode('utf-8'),(HOST,PORT))
            response = sock.recv(1024).decode('utf-8')
        except socket.timeout:
            return

        #Send command
        meta = json.loads(response)
        for m in meta['measurements']:
            self.measurements.append(m[0])
            self.units[m[0]] = m[1]

    def getdata(self):
        '''
        Get current sensor data
        '''
        cmd = json.dumps({'command':'getdata','arg':self.name})
        #Try to connect and send
        try:
            sock.sendto(cmd.encode('utf-8'),(HOST,PORT))
            response = sock.recv(1024).decode('utf-8')
        except socket.timeout:
            return

        #Store current data
        self.data = json.loads(response)

    def renderPage(self):
        '''
        Generate a page for the current data
        
        Returns
        - PIL image (not bytes) so that function can be unit tested.
        '''
        #Create image
        im = Image.new('1',(128,64),color=0)
        d = ImageDraw.Draw(im)

        #Extract the measurement time from first measurement
        mtime = self.data[self.measurements[0]][0]

        #Display content
        headstr = '{}      {}'.format(self.name,mtime)
        datastr = ''
        for m in self.measurements:
            datastr = datastr + '{}:   {} {}\n'.format(m,self.data[m],self.units[m])

        d.text((0,0),headstr,font=font,fill=255)
        d.multiline_text(
                (20,20),
                datastr,
                font=font,
                fill=255,
                spacing=2)

        #Draw a rectangle to indicate more data
        d.polygon([(50,110),(50,120),(55,105)],fill=255)

        return im

# Add any pages we want to switch between here for easy 
# selecting between later
class Page(Enum):
    System = 0
    Data = 1

def clearDisplay():
    '''
    Create an all 0 image to clear display
    '''
    im = Image.new('1',(128,64),color=0)
    return im.tobytes()

def run():
    '''
    Initializes pages based on settings
    sent by databear
    Main Loop:
    1. Wait for button to wake from sleep
    2. Check page setting: system vs sensor data
    3. Display page 
        - if system, display system page
        - if data, display data page
    3. Check for button press
        - switch page setting to display if down arrow
        - switch page setting to system if up arrow
    4. Break loop if Ctl-C
    '''
    #Initialize system display
    system = system_display()
    total_pages = 0 #**Hardcoded for testing

    #Create a data display for each sensor
    sensorpages = []
    for sensor in system.sensors:
        sensorpage = sensor_display(sensor)
        sensorpage.getmeta() #Load metadata
        sensorpages.append(sensorpage)

    #Initial settings:
    currentPage = Page.System
    sleeping = True
    lastButtonTime = 0.0
    sensorpagenum = 0

    #Initialize button objects
    btnObj = open('/dev/input/event0','rb')
    btntype = {28:'Select',1:'Cancel',103:'Up',108:'Down'}

    #Create a selector object and register button
    sel = selectors.DefaultSelector()
    sel.register(btnObj,selectors.EVENT_READ)

    while True:

        # Generate image but only if awake
        if not sleeping:
            if currentPage == Page.System:
                img = system.renderPage()
            elif currentPage == Page.Data:
                img = sensorpages[sensorpagenum].renderPage()
        
            with open('/dev/fb0','wb') as f:
                f.write(img.tobytes())

        #Check for input
        event = sel.select(timeout=0)
        if event:
            #Read in button press
            data = btnObj.read(16)
            button = struct.unpack('2IHHI',data)

            #Interpret button press
            if (button[3] in [28,1,103,108]) and (button[4]==0):
                # Any key release turns off sleeping and sets last event time
                sleeping = False
                lastButtonTime = time.time()
                if btntype[button[3]]=='Up':
                    #Up button
                    currentPage = currentPage - 1
                elif btntype[button[3]]=='Down':
                    currentPage = currentPage + 1
                else:
                    pass

                #Check if at first or last page
                #If at first don't go up, at last circle back to first
                if (currentPage < 0) or (currentPage > total_pages):
                    currentPage = 0
    
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
    #run()
    #systemdisp = system_display()
    testsensor = sensor_display('tph1')
    






