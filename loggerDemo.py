'''
Data Logger

 - Components:
    -- Measure
        - Measure each configured sensor
        - Complete measurements at sample frequency
    -- Store
        - Process the measurements: max, min, avg
        - Store data in database at storage frequency

 - General Algorithm
    1. Initialization
        - Read any configuration files
        - Initialize sensor objects for measurement
    2. Measure
        - Check clock for measure time
            - Measure sensors
            - Store values in working memory
    3. Store
        - Check clock for storage time
            - Process measurements
            - Store in database 
'''

import schedule
import time #For sleeping during execution
import sensor
import csv

#-------- Logger Initialization and Setup ------
class DataLogger:
    '''
    A data logger
    '''
    def __init__(self,logname):
        '''
        Initialize a new data logger
        Input - logname. Used with output data file
        '''
        self.name = logname
        
        self.sensors = {}
        self.measurements = [] #Form (<measurement>,<sensor>)
        self.logschedule = schedule.Scheduler()

        #Create output file
        self.csvfile = open(logname+'.csv','w',newline='')
        self.csvwrite = csv.DictWriter(self.csvfile,['dt','measurement','value','sensor'])
        self.csvwrite.writeheader()

    def addSensor(self,name,sn):
        '''
        Add a sensor to the logger
        '''
        self.sensors[name] = sensor.Sensor(name,sn)

    def addMeasurement(self,name,mtype,sensor,settings):
        '''
        Add a measurement to a sensor
        '''
        self.sensors[sensor].add_measurement(name,mtype,settings)

    def scheduleMeasurement(self,name,sensor,frequency):
        '''
        Schedule a measurement
        Frequency is seconds
        '''
        m = self.sensors[sensor].measure
        self.logschedule.every(frequency).do(m,name)
        
    def scheduleStorage(self,name,sensor,frequency):
        '''
        Schedule when storage takes place
        '''
        s = self.storeMeasurement
        self.logschedule.every(frequency).do(s,name,sensor,'sample')

    def storeMeasurement(self,name,sensor,process):
        '''
        Store measurement data according to process.
        - process is fixed at 'sample' for now.
        Deletes any unstored data.
        '''
        if not self.sensors[sensor].data[name]:
            #No data stored
            return

        if process=='sample':
            currentdata = self.sensors[sensor].data[name][-1]
            dt = currentdata[0].strftime('%Y-%m-%d %H:%M:%S:%f')
            val = currentdata[1]
            datadict = {
                    'dt':dt,
                    'measurement':name,
                    'value':val,
                    'sensor':sensor}

            #Output row to CSV
            self.csvwrite.writerow(datadict)
            

#-------- Logger initialization --------
datalogger = DataLogger('myLogger')

#Define measurement settings
airTsettings = {
    'port':'/dev/ttyMAX0',
    'address':3,
    'register':210,
    'regtype':'float',
    'timeout':0.1
}
RHsettings = {
    'port':'/dev/ttyMAX0',
    'address':3,
    'register':212,
    'regtype':'float',
    'timeout':0.1
}
RMYsettings = {
    'port':'/dev/ttyMAX5',
    'baud':9600,
    'timeout':0,
    'dataRE':r'\d\d\d\d.\d\d'
}

datalogger.addSensor('tph',6131)
datalogger.addSensor('rmy',8888)

datalogger.addMeasurement('airT','modbus','tph',airTsettings)
datalogger.addMeasurement('rh','modbus','tph',RHsettings)
datalogger.addMeasurement('bp','streaming','rmy',RMYsettings)

datalogger.scheduleMeasurement('rh','tph',5)
datalogger.scheduleMeasurement('bp','rmy',15)
datalogger.scheduleMeasurement('airT','tph',10)

datalogger.scheduleStorage('airT','tph',30)
datalogger.scheduleStorage('bp','rmy',30)


#-------- Run data logger -----------
while True:
    try:
        datalogger.logschedule.run_pending()
        sleeptime = datalogger.logschedule.idle_seconds
        if sleeptime > 0:
            time.sleep(sleeptime)

    except KeyboardInterrupt:
        break

#Shut down logger
datalogger.csvfile.close()





