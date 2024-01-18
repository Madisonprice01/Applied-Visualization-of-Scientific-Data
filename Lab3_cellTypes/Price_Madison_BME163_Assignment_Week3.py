import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import matplotlib.patheffects as patheffects
import numpy as np
import statistics as stat
import argparse

# parse command line args ----------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser()  # instantiate parser object to which you can add arguments

parser.add_argument('--cellTypeFile', '-c', type=str, action='store', help='cell type file',
                    default='BME163_Input_Data_Week3.celltype.tsv')
parser.add_argument('--positionFile', '-p', type=str, action='store', help='position file',
                    default='BME163_Input_Data_Week3.position.tsv')
parser.add_argument('--outFile', '-o', type=str, action='store', help='output file',
                    default='Price_Madison_BME163_Assignment_Week3.png')


args = parser.parse_args()  # get args back by parsing them
outFile = args.outFile
cellTypeFile = args.cellTypeFile
positionFile = args.positionFile

# generate figure and panels -------------------------------------------------------------------------------------------

plt.style.use('BME163.mplstyle')

figureHeight = 4
figureWidth = 8
plt.figure(figsize=(figureWidth, figureHeight))

# place panels of correct size within figure
mainPanelWidth = 2
mainPanelHeight = 2
relativeMainPanelWidth = mainPanelWidth / figureWidth
relativeMainPanelHeight = mainPanelHeight / figureHeight

panel1 = plt.axes([0.1, 0.2, relativeMainPanelWidth, relativeMainPanelHeight],    # left, bottom, width, height
                  xlabel='tSNE 2', ylabel='tSNE 1')

# set x and y limits
panel1.set_xlim(-30, 30)
panel1.set_ylim(-40, 30)

# place the tick marks and tick labels
panel1.tick_params(bottom=True, labelbottom=True,
                   left=True, labelleft=True,
                   right=False, labelright=False,
                   top=False, labeltop=False)

# add data to figure ---------------------------------------------------------------------------------------------------

dict = dict()
xValuesMonocyte = []
yValuesMonocyte = []
xValuesTcell = []
yValuesTcell = []
xValuesBcell = []
yValuesBcell = []

# add 'cell type': (x coord, y coord) as key:value pairs to a dictionary
with open(positionFile, 'r') as pFile:
    for line in pFile:
        a = line.rstrip().split()
        name = a[0]
        x = float(a[1])
        y = float(a[2])
        dict[name] = [x, y]

# update dictionary values with cell type
with open(cellTypeFile, 'r') as cFile:
    next(cFile)
    for line in cFile:
        a = line.rstrip().split()
        cellType = a[1]
        name = a[2]
        dict[name].append(cellType)

# iterate through dict and plot points based on cell type
for name in dict:
    if dict[name][2] == 'monocyte':
        panel1.plot(dict[name][0], dict[name][1],
                    marker='o',
                    markerfacecolor='grey',
                    markersize=4,
                    markeredgewidth=0,
                    linewidth=0)
        xValuesMonocyte.append(dict[name][0])
        yValuesMonocyte.append(dict[name][1])

    if dict[name][2] == 'tCell':
        panel1.plot(dict[name][0], dict[name][1],
                    marker='o',
                    markerfacecolor='red',
                    markersize=4,
                    markeredgewidth=0,
                    linewidth=0)
        xValuesTcell.append(dict[name][0])
        yValuesTcell.append(dict[name][1])

    if dict[name][2] == 'bCell':
        panel1.plot(dict[name][0], dict[name][1],
                    marker='o',
                    markerfacecolor='blue',
                    markersize=4,
                    markeredgewidth=0,
                    linewidth=0)
        xValuesBcell.append(dict[name][0])
        yValuesBcell.append(dict[name][1])

# Calculate x and y coords for cell type text
xMedianMonocyte = stat.median(xValuesMonocyte)
yMedianMonocyte = stat.median(yValuesMonocyte)

xMedianTcell = stat.median(xValuesTcell)
yMedianTcell = stat.median(yValuesTcell)

xMedianBcell = stat.median(xValuesBcell)
yMedianBcell = stat.median(yValuesBcell)



txt1 = plt.text(xMedianMonocyte,yMedianMonocyte,'monocyte', size=8, color='black', ha='center', va='center')
txt1.set_path_effects([patheffects.withStroke(linewidth=1, foreground='w')])

txt2 = plt.text(xMedianTcell,yMedianTcell, 'tCell', size=8, color='black', ha='center', va='center')
txt2.set_path_effects([patheffects.withStroke(linewidth=1, foreground='w')])

txt3 = plt.text(xMedianBcell,yMedianBcell,'bCell', size=8, color='black', ha='center', va='center')
txt3.set_path_effects([patheffects.withStroke(linewidth=1, foreground='w')])

# ----------------------------------------------------------------------------------------------------------------------

plt.savefig(fname=outFile, dpi=600)