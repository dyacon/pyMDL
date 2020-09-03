'''
Testing the Python "selectors" module
https://docs.python.org/3/library/selectors.html#module-selectors
Use on the MDL
'''

import selectors
import time
import struct

#Open the device file
btnObj = open('/dev/input/event0','rb')

#Create a selector object and register button
sel = selectors.DefaultSelector()
sel.register(btnObj,selectors.EVENT_READ)

#Loop checking for button presses
btntype = {28:'Select',1:'Cancel',103:'Up',108:'Down',0:'SYN'}
while True:
    print('Check for button')
    event = sel.select(timeout=0)
    if event:
        print('Event Detected')
        print(event)
        #Read in button press
        data = btnObj.read(16)
        button = struct.unpack('2IHHI',data)
        print('Button = {}'.format(btntype[button[3]]))
    else:
        print('No event detected')
    time.sleep(1)