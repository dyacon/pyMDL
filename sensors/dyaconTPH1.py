'''
Dyacon TPH-1 Sensor
This version creates a display on the MDL
- Platform: MDL
- Connection: Serial Port Module
- Interface: DataBear Sensor Interface V0.1

'''

import datetime
import minimalmodbus as mm
from databear.errors import MeasureError, SensorConfigError
from PIL import Image, ImageDraw, ImageFont

class tphdisplay:
    '''
    Creates a display on the MDL for tph
    '''
    def __init__(self):
        '''
        Set up basic image
        '''
        self.image = Image.new('1',(128,64),color=0)
        self.font = ImageFont.truetype(
            '/usr/share/fonts/liberation/LiberationMono-Regular.ttf',10)
        self.draw = ImageDraw.Draw(self.image)

    def displaydata(self,dt,airT,rh,bp):
        dispstr = ('Dyacon TPH-1\n'
                   'Air T:  {0:%H:%M:%S} {1:.2f}\n'
                   'RH:     {0:%H:%M:%S} {2:.1f}\n'
                   'BP:     {0:%H:%M:%S} {3:.1f}\n'.format(dt,airT,rh,bp)
                   )
        
        #Clear display
        self.draw.rectangle([(0,0),(128,64)],fill=0)
        
        self.draw.multiline_text(
            (0,0),
            dispstr,
            font=self.font,
            fill=255,
            spacing=2
        )

        imbytes = self.image.tobytes()

        with open('/dev/fb0','wb') as f:
            f.write(imbytes)



class dyaconTPH:
    #Inherit from "modbus sensor class"?
    def __init__(self,name,settings):
        '''
        Create a new Dyacon TPH sensor
        Inputs
            - Name for sensor
            - settings['serialnum'] = Serial Number
            - settings['port'] = Serial com port
            - settings['address'] = Sensor modbus address
        '''
        try:
            self.name = name
            self.sn = settings['serialnumber']
            self.port = settings['port']
            self.address = settings['address']
            self.frequency = settings['measurement']
        except KeyError as ke:
            raise SensorConfigError('YAML missing required sensor setting')

        #Serial settings
        self.rs = 'RS485'
        self.duplex = 'half'
        self.resistors = 1
        self.bias = 1

        #Define characteristics of this sensor
        self.sensor_type = 'polled'
        self.maxfrequency = 1  #Maximum frequency in seconds the sensor can be polled

        #Define measurements
        airT = {'name':'airT','register':210,'regtype':'float'}
        rh = {'name':'rh','register':212,'regtype':'float'}
        bp = {'name':'bp','register':214,'regtype':'float'}
        self.measurements = [airT,rh,bp]

        #Setup measurement
        self.comm = mm.Instrument(self.port,self.address)
        self.comm.serial.timeout = 0.3

        #Initialize data structure
        self.data = {'airT':[],'rh':[],'bp':[]} #Empty data dictionary

        #Display
        self.display = tphdisplay()

    def measure(self):
        '''
        Read in data using modbus
        '''
        fails = {} #keep track of measurement failures
        vals = [] #keep track of values for display
        for measure in self.measurements:
            dt = datetime.datetime.now()
            timestamp = dt.strftime('%Y-%m-%d %H:%M:%S %f')
            
            try:
                val = self.comm.read_float(measure['register'])
                self.data[measure['name']].append((dt,val))
                vals.append(val)

            except mm.NoResponseError as norsp:
                fails[measure['name']] = 'No response from sensor'
        
        #Display data on MDL
        self.display.displaydata(dt,vals[0],vals[1],vals[2])
        
        #Raise a measurement error if a fail is detected
        if len(fails)>0:
            failnames = list(fails.keys())
            raise MeasureError(failnames,fails)

    def getdata(self,name,startdt,enddt):
        '''
        Return a list of values such that
        startdt <= timestamps < enddt
        - Inputs: datetime objects
        '''
        output = []
        data = self.data[name]
        for val in data:
            if (val[0]>=startdt) and (val[0]<enddt):
                output.append(val)
        return output


    def cleardata(self,name,startdt,enddt):
        '''
        Clear data values for a particular measurement
        Loop through values and remove. Note: This is probably
        inefficient if the data structure is large.
        '''
        savedata = []
        data = self.data[name]
        for val in data:
            if (val[0]<startdt) or (val[0]>=enddt):
                savedata.append(val)

        self.data[name] = savedata
