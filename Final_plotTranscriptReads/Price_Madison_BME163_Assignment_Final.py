import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import argparse


# parse command line args ----------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument('--pslFile1', '-i1', type=str, action='store', help='psl file 1',
                    default='BME163_Input_Data_5.psl')
parser.add_argument('--pslFile2', '-i2', type=str, action='store', help='psl file 2',
                    default='BME163_Input_Data_6.psl')
parser.add_argument('--gtfFile', '-g', type=str, action='store', help='gtf file',
                    default='gencode.vM12.annotation.gtf')
parser.add_argument('--coords', '-c', type=str, action='store', help='coordinates',
                    default='chr7:45232000-45241000')
parser.add_argument('--outFile', '-o', type=str, action='store', help='output file',
                    default='Price_Madison_BME163_Assignment_Final.png')

args = parser.parse_args()
pslFile1 = args.pslFile1
pslFile2 = args.pslFile2
gtfFile = args.gtfFile
c = args.coords
coords = ((c.split(':')[0]),int(c.split(':')[1].split('-')[0]),int(c.split(':')[1].split('-')[1]))   # chromosome #, area start, area end
outFile = args.outFile

# panel formatting -----------------------------------------------------------------------------------------------------

plt.style.use('BME163.mplstyle')
figureHeight = 5
figureWidth = 5
plt.figure(figsize=(figureWidth, figureHeight))

panelWidth = 4.9
panelHeight = 1.5
relativePanelWidth = panelWidth / figureWidth
relativePanelHeight = panelHeight / figureHeight

panel1 = plt.axes([0.01, 0.65, relativePanelWidth, relativePanelHeight])
panel2 = plt.axes([0.01, 0.33, relativePanelWidth, relativePanelHeight])
panel3 = plt.axes([0.01, 0.01, relativePanelWidth, relativePanelHeight])

panel1.tick_params(bottom=False, labelbottom=False,
                   left=False, labelleft=False,
                   right=False, labelright=False,
                   top=False, labeltop=False)
panel2.tick_params(bottom=False, labelbottom=False,
                   left=False, labelleft=False,
                   right=False, labelright=False,
                   top=False, labeltop=False)
panel3.tick_params(bottom=False, labelbottom=False,
                   left=False, labelleft=False,
                   right=False, labelright=False,
                   top=False, labeltop=False)

xMin = coords[1]-1
xMax = coords[2]+1
yMin = 0
panel1.set_xlim(xMin, xMax)
panel1.set_ylim(yMin, 9.8)
panel2.set_xlim(xMin, xMax)
panel2.set_ylim(yMin, 69.2)
panel3.set_xlim(xMin, xMax)
panel3.set_ylim(yMin, 444)

# functions ------------------------------------------------------------------------------------------------------------

def readGTF(gtfFile,chromosome,areaStart,areaEnd):

    myDict = dict()
    valid = ['transcript','exon','CDS']
    file = open(gtfFile, 'r')
    chromosome = [chromosome]
    for line in file:
        if line[0] != '#':
            splitLine = line.strip().split('\t')
            transcriptID = splitLine[8].split('"')[3]
            chrom = splitLine[0]
            type = splitLine[2]
            start = int(splitLine[3])
            end = int(splitLine[4])
            if chrom in chromosome and ((areaStart <= start <= areaEnd) or (areaStart <= end <= areaEnd)):
                if type in valid:
                    if transcriptID in myDict:
                        myDict[transcriptID].append((start, end, type, chrom))
                    else:
                        myDict[transcriptID] = [(start, end, type, chrom)]

    reads = []
    for key,value in myDict.items():
        blockStarts = []
        blockWidths = []
        heights = []
        start,end = 0, 0
        read = [0, 0, [], False]
        for tuple in value:
            if tuple[2] == 'transcript':
                start = tuple[0]
                end = tuple[1]
            else:
                blockStart = tuple[0]
                blockEnd = tuple[1]
                blockWidth = blockEnd - blockStart
                blockStarts.append(blockStart)
                blockWidths.append(blockWidth)
                if tuple[2] == 'exon':
                    heights.append(0.25)
                if tuple[2] == 'CDS':
                    heights.append(0.50)
            # vvv this will add all exons and CDS to the lists for each tuple in value so you have duplicates
        for x in range(len(blockWidths)):
            read[2].append([blockStarts[x], blockWidths[x], heights[x]])
        read[0] = start
        read[1] = end
        reads.append(read)
    return reads


def readPSL(pslFile,chromosome,areaStart,areaEnd):
    reads = []
    chromosome = [chromosome]
    with open(pslFile) as file:
        for line in file:
            splitLine = line.strip().split('\t')
            chrom = splitLine[13]
            start = int(splitLine[15])
            end = int(splitLine[16])
            if chrom in chromosome and start >= areaStart and end <= areaEnd:
                blockWidths = np.array(splitLine[18].split(',')[:-1], dtype=int)
                blockStarts = np.array(splitLine[20].split(',')[:-1], dtype=int)
                read = [start, end, [[blockStarts[x], blockWidths[x], 0.5] for x in range(len(blockWidths))], False]
                reads.append(read)
    return reads


def plotAlignments(alignment, yPos, panel, color, linewidth, edgecolor = None):
    xStart = alignment[0]
    width = alignment[1]-alignment[0]
    thinRectangle = mplpatches.Rectangle((xStart, yPos-.025), width , 0.05, facecolor=color, linewidth=linewidth, edgecolor = edgecolor)
    panel.add_patch(thinRectangle)
    for block in alignment[2]:
        thickRectangle = mplpatches.Rectangle((block[0], yPos-(block[2]/2)), block[1], block[2], facecolor=color, linewidth=linewidth, edgecolor = edgecolor)
        panel.add_patch(thickRectangle)


def stackAlignments(alignments, panel, color, lineWidth, sortBy = 'start', edgecolor = None):
    sortedAlignments = []
    yPos = 1
    if sortBy == 'start':
        sortedAlignments = sorted(alignments, key = lambda x: (x[0], x[1]))
    if sortBy == 'end':
        sortedAlignments = sorted(alignments, key=lambda x: x[1], reverse = True)
    plottedCount = 0
    while plottedCount < len(sortedAlignments):
        previousEnd = 0
        for alignment in sortedAlignments:
            start = alignment[0]
            if alignment[-1] == False:
                if start > previousEnd:
                    plotAlignments(alignment, yPos, panel, color, lineWidth, edgecolor)
                    alignment[-1] = True
                    previousEnd = alignment[1]
                    plottedCount += 1
        yPos += 1


# parse file data ------------------------------------------------------------------------------------------------------

iYellow=(248/255,174/255,51/255)
iBlue=(88/255,85/255,120/255)

alignments1 = readPSL(pslFile1, coords[0], coords[1], coords[2])    # file 5 goes on bottom
alignments2 = readPSL(pslFile2, coords[0], coords[1], coords[2])    # file 6 goes in middle
alignments3 = readGTF(gtfFile, coords[0], coords[1], coords[2])

stackAlignments(alignments3, panel1, 'Grey', 0.25, 'start', 'black')
stackAlignments(alignments2, panel2, iBlue, 0.05, 'start', 'black')
stackAlignments(alignments1, panel3, iYellow, 0.01, 'end', 'black')

plt.savefig(fname=outFile, dpi=2400)
