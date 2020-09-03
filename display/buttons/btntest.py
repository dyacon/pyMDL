'''
Test button inputs on MDL
- Displays which botton is pressed on the display

https://www.kernel.org/doc/Documentation/input/input.txt

struct input_event {
	struct timeval time;
	unsigned short type;
	unsigned short code;
	unsigned int value;
};

Python unpacking: Read 16 bytes, struct.unpack('2IHHI')
'''
import struct
from PIL import Image, ImageDraw, ImageFont

#Open event file
f = open('/dev/input/event0','rb')

#Set up image
image = Image.new('1',(128,64),color=0)
fnt = ImageFont.truetype(
            '/usr/share/fonts/liberation/LiberationMono-Regular.ttf',10)
draw = ImageDraw.Draw(image)

#Button map
btntype = {28:'Select',1:'Cancel',103:'Up',108:'Down'}

while 1:
    #Read in data and print result to screen
    data = f.read(16)
    button = struct.unpack('2IHHI',data)
    print(button)

    #Display button on screen IF pushed AND released
    # button = (time1, time2, type, code, value)
    if (button[3] in [28,1,103,108]) and (button[4]==0):
        disp = btntype[button[3]]
        
        #Clear display
        draw.rectangle([(0,0),(128,64)],fill=0)

        #Draw button
        draw.text((20,20),btntype[button[3]],font=fnt,fill=255)

        imbytes = image.tobytes()
        #print(imbytes)

        with open('/dev/fb0','wb') as fimg:
            fimg.write(imbytes)
    


