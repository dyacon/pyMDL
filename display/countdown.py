'''
Testing pillow
- Make a countdown and see how fast it appears
'''

from PIL import Image, ImageDraw, ImageFont

countdown = ['10','9','8','7','6','5','4','3','2','1']
fnt = ImageFont.load_default()

for count in countdown:
    image = Image.new('1',(128,64),color=0)

    d = ImageDraw.Draw(image)
    d.rectangle([(10,10),(30,30)],outline=255)
    d.text((15,15),count,font=fnt, fill=255)

    #image.show()

    imbytes = image.tobytes()
    #print(imbytes)

    with open('/dev/fb0','wb') as f:
        f.write(imbytes)
