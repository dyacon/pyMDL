'''
Testing pillow text
'''

from PIL import Image, ImageDraw, ImageFont

im = Image.new('1',(128,64),color=0)

fnt = ImageFont.truetype(
    '/usr/share/fonts/liberation/LiberationMono-Regular.ttf',10)
fnt2 = ImageFont.load_default()
d = ImageDraw.Draw(im)
#d.rectangle([(0,0),(50,30)],outline=255,fill=255)
d.multiline_text(
        (0,0),
        'Hello World - \n 1,2,3,4,5 \n ABC abc',
        font=fnt,
        fill=255,
        spacing=2)

d.text((0,40),'Hello World',font=fnt2,fill=255)

imbytes = im.tobytes()

with open('/dev/fb0','wb') as f:
    f.write(imbytes)
