'''
Testing Serial Module Ports
Setup:
Create "loopbacks". Connect ports 1-4 to 5-8 using RS485

Algorithm:
- import modules: serial
- configure gpio on all ports to RS485
- send test message on all ports sequentially
- verify test message received on all ports sequentially
- display results

'''
import serial

#Configure all GPIO
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

smports = ['SM1','SM2','SM3','SM4','SM5','SM6','SM7','SM8']
for port in smports:
    gpioconfig(port,'RS485',0,0)

#Create a connection on all ports
portnames = [
    '/dev/ttyMAX0',
    '/dev/ttyMAX1',
    '/dev/ttyMAX2',
    '/dev/ttyMAX3',
    '/dev/ttyMAX4',
    '/dev/ttyMAX5',
    '/dev/ttyMAX6',
    '/dev/ttyMAX7',
]
smconns = []
for port in portnames:
    smconns.append(serial.serial(port,...))

#Send and recieve on all ports
#Need to send from all before checking recieve on all
for port in portnames:
    serial.send('XXX')

#Read in and verify correct
for port in portnames:
    serial.receive('XXX')
    if correctdata:
        print('port sm... = pass')



