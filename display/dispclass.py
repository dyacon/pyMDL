'''
Testing a display class
'''
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

class tphdisplay:
    '''
    Creates a display on the MDL for tph
    '''
    def __init__(self):
        '''
        Set up basic image
        '''
        self.image = Image.new('1',(128,64),color=0)
        self.font = ImageFont.truetype(
            '/usr/share/fonts/liberation/LiberationMono-Regular.ttf',10)
        self.draw = ImageDraw.Draw(self.image)

    def displaydata(self,dt,airT,rh,bp):
        dispstr = ('Dyacon TPH-1\n'
                   'Air T:  {0:%H:%M:%S} {1:.2f}\n'
                   'RH:     {0:%H:%M:%S} {2:.1f}\n'
                   'BP:     {0:%H:%M:%S} {3:.1f}\n'.format(dt,airT,rh,bp)
                   )
        
        self.draw.multiline_text(
            (0,0),
            dispstr,
            font=self.font,
            fill=255,
            spacing=2
        )

        imbytes = self.image.tobytes()

        with open('/dev/fb0','wb') as f:
            f.write(imbytes)

#Test
dt = datetime.now()
at = 25.66754
rh = 15.55664
bp = 856.99456

tph = tphdisplay()
tph.displaydata(dt,at,rh,bp)