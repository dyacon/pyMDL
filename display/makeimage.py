'''
Testing pillow
- Create a small image
'''

from PIL import Image, ImageDraw, ImageFont

image = Image.new('1',(128,64),color=0)

d = ImageDraw.Draw(image)
fnt = ImageFont.load_default()
d.line([(0,0),(0,5)],fill=255,width=1)
d.text((20,20),'Hello World',font=fnt, fill=255)

#image.show()

imbytes = image.tobytes()
print(imbytes)

with open('/dev/fb0','wb') as f:
    f.write(imbytes)