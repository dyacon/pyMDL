'''
Testing pillow with different fonts
'''

from PIL import Image, ImageDraw, ImageFont

im = Image.new('1',(128,64),color=0)
d = ImageDraw.Draw(im)

libm = ImageFont.truetype('LiberationMono-Regular.ttf',10)
vcr = ImageFont.truetype('VCR_OSD_MONO.ttf',10)
dfnt = ImageFont.load_default()

#Clear image
d.rectangle([(0,0),(128,64)],fill=0,outline=255)

#Display content
teststr1 = 'ABCefg 01238'
teststr2 = 'GHIJKL 56789'
teststr3 = 'abcdefghijkl'

d.text((0,0),teststr1,font=libm,fill=255)
d.text((0,20),teststr1,font=vcr,fill=255)
d.text((0,40),teststr1,font=dfnt,fill=255)

imbytes = im.tobytes()

with open('/dev/fb0','wb') as f:
    f.write(imbytes)
