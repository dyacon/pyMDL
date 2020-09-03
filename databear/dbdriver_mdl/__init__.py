'''
A DataBear driver for the MDL
'''
from dbdriver_mdl import portconfig

class mdldriver:
    def __init__(self):
        '''
        Create a new driver instance
        Could load a config file here...
        '''
        #Map DataBear ports to hardware ports
        self.ports = {
            'port1':'/dev/ttyMAX0',
            'port2':'/dev/ttyMAX1',
            'port3':'/dev/ttyMAX2',
            'port4':'/dev/ttyMAX3',
            'port5':'/dev/ttyMAX4',
            'port6':'/dev/ttyMAX5',
            'port7':'/dev/ttyMAX6',
            'port8':'/dev/ttyMAX7'
        }
    def connect(self,databearport):
        '''
        Configure hardware port and return name
        '''
        mdlport = self.ports[databearport]
        portconfig.gpioconfig(mdlport,'RS485','half',1,1)
        #Wait for configuration?
        return mdlport

