'''
MDL-700 Datalogger

- Uses Databear for logger functionality
- Configures serial ports
- Defines new measurement methods
'''

import subprocess

#Function for serial port configuration using GPIO
def portconfig(portnum,RSmode,duplex,resistors,bias):
    '''
    MDL serial port configuration
    portnum - <int> serial port 1-8
    RSmode - 'RS485' or 'RS232'
    duplex - 'full' or 'half'
    resistors - 1 or 0
    bias - 1 or 0
    '''
    RSmodes = {'RS485':1,'RS232':0}
    duplexval = {'full':1,'half':0}
    gpiopins = [0,4,8,12]

    if (portnum >= 1) and (portnum <=4):
        gpiochip = 'gpiochip1'
        gpiopins = [x+(portnum-1) for x in gpiopins]
    elif (portnum >= 5) and (portnum <=8):
        gpiochip = 'gpiochip2'
        gpiopins = [x+(portnum-5) for x in gpiopins]
    else:
        print('error')

    RSset = '{}={}'.format(gpiopins[0],RSmodes[RSmode])
    duplexset = '{}={}'.format(gpiopins[1],duplexval[duplex])
    resistset = '{}={}'.format(gpiopins[2],resistors)
    biaset = '{}={}'.format(gpiopins[3],bias)

    gpiocmd = 'gpioset {} {} {} {} {}'.format(
        gpiochip,RSset,duplexset,resistset,biaset)
    
    print(gpiocmd)

#Serial port settings
portconfig(2,'RS485','half',1,1)
portconfig(5,'RS232','full',0,1)