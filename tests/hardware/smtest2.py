'''
Testing Serial Module Ports
Version 2 - Full duplex to multiple ports
Setup:
Create "loopbacks".

Algorithm:
- import modules: serial
- configure gpio on all ports to RS485
- send test message on all ports sequentially
- verify test message received on all ports sequentially
- display results

'''
import serial
import subprocess
import time

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

#smports = ['SM1','SM2','SM3','SM4','SM5','SM6','SM7','SM8']
#smports = ['SM2','SM7']
smports = ['SM1','SM4','SM8']
#portnames = {'SM2':'/dev/ttyMAX1','SM7':'/dev/ttyMAX6'}
portnames = {
    'SM1':'/dev/ttyMAX0',
    'SM2':'/dev/ttyMAX1',
    'SM3':'/dev/ttyMAX2',
    'SM4':'/dev/ttyMAX3',
    'SM5':'/dev/ttyMAX4',
    'SM6':'/dev/ttyMAX5',
    'SM7':'/dev/ttyMAX6',
    'SM8':'/dev/ttyMAX7',
}
for port in smports:
    gpioconfig(portnames[port],'RS485','full',0,0)

#Create a connection on all ports
smconns = {}
#Set up all port connections
for port in smports:
    comm = serial.Serial(
        portnames[port],
        19200,
        timeout=0
    )
    smconns[port] = comm

def sendmsg(port):
    '''
    Send hello message from port
    '''
    msg = 'hello from {}'.format(port)
    sbytes = smconns[port].write(msg.encode('utf-8'))
    print('{} sent {} bytes'.format(port,sbytes))

def readmsg(port):
    '''
    Receive a message on a port
    '''
    dbytes = smconns[port].in_waiting
    rmsg = smconns[port].read(dbytes).decode('utf-8')
    print('Port: {} received message: {}'.format(port,rmsg))

#Testing
sendmsg('SM1')
time.sleep(1)
readmsg('SM4')
readmsg('SM8')




