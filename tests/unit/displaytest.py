'''
Functions to test different aspects of the display.
Not currently using unittest because test results involve displaying images.
'''
import numpy as np
import matplotlib.pyplot as plt
import pymdl.display


def test_displayData(sname,data):
    '''
    Test displayData with hardcoded data
    '''
    measurements = ['T','RH','BP']
    units = {'T':'C','RH':'%','BP':'mb'}

    img = pymdl.display.displayData(
        sname,
        data['dt'],
        measurements,
        data,
        units)

    #Display image
    npimg = np.asarray(img)
    plt.imshow(npimg,cmap='gray')
    plt.show()

def test_getdata():
    '''
    Test getdata
    Databear must be running
    '''
    data = pymdl.display.getdata('tph1')
    return data

if __name__ == "__main__":
    testdata = test_getdata()
    test_displayData('tph1',testdata)
        
    
