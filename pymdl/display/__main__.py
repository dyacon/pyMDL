'''
MDL Display App
Displays status and data from databear.
- Must test on MDL
'''

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from enum import Enum
import importlib.resources as pkg_resource
import struct
import selectors
import socket
import time
import json

#Run parameters
sleepSeconds = 10
with pkg_resource.path('pymdl.fonts','cherry-11-r.pil') as fntpath:
    mdlfont = ImageFont.load(fntpath)

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
        self.dbstatus = 'DataBear Inactive'
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
        headerstr = ('MDL-700     {}\n'.format(timestr))

        statstr = ('IP: 225.252.255.255\n'
                   'Status:\n'
                   '{}\n'.format(self.dbstatus))

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
        # print("self.measurements: {}".format(json.dumps(self.measurements)))
        # print("self.data: {}".format(json.dumps(self.data)))
        # print("self.units: {}".format(json.dumps(self.units)))
        if self.data[self.measurements[0]]:
            mtime = self.data[self.measurements[0]][0]
        else:
            mtime = "2020-03-03 03:03"

        #Display content
        headstr = '{}      {}'.format(self.name,mtime[-5:])
        datastr = ''
        for m in self.measurements:
            # print("Adding measurement {}".format(m))
            if m in self.data and self.data[m] and m in self.units:
                datastr = datastr + '{}:   {} {}\n'.format(m,self.data[m][1],self.units[m])
            else:
                datastr = datastr + '{}: missing data'.format(m)

        d.text((0,0),headstr,font=self.font,fill=255)
        d.multiline_text(
                (20,20),
                datastr,
                font=self.font,
                fill=255,
                spacing=2)

        #Draw a rectangle to indicate more data
        d.polygon([(50,110),(50,120),(55,105)],fill=255)

        return im

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
    maxpageindex = len(system.sensors)
    print('maxpageindex is ' + str(maxpageindex))

    #Create a data display for each sensor
    sensorpages = []
    for sensor in system.sensors:
        sensorpage = sensor_display(sensor)
        sensorpages.append(sensorpage)

    #Initial settings:
    currentPage = 0
    sleeping = True
    lastButtonTime = 0.0

    #Initialize button objects
    btnObj = open('/dev/input/event0','rb')
    btntype = {28:'Select',1:'Cancel',103:'Up',108:'Down'}

    #Create a selector object and register button
    sel = selectors.DefaultSelector()
    sel.register(btnObj,selectors.EVENT_READ)

    while True:

        #Check for input
        event = sel.select(timeout=0)
        if event:
            print('event detected')
            lastButtonTime = time.time()
            
            #Read in button type
            data = btnObj.read(16)
            button = struct.unpack('2IHHI',data)
            print(button)

            #Read in SYN message?
            data = btnObj.read(16)
            syn = struct.unpack('2IHHI',data)
            print(syn)

            #Interpret button press, respond to push not release
            if (button[3] in [28,1,103,108]) and (button[4]==1):
                print('button release')      
                #Wake up on button release if sleeping
                if sleeping:
                    print('wake up')
                    sleeping=False
                    #Always start at the system page
                    currentPage=0
                else:
                    #Interpret button press
                    if btntype[button[3]]=='Up':
                        #Up button
                        currentPage = currentPage - 1
                        print('Up: page = {}'.format(currentPage))
                    elif btntype[button[3]]=='Down':
                        currentPage = currentPage + 1
                        print('Down: page = {}'.format(currentPage))
                    else:
                        pass
            
                #Check if at first or last page
                #If at first don't go up, at last circle back to first
                if (currentPage < 0) or (currentPage > maxpageindex):
                    print('reset currentpage')
                    currentPage = 0

            
        #Generate image if awake
        if not sleeping:
            if currentPage == 0:
                img = system.renderPage()
            else:
                sensorpages[currentPage-1].getdata()
                img = sensorpages[currentPage-1].renderPage()
        
            with open('/dev/fb0','wb') as f:
                f.write(img.tobytes())
            
        # If the last button press was more than sleepSeconds seconds ago,
        # go back to sleep
        if not sleeping and (time.time() - lastButtonTime) > sleepSeconds:
            print('No button press for over ' + str(sleepSeconds) + 
                ' seconds, clearing display')
            sleeping = True

            imbytes = clearDisplay()

            with open('/dev/fb0','wb') as f:
                f.write(imbytes)

        #Sleep 1s between cycles
        time.sleep(1)

if __name__ == "__main__":
    run()
    






