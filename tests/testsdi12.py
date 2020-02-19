#Test Dyacon WSD2 sensor 

from databear import sensorfactory
from databear import logger
from databear.sensors import dyaconWSD2


sensorfactory.factory.register_sensor('dyaconWSD2', dyaconWSD2.dyaconWSD2)

datalogger = logger.DataLogger('testsdi12')

#Sensor settings
wsdsettings = {
    'serialnumber':555,
    'port':'/dev/ttyMAX3',
    'address':'0',
    'measurement':10
}

datalogger.addSensor('dyaconWSD2','mywsd',wsdsettings)

datalogger.scheduleMeasurement('mywsd',5)

datalogger.scheduleStorage('speed','mywsd',30)
datalogger.scheduleStorage('direction','mywsd',30)

#datalogger.run()
