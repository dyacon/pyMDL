'''
MDL Port Configuration

'''
import subprocess

#Function for serial port configuration using GPIO
def gpioconfig(port,RSmode,duplex,resistors,bias):
    '''
    MDL serial port configuration
    port - /dev/ttyMAXn
    RSmode - 'RS485' or 'RS232'
    duplex - 'full' or 'half'
    resistors - 1 or 0
    bias - 1 or 0
    '''
    mdlportnums = {
        '/dev/ttyMAX0':0,'/dev/ttyMAX1':1,
        '/dev/ttyMAX2':2,'/dev/ttyMAX3':3,
        '/dev/ttyMAX4':4,'/dev/ttyMAX5':5,
        '/dev/ttyMAX6':6,'/dev/ttyMAX7':7}
    RSmodes = {'RS485':1,'RS232':0}
    duplexval = {'full':0,'half':1}
    gpiopins = [0,1,2,3]

    portnum = mdlportnums[port]

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

def configUpdate(config):
    '''
    Update config data structure to match MDL
    - config - Loaded YAML
    '''
    #Constants
    mdlports = {'SM1':'/dev/ttyMAX0','SM2':'/dev/ttyMAX1','SM3':'/dev/ttyMAX2',
                'SM4':'/dev/ttyMAX3','SM5':'/dev/ttyMAX4','SM6':'/dev/ttyMAX5',
                'SM7':'/dev/ttyMAX6','SM8':'/dev/ttyMAX7'}
   

    #Change port on each sensor
    sensors = config['sensors']
    for sensor in sensors:
        port = sensor['settings']['port']

        #Change port for DataBear modbus
        sensor['settings']['port'] = mdlports[port]
    
    return config

        