import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import argparse


# parse command line args ----------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument('--inFile', '-i', type=str, action='store', help='input file',
                    default='BME163_Input_Data_4.txt')
parser.add_argument('--outFile', '-o', type=str, action='store', help='output file',
                    default='Price_Madison_BME163_Assignment_Week6.png')
args = parser.parse_args()
inFile = args.inFile
outFile = args.outFile


# generate figure and panels -------------------------------------------------------------------------------------------

plt.style.use('BME163.mplstyle')

figureHeight = 3
figureWidth = 5
plt.figure(figsize=(figureWidth, figureHeight))

# place panels of correct size within figure
panel1Width = 0.75
panel2Width = 2.5
panelHeight = 2.5
relativePanel1Width = panel1Width / figureWidth
relativePanelHeight = panelHeight / figureHeight

panel1 = plt.axes([0.1, 0.1, relativePanel1Width, relativePanelHeight],    # left, bottom, width, height
                  xlabel='CT', ylabel='Number of genes')

# set x and y limits
xMin = 0
xMax = 16
yMin = 0
yMax = 1262   # 1236?

panel1.set_xlim(xMin, xMax)
panel1.set_ylim(yMin, yMax)

# place the tick marks and tick labels
panel1.tick_params(bottom=True, labelbottom=True,
                   left=True, labelleft=True,
                   right=False, labelright=False,
                   top=False, labeltop=False)

panel1.set_xticks([1,3,5,7,9,11,13,15])
panel1.set_xticklabels(['0','','6','','12','','18',''])


# color maps -----------------------------------------------------------------------------------------------------------

viridis5 = (253/255, 231/255, 37/255)
viridis4 = (94/255, 201/255, 98/255)
viridis3 = (33/255, 145/255, 140/255)
viridis2 = (59/255, 82/255, 139/255)
viridis1 = (68/255, 1/255, 84/255)

R12 = np.linspace(viridis1[0],viridis2[0],25)
G12 = np.linspace(viridis1[1],viridis2[1],25)
B12 = np.linspace(viridis1[2],viridis2[2],25)

R23 = np.linspace(viridis2[0],viridis3[0],25)
G23 = np.linspace(viridis2[1],viridis3[1],25)
B23 = np.linspace(viridis2[2],viridis3[2],25)

R34 = np.linspace(viridis3[0],viridis4[0],25)
G34 = np.linspace(viridis3[1],viridis4[1],25)
B34 = np.linspace(viridis3[2],viridis4[2],25)

R45 = np.linspace(viridis4[0],viridis5[0],26)
G45 = np.linspace(viridis4[1],viridis5[1],26)
B45 = np.linspace(viridis4[2],viridis5[2],26)

R = np.concatenate((R12,R23,R34,R45),axis=None)
G = np.concatenate((G12,G23,G34,G45),axis=None)
B = np.concatenate((B12,B23,B34,B45),axis=None)

# parse file data ------------------------------------------------------------------------------------------------------

def normalize(list):
    maximum = max(list[:-1])
    minimum = min(list[:-1])
    normalized = []
    for x in list[:-1]:
        xNormalized = int(((x-minimum)/(maximum-minimum))*100)
        normalized.append(xNormalized)
    normalized.append(int(list[-1]))
    return normalized


file = open(inFile, 'r')
next(file)
list = []
for row in file:
    x = row.rstrip().split()
    data = [float(x[4]),float(x[5]),float(x[6]),float(x[7]),float(x[8]),float(x[9]),float(x[10]),float(x[11]),float(x[13])]
    normalizedData = normalize(data)
    list.append(normalizedData)

y=0
for row in sorted(list,key=lambda x: x[-1],reverse=True):   # sort based on (np.argmax(x))?
    y+=1
    x=0
    for i in row:
        rectangle=mplpatches.Rectangle((x,y),3,1, facecolor=(R[i],G[i],B[i]),linewidth=0)
        panel1.add_patch(rectangle)
        x+=2

# ----------------------------------------------------------------------------------------------------------------------

plt.savefig(fname=outFile, dpi=600)


# start with function that shades area of a triangle by drawing lots of lines
    # give function three points and the panel to put the triangle
    # def triangle(point1,point2, point3, panel1):
    # create a linspace between point 2 and 3 containing lots of points
        # xList = np.linspace(point2[0],point3[0],500)
        # yList = np.linspace(oint2[1],point3[1],500)
        # for index in range (0,lenxList),1):
            # xValue = xList[index]
            # yValue = yList[index]
            # panel.plot([point1[0], xValue],[point1[1],yValue],
                        # color='black'.
                        # linewidth=0.25)

# circular histogram is not made of triangles though
# one line will be an arc
# we have plotted points in a circle in assignment 1 (center of arcs won't be 0,0, will need an offset))
# filling also has to be grey while bordr is black

# lecture 21 code ^^
# def arc(radian1,radian2,radius,panel):
    # xList = []
    # yList = []

    # for step in np.linspace(radian1, radian2,10):
        # x = np.cos(step)*radius
        # y = np.sin(step)*radius
        # xList.append(x)
        # yList.append(y)

    # panel.plot(xList, yList,
                # color='black',
                # linewidth=0,
                # marker='o',
                # markersize=2,
                # markeredgewidth=0,
                # markerfacecolor='purple')

# radius = 4
# radian1 = 0
# radian2 = np.pi (half a circle)  # matplotlib goes counter clockwise, but we want tp plot clockwise


