'''
MDL-700 Datalogger
Measure with Dyacon TPH1 and WSD1 as defined in DataBear

'''

#Import databear components
from databear.sensors import dyaconTPH1,dyaconWSD2 
from databear import logger,sensorfactory

#Import MDL functions
from pymdl import mdl_functions

#Import other libraries
import sys
import yaml

#Register project sensors with sensor factory
#   register_sensor(<sensortype>,<sensorclass>)
#The sensortype string should match the sensortype specified in the yaml
#Example: sensorfactory.factory.register_sensor('simStream', simStream.SimStream)
sensorfactory.factory.register_sensor('dyaconTPH', dyaconTPH1.dyaconTPH)

#Read in path to YAML from commandline arg
if len(sys.argv) < 2:
        print('Enter path to config file from current directory')
        exit(0)

configpath = sys.argv[1]

#Import config file
with open(configpath,'rt') as yin:
    configyaml = yin.read()

config = yaml.safe_load(configyaml)

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
