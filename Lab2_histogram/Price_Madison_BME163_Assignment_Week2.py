import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import math
import argparse

parser = argparse.ArgumentParser()  # instantiate parser object to which you can add arguments

parser.add_argument('--inFile', '-i', type=str, action='store', help='input file')
parser.add_argument('--outFile', '-o', type=str, action='store', help='output file',
                    default='Price_Madison_BME163_Assignment_Week2.png')

args = parser.parse_args()  # get args back by parsing them
inFile = args.inFile
outFile = args.outFile

# -----------------------------------------------------------------------------------------------------------------------
plt.style.use('BME163.mplstyle')

# make figure the size we want
figureHeight = 2
figureWidth = 5
plt.figure(figsize=(figureWidth, figureHeight))

# place panels of correct size within figure
mainPanelWidth = 1
mainPanelHeight = 1
relativeMainPanelWidth = mainPanelWidth / figureWidth
relativeMainPanelHeight = mainPanelHeight / figureHeight

sidePanelHeight = 1
sidePanelWidth = 0.25
relativeSidePanelHeight = sidePanelHeight / figureHeight
relativeSidePanelWidth = sidePanelWidth / figureWidth

topPanelHeight = 0.25
topPanelWidth = 1
relativeTopPanelHeight = topPanelHeight / figureHeight
relativeTopPanelWidth = topPanelWidth / figureWidth

panel1 = plt.axes([0.14, 0.15, relativeMainPanelWidth, relativeMainPanelHeight])  # left, bottom, width, height
panel2 = plt.axes([0.076, 0.15, relativeSidePanelWidth, relativeSidePanelHeight])  # side panel
panel3 = plt.axes([0.14, 0.685, relativeTopPanelWidth, relativeTopPanelHeight])  # top panel

# place the tick marks and tick labels
panel1.tick_params(bottom=True, labelbottom=True,
                   left=False, labelleft=False,
                   right=False, labelright=False,
                   top=False, labeltop=False)
panel2.tick_params(bottom=True, labelbottom=True,
                   left=True, labelleft=True,
                   right=False, labelright=False,
                   top=False, labeltop=False)
panel3.tick_params(bottom=False, labelbottom=False,
                   left=True, labelleft=True,
                   right=False, labelright=False,
                   top=False, labeltop=False)

# set x and y limits
panel1.set_xlim(0, 15)
panel1.set_ylim(0, 15)

panel2.set_xlim(20, 0)
panel2.set_ylim(0, 15)

panel3.set_xlim(0, 15)
panel3.set_ylim(0, 20)

# plot scatter plot
# read data from file
xList = []
yList = []

for line in open('BME163_Input_data_1.txt'):
    a = line.rstrip().split('\t')
    x = math.log(int(a[1]) + 1, 2)
    y = math.log(int(a[2]) + 1, 2)
    xList.append(x)
    yList.append(y)

# make plot in center
panel1.plot(xList, yList,
            marker='o',
            markersize=1.5,
            linewidth=0,
            markeredgewidth=0,
            markerfacecolor='black',
            alpha=0.1)

# x histogram
bins = np.arange(0, 15, 0.5)
# bins = np.linspace(0,15,31)
xHisto, bins = np.histogram(xList, bins)

for index in range(0, len(xHisto), 1):
    bottom = 0
    left = bins[index]
    width = bins[index + 1] - left
    # width = relativeTopPanelWidth/30
    height = math.log(int(xHisto[index]) + 1, 2)
    rectangle1 = mplpatches.Rectangle((left, bottom), width, height,
                                      linewidth=0.1,
                                      edgecolor='black',
                                      facecolor='grey')
    panel3.add_patch(rectangle1)

# y histogram
yHisto, bins = np.histogram(yList, bins)

for index in range(0, len(yHisto), 1):
    # bottom = 0.15 + ((relativeSidePanelHeight/30)*index)
    bottom = bins[index]
    # left = (0.076 + relativeSidePanelWidth) - yHisto[index]
    left = 0
    width = math.log(int(yHisto[index]) + 1, 2)
    # height = relativeSidePanelHeight/30
    height = bins[index + 1] - bottom
    rectangle1 = mplpatches.Rectangle((left, bottom), width, height,
                                      linewidth=0.1,
                                      edgecolor='black',
                                      facecolor='grey')
    panel2.add_patch(rectangle1)

# -----------------------------------------------------------------------------------------------------------------------

plt.savefig(fname=outFile, dpi=600)
