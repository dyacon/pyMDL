'''
A databear API simulator
Use to develop the display without running databear
'''

import threading
import socket
import selectors
import json


class simAPI:
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
        while True:
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

    def getResponse(self,cmd,args):
        '''
        Generate response for a particular command and argument
        Commands
            - status
            - getdata
        '''
        if cmd == 'status':
            response = {
                'status':'running',
                'sensors':['tph1','wsd1']
            }
        elif cmd == 'getdata':
            response = {
                'data':('2020-12-01',55.2),
                'units':'test'
            }
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



