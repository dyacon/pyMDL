'''
Testing pillow text
'''

from PIL import Image, ImageDraw, ImageFont

im = Image.new('1',(500,500),color=255)

fnt = ImageFont.truetype('arial.ttf',15)
d = ImageDraw.Draw(im)
d.text((20,20),'Hello World',font=fnt)

im.show()