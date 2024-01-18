import matplotlib.pyplot as plt
import numpy as np
import argparse
import random


# functions ------------------------------------------------------------------------------------------------------------

    # print error command if can't plot any more points

def swarmplot(yList,xCenter,pointSize,xMin,xMax,yMin,yMax,panelWidth,panelHeight):
    minDistance = pointSize/72
    increment = minDistance/5
    placedPoints = []

    for yCoord in yList:
        xCoord = xCenter
        if len(placedPoints) == 0:
            placedPoints.append((xCoord,yCoord))
        else:
            var = False
            shift = 0
            count = 0
            while var == False:
                count += 1
                distances = []
                for point in placedPoints:
                    xDistance = (abs(xCoord-point[0])/(xMax-xMin))*panelWidth
                    yDistance = (abs(yCoord-point[1])/(yMax-yMin))*panelHeight
                    distance = (xDistance**2+yDistance**2)**0.5
                    distances.append(distance)
                if min(distances) > minDistance:
                    placedPoints.append((xCoord,yCoord))
                    var = True
                    break
                if min(distances) == 0.4:
                    break
                else:
                    if count % 2 == 0:
                        xCoord += increment*(count/2)
                    else:
                        xCoord -= increment*(count/2)
    return placedPoints


# parse command line args ----------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser()  # instantiate parser object to which you can add arguments

parser.add_argument('--inFile', '-i', type=str, action='store', help='input file',
                    default='BME163_Input_Data_3.txt')
parser.add_argument('--outFile', '-o', type=str, action='store', help='output file',
                    default='Price_Madison_BME163_Assignment_Week4.png')


args = parser.parse_args()
inFile = args.inFile
outFile = args.outFile


# generate figure and panels -------------------------------------------------------------------------------------------

plt.style.use('BME163.mplstyle')

figureHeight = 3
figureWidth = 10
plt.figure(figsize=(figureWidth, figureHeight))

# place panels of correct size within figure
panelWidth = 6
panelHeight = 2
relativePanelWidth = panelWidth / figureWidth
relativePanelHeight = panelHeight / figureHeight

panel1 = plt.axes([0.1, 0.15, relativePanelWidth, relativePanelHeight],    # left, bottom, width, height
                  xlabel='Subread Coverage', ylabel='Identity (%)')

# set x and y limits
xMin = 0
xMax = 12
yMin = 75
yMax = 100
panel1.set_xlim(xMin, xMax)
panel1.set_ylim(yMin, yMax)

# place the tick marks and tick labels
panel1.tick_params(bottom=True, labelbottom=True,
                   left=True, labelleft=True,
                   right=False, labelright=False,
                   top=False, labeltop=False)



# parse file data ---------------------------------------------------------------------------------------------------

dict = dict()

# dictionary (keys = bin, values = list of percent values)
with open(inFile, 'r') as file:
    for line in file:
        columns = line.rstrip().split()
        column1 = columns[0]
        subreadCov = column1.rstrip().split('_')[3]
        if int(subreadCov) > 10:
            subreadCov = '>10'
        if subreadCov not in dict:
            dict[subreadCov] = [float(columns[1])]
        if subreadCov in dict:
            dict[subreadCov].append(float(columns[1]))


for key in dict:
    yList = dict[key]
    pointSize = 1
    if key != '>10':
        xCenter = int(key)
    if key == '>10':
        xCenter = 11
    sample1000 = random.sample(yList, 1000)
    coordTuples = swarmplot(sample1000, xCenter, pointSize, xMin, xMax, yMin, yMax, panelWidth, panelHeight)
    for tuple in coordTuples:
        xCoord = tuple[0]
        yCoord = tuple[1]
        panel1.plot(xCoord,yCoord, marker='o',
                   markerfacecolor='black',
                    markersize=1,
                    markeredgewidth=0,
                    linewidth=0)

for x in range(1,12):
    key = str(x)
    width = 0.4
    if key in dict.keys():
        median = np.median(dict[key])
    else:
        median = np.median(dict['>10'])
    panel1.plot([x-width, x+width], [median, median], linewidth=1, color='red')

# ----------------------------------------------------------------------------------------------------------------------

plt.savefig(fname=outFile, dpi=600)