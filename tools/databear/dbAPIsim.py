'''
A databear API simulator
Use to develop the display without running databear
'''

import threading
import socket
import selectors
import json


class simAPI:

    #Define dummy sensors
    sensors = ['tph1','wsd1']
    measurements = {
        'tph1':[
            ('air_temperature','C'),
            ('relative_humidity','%'),
            ('barometric_pressure','mb')
            ],
        'wsd1':[
            ('speed','m/s'),
            ('direction','degrees'),
            ('speed_2m','m/s'),
            ('direction_2m','degrees'),
            ('speed_10m','m/s'),
            ('direction_10m','degrees')
            ]
        }
    data_tph = {
        'air_temperature':('2020-12-17 11:05',34.33),
        'relative_humidity':('2020-12-17 11:05',15),
        'barometric_pressure':('2020-12-17 11:05',800.55)
    }
    data_wind = {
        'speed':('2020-12-17 11:10',22),
        'direction':('2020-12-17 11:10',150),
        'speed_2m':('2020-12-17 11:10',22),
        'direction_2m':('2020-12-17 11:10',150),
        'speed_10m':('2020-12-17 11:10',22),
        'direction_10m':('2020-12-17 11:10',150)
        }
    data = {'tph1':data_tph,'wsd1':data_wind}
    runflag = True


    def __init__(self):
        #Set up socket and select
        self.udpsocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.udpsocket.bind(('localhost',62000))
        self.udpsocket.setblocking(False)
        self.sel = selectors.DefaultSelector()
        self.sel.register(self.udpsocket,selectors.EVENT_READ)
        self.listen = True #A flag to determine when to stop

    def listenUDP(self):
        '''
        Listen on UDP socket
        '''
        while self.runflag:
            try:
                #Check for UDP comm
                event = self.sel.select(timeout=1)
                if event:
                    self.readUDP()
            except KeyboardInterrupt:
                self.udpsocket.close()
                break

    def readUDP(self):
        '''
        Read message, respond, add any messages
        to the message queue
        Message should be JSON
        {'command': <cmd> , 'arg': <optional argument>}
        '''
        msgraw, address = self.udpsocket.recvfrom(1024)

        #Decode message
        msg = json.loads(msgraw)

        #Respond
        response = self.getResponse(msg['command'],msg.get('arg',None))
            
        #Send a response
        self.udpsocket.sendto(json.dumps(response).encode('utf-8'),address)

    def getResponse(self,cmd,arg):
        '''
        Generate response for a particular command and argument
        Commands
            - status
            - getdata
        '''
        if cmd == 'status':
            response = {
                'status':'running',
                'sensors':self.sensors,
            }
        elif cmd == 'getsensor':
            response = {
                'measurements':self.measurements[arg]
            }

        elif cmd == 'getdata':
            response = self.data[arg]
        elif cmd == 'shutdown':
            response = {'response':'OK'}
            self.runflag = False
        else:
            response = {'error':'Invalid Command'}
        
        return response

if __name__ == "__main__":
    '''
    Run the simulator
    '''
    #Instantiate API
    api = simAPI()
    
    #Start listening
    api.listenUDP()
    print('Shutting down')



