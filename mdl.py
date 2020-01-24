'''
MDL-700 Datalogger

- Uses DataBear for logger functionality (pip install databear)
- Configures MDL serial ports using configuration YAML
- Optional: Define new measurement methods
'''

import databear.logger
import sys
import yaml
import subprocess #For GPIO config

#Read in path to YAML from commandline arg
if len(sys.argv) < 2:
        print('Enter path to config file from current directory')
        exit(0)

configpath = sys.argv[1]

#Import config file
with open(configpath,'rt') as yin:
    configyaml = yin.read()

config = yaml.load(configyaml)

#Function for serial port configuration using GPIO
def portconfig(portnum,RSmode,duplex,resistors,bias):
    '''
    MDL serial port configuration
    portnum - <int> serial port 0-7
    RSmode - 'RS485' or 'RS232'
    duplex - 'full' or 'half'
    resistors - 1 or 0
    bias - 1 or 0
    '''
    RSmodes = {'RS485':1,'RS232':0}
    duplexval = {'full':1,'half':0}
    gpiopins = [0,1,2,3]

    if (portnum >= 0) and (portnum <= 3):
        gpiochip = 'gpiochip1'
        gpiopins = [x + 4*portnum for x in gpiopins]
    elif (portnum >= 4) and (portnum <=7):
        gpiochip = 'gpiochip2'
        gpiopins = [x + 4*(portnum-4) for x in gpiopins]
    else:
        print('error')

    RSset = '{}={}'.format(gpiopins[0],RSmodes[RSmode])
    duplexset = '{}={}'.format(gpiopins[1],duplexval[duplex])
    resistset = '{}={}'.format(gpiopins[2],resistors)
    biaset = '{}={}'.format(gpiopins[3],bias)

    gpiocmd = 'gpioset {} {} {} {} {}'.format(
        gpiochip,RSset,duplexset,resistset,biaset)
    
    print(gpiocmd)
    subprocess.run([gpiocmd],shell=True)

#Extract serial port related settings, set GPIO, update config dict for databear
sensors = config['sensors']
mdlports = {'SM1':'/dev/ttyMAX0','SM2':'/dev/ttyMAX1','SM3':'/dev/ttyMAX2',
            'SM4':'/dev/ttyMAX3','SM5':'/dev/ttyMAX4','SM6':'/dev/ttyMAX5',
            'SM7':'/dev/ttyMAX6','SM8':'/dev/ttyMAX7'}
mdlportnums = {'SM1':0,'SM2':1,'SM3':2,
               'SM4':3,'SM5':4,'SM6':5,
               'SM7':6,'SM8':7}
for sensor in sensors:
    measurements = sensor['measurements']
    for measurement in measurements:
        #Get serial settings from dictionary
        port = measurement['port']
        serialtype = measurement['serial']
        duplex = measurement['duplex']

        #Configure GPIO - always assumes resistors and bias set
        portconfig(mdlportnums[port],serialtype,duplex,1,1)

        #Change port for DataBear modbus
        measurement['port'] = mdlports[port]

#Create a logger
datalogger = databear.logger.DataLogger(config)

#Run logger
datalogger.run()