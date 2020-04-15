'''
Test out pillow library
- Follow tutorial: https://pillow.readthedocs.io/en/stable/handbook/tutorial.html
'''

from PIL import Image, ImageDraw, ImageFont

im = Image.open('DataBearStore.png')

print(im.format, im.size, im.mode)

#Try manipulating
#im = im.rotate(45)
im = im.transpose(Image.FLIP_LEFT_RIGHT)

#Try drawing
fnt = ImageFont.truetype('arial.ttf',15)
d = ImageDraw.Draw(im)
d.ellipse([(2,2),(100,30)],fill='green',width=6)
d.text((20,20),'Hello World',font=fnt)



im.show()