
import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import math
import argparse

parser = argparse.ArgumentParser()        # instantiate parser object to which you can add arguments

parser.add_argument('--inFile', '-i', type=str, action='store', help='input file')
parser.add_argument('--outFile', '-o', type=str, action='store', help='output file',default='Price_Madison_BME163_Assignment1_Week1.png')

args = parser.parse_args()   # get args back by parsing them
inFile = args.inFile
outFile = args.outFile

#-----------------------------------------------------------------------------------------------------------------------
blue=(0,0,1)
red=(1,0,0)
green=(0,1,0)
yellow=(1,1,0)
black=(0,0,0)
white=(1,1,1)

def colormap(color1,color2,n):
    R=np.linspace(color1[0],color2[0],n)
    G=np.linspace(color1[1],color2[1],n)
    B=np.linspace(color1[2],color2[2],n)
    return R,G,B

R1,G1,B1=colormap(black,white,28)
Rx,Gx,Bx=colormap(red,blue,11)
Ry,Gy,By=colormap(green,blue,11)
#-----------------------------------------------------------------------------------------------------------------------

plt.style.use('BME163.mplstyle')

# make figure the size we want
figureHeight=2
figureWidth=3.42
plt.figure(figsize=(figureWidth,figureHeight))

# place panels of correct size within figures
panelWidth=1
panelHeight=1
relativePanelWidth=panelWidth/figureWidth
relativePanelHeight=panelHeight/figureHeight

panel1=plt.axes([0.1,0.2,relativePanelWidth,relativePanelHeight])    # left,bottom, width,height  #0.55?
panel2=plt.axes([0.55,0.2,relativePanelWidth,relativePanelHeight])

panel1.tick_params(bottom=False, labelbottom=False,
                   left=False, labelleft=False,
                   right=False, labelright=False,
                   top=False, labeltop=False)
panel2.tick_params(bottom=False, labelbottom=False,
                   left=False, labelleft=False,
                   right=False, labelright=False,
                   top=False, labeltop=False)

# plot points in the left panel with correct color
#xList=np.arange(0,1.57,.0654)    # 24 dots from 0 to pi/2(1.57)
quarter= math.pi/2
xList=np.arange(0,quarter,quarter/24)    # 24 dots from 0 to pi/2

for value in xList:
    xvalue=np.cos(value)*100   # generates circle with radius of 100
    yvalue=np.sin(value)*100
    panel1.plot(xvalue,yvalue,
                marker='o',
                #markerfacecolor=(R1[int(value/.06545)],G1[int(value/.06545)],B1[int(value/.06545)]),
                markerfacecolor=(1-np.cos(value),1-np.cos(value),1-np.cos(value)),
                markersize=2,
                markeredgewidth=0,
                linewidth=0)

# use x lim and y lim functions to only get top right quadrant of the circle
panel1.set_xlim(0,100)
panel1.set_ylim(0,100)


# plot rectangles in the right panel with color gradients
for x in np.arange(0,1,0.1):
    for y in np.arange(0,1,0.1):
        rectangle=mplpatches.Rectangle((x,y),0.1,0.1,
                                       facecolor=(1-x,1-y,1),
                                       edgecolor='black',
                                       linewidth=0.75)
        panel2.add_patch(rectangle)

plt.savefig(fname=outFile,dpi=600)
