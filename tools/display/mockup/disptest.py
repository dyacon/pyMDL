# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# ## Testing some different display configurations
# Use this on Windows to preview what the display might look like on the MDL
# %% [markdown]
# ### Create basic image

# %%
#Import PIL and use matplotlib for display
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np

#Create image
im = Image.new('1',(128,64),color=0)
fnt = ImageFont.truetype('LiberationMono-Regular.ttf',10)
d = ImageDraw.Draw(im)


# %% [markdown]
# ### Test data displays

# %%
#Clear image
d.rectangle([(0,0),(128,64)],fill=0,outline=255)

#Display content
teststr = ('Dyacon TPH-1\n'
           'T:  20.56 C\n'
           'RH: 35%\n'
           'BP: 890 mb\n'
           'Test test test\n'
           'Test test test\n')

d.multiline_text(
        (0,0),
        teststr,
        font=fnt,
        fill=255,
        spacing=2)

npim = np.asarray(im)
plt.imshow(npim,cmap='gray')

# %% [markdown]
# #### Test system display

# %%
#Clear image
d.rectangle([(0,0),(128,64)],fill=0,outline=255)

#Display content
headerstr = ('MDL-700     13:45:22\n'
           'DataBear V1.2 - Running\n'
           'Status:\n')

d.multiline_text(
        (0,0),
        headerstr,
        font=fnt,
        fill=255,
        spacing=2)

npim = np.asarray(im)
plt.imshow(npim,cmap='gray')

# %% [markdown]
# ### Test font options

# %%
#Clear image
d.rectangle([(0,0),(128,64)],fill=0,outline=255)

#Display content
teststr1 = 'ABCDEF 01234'
teststr2 = 'GHIJKL 56789'
teststr3 = 'abcdefghijkl'

d.text((0,0),teststr1,font=fnt,fill=255)
d.text((0,20),teststr2,font=fnt,fill=255)
d.text((0,40),teststr3,font=fnt,fill=255)

npim = np.asarray(im)
plt.imshow(npim,cmap='gray')


# %%


