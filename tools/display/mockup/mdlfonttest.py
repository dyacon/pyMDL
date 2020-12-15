'''
Test different fonts on the MDL
'''

from PIL import Image, ImageDraw, ImageFont
import sys

#Read in command line args
if len(sys.argv) <= 1:
    fontselect = 'cherry-10-r'
else:
    fontselect = sys.argv[1] 

im = Image.new('1',(128,64),color=0)
d = ImageDraw.Draw(im)

testfont = ImageFont.load(fontselect)
dfnt = ImageFont.load_default()

#Clear image
d.rectangle([(0,0),(128,64)],fill=0,outline=255)

#Display content
teststr1 = 'ABCefg 01238 GHIjkl 56789'
teststr2 = 'mnOPqRs TuvwXYZ'

d.text((0,0),teststr1,font=testfont,fill=255)
d.text((0,15),teststr2,font=testfont,fill=255)
d.text((0,30),teststr1,font=dfnt,fill=255)
d.text((0,45),teststr2,font=dfnt,fill=255)

imbytes = im.tobytes()

with open('/dev/fb0','wb') as f:
    f.write(imbytes)
