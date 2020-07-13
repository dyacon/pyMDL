'''
Test 3 sensors on MDL
A test of three different sensors to gage general functionality
- Dyacon TPH
- RMYoung 61302V
- simSensor

'''

#----- Import databear components ----
from databear.sensors import rmyng61302V, dyaconTPH1,simSensor
from databear import logger,sensorfactory 

#Import MDL functions
from pymdl import mdl_functions

#Import other libraries
import sys
import yaml

#-----  Register custom sensors with the sensor factory ----
#import <module containing custom sensor class>
sensorfactory.factory.register_sensor('rmyBP',rmyng61302V.rmyoungBP)
sensorfactory.factory.register_sensor('dyTPH',dyaconTPH1.dyaconTPH)
sensorfactory.factory.register_sensor('sim',simSensor.sensorSim)

#Read in path to YAML from commandline arg
if len(sys.argv) < 2:
        print('Enter path to config file from current directory')
        exit(0)

configpath = sys.argv[1]

#Import config file
with open(configpath,'rt') as yin:
    configyaml = yin.read()

config = yaml.load(configyaml)

#Update configuration for compatibility with databear
config = mdl_functions.configUpdate(config)

#Create a logger
datalogger = logger.DataLogger(config)

#Configure GPIO
for sensor in datalogger.sensors.values():
    #Get serial settings from sensor
    port = sensor.port
    rs = sensor.rs
    duplex = sensor.duplex
    resistors = sensor.resistors
    bias = sensor.bias
    #Configure port
    mdl_functions.gpioconfig(port,rs,duplex,resistors,bias)

#Run logger
datalogger.run()