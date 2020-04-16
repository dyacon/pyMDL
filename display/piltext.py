'''
Testing pillow text
'''

from PIL import Image, ImageDraw, ImageFont

im = Image.new('1',(128,64),color=0)

fnt = ImageFont.truetype(
    '/usr/share/fonts/liberation/LiberationMono-Regular.ttf',15)
d = ImageDraw.Draw(im)
d.text((20,20),'Hello World',font=fnt,fill=255)

imbytes = im.tobytes()

with open('/dev/fb0','wb') as f:
    f.write(imbytes)