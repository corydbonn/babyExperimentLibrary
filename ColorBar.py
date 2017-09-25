#This script builds on the Psychopy grating stimulus type to create a color bar with blended colors.

#To draw a stimulus with this, specify the following arguments:
#window in which the stim appears, the number of steps to take between colors, the edge color, the center color, the blend type (parabolic or linear symmetric), the width (in pixels) and the height (in pixels), and x and y coordinates (in pixels)

#arguments:
#window: variable, eg., win
#numColors: integer, eg., 30
#rgbend: hex code or rgb values, eg., '#ffccjj' or (255,0,204)
#rgbmid: same as above
#blend: mathematical shape; choose 'parabolic' or 'linearSymmetric', linear (asymmetric) is default with any other specification
#width: width in pixels, eg., 500
#height: height in pixels, eg., 20
#x: horiz distance from origin in pixels, neg = left; eg., -40.
#y: vert distance from origin in pixels, neg = down; eg., 40.

#Example function call:
#bar = colorBar(win, 30, hex_to_rgb('#660066'), hex_to_rgb('#ff66cc'), 'linearSymmetric', 500, 20)
    #default is black to white

#packages required
from psychopy import visual
import numpy as np

#function to convert hex to rgb
def hex_to_rgb(hex):
     hex = hex.lstrip('#')
     hlen = len(hex)
     return tuple(int(hex[i:i+hlen/3], 16) for i in range(0, hlen, hlen/3))

#main function
def colorBar(window, numColors, edgeColor, midColor, blend, width, height, x, y):
    if window: #make sure window is defined
        pass
    else:
        print 'no output window chosen for color bar'

    colors = numColors

    #function to convert rgb numbers to psychopy's scale from -1 to 1
    def convColor(rgbtuple):
        arr = np.array(rgbtuple)
        return (arr - 128.)/128

    #main function
    def getColorVals(end, mid):

        #take colors and derive gradient using numpy
            #first option -- parabolic gradient, places more emphasis on mid color
        if blend == 'parabolic':
            #derived using the a(x-h)^2 + k formula for parabola
            absEnd = np.sqrt(abs(end-mid))

            if end < mid: #for downard facing parabola
                return -np.linspace(-absEnd, absEnd, num=colors, endpoint=True)**2 + mid
            elif end > mid: #for upward facing parabola
                return np.linspace(-absEnd, absEnd, num=colors, endpoint=True)**2 + mid
            else:
                return np.repeat(end,colors) #default to constant color channel

        elif blend == 'linearSymmetric': #places equal emphasis on edge and mid
            rampUp = np.linspace(end, mid, num=colors/2, endpoint=True) #gradient from edge to mid
            rampDown = np.linspace(mid, end, num=colors/2, endpoint=True) #gradient from mid to edge
            return np.concatenate((rampUp, rampDown), axis=0) #join for symmetric gradient

        else:
            return np.linspace(mid, end, num=colors, endpoint=True) #default to just plain linear gradient

    #declare array for gradient color input in rgb channels
    channels = [[],[],[]]

    #check if hex or rgb input, then convert to psychopy color space
        #check edge input
    if type(edgeColor) == str:
        try:
            rgbend = convColor(hex_to_rgb(edgeColor))
        except:
            rgbend = convColor(hex_to_rgb('#000000'))
    else:
        rgbend = convColor(edgeColor)

        #check mid input
    if type(midColor) == str:
        try:
            rgbmid = convColor(hex_to_rgb(midColor))
        except:
            rgbmid = convColor(hex_to_rgb('#ffffff'))
    else:
        rgbmid = convColor(edgeColor)


    #run the above functions for getting the colors of the gradient
    for h in range(3):
        channels[h].extend(getColorVals(rgbend[h],rgbmid[h]))

    #preaollocate space for the texture argument in GratingStim, which implements the colors
    myTex = np.zeros((colors,1,4))

    #place linear arrays from color channels into the texture
    for i in range(colors):
        for j in range(3):
            myTex[i][0][j] = channels[j][i]
        #set alpha/opacity to 1; if change desired, add an argument to the function definition and replace here
        myTex[i][0][3] = 1
        #myTex[i][0][3] = alpha

    #run psychopy stimulus function with derived texture input
    myStim = visual.GratingStim(window, tex=myTex, mask=None, size=(width,height), pos=(x, y))

    #return the defined stimulus
    return myStim
