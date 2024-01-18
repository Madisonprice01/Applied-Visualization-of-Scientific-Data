import matplotlib.pyplot as plt
import numpy as np
import argparse
import matplotlib.image as mpimg


# functions ------------------------------------------------------------------------------------------------------------

def fastaReader(fastaFile):
    seqDict1={}
    name=''
    sequence=[]
    for line in open(fastaFile):
        if line[0] =='>':
            if name:
                seqDict1[name]=('').join(sequence)
            name=line[1:].strip().split()[0]
            sequence=[]
        else:
           sequence.append(line.strip())
    if sequence:
        seqDict1[name]=('').join(sequence)
    return seqDict1


# parse command line args ----------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser()  # instantiate parser object to which you can add arguments

parser.add_argument('--bedFile', '-b', type=str, action='store', help='bed file',
                    default='Splice_Locations_chr15.bed')
parser.add_argument('--GenomeFile', '-G', type=str, action='store', help='Genome file',
                    default='chr15.fasta')
parser.add_argument('--outFile', '-o', type=str, action='store', help='output file',
                    default='Price_Madison_BME163_Assignment_Week5.png')
parser.add_argument('--aFile', '-a', type=str, action='store', help='a file',
                    default='A.png')
parser.add_argument('--tFile', '-t', type=str, action='store', help='t file',
                    default='T.png')
parser.add_argument('--cFile', '-c', type=str, action='store', help='c file',
                    default='C.png')
parser.add_argument('--gFile', '-g', type=str, action='store', help='g file',
                    default='G.png')


args = parser.parse_args()
bedFile = args.bedFile
genomeFile = args.GenomeFile
outFile = args.outFile

aFile = args.aFile
tFile = args.tFile
cFile = args.cFile
gFile = args.gFile

# generate figure and panels -------------------------------------------------------------------------------------------

plt.style.use('BME163.mplstyle')

figureHeight = 2
figureWidth = 5
plt.figure(figsize=(figureWidth, figureHeight))

# place panels of correct size within figure
panelWidth = 1.5
panelHeight = 0.5
relativePanelWidth = panelWidth / figureWidth
relativePanelHeight = panelHeight / figureHeight

panel1 = plt.axes([0.1, 0.3, relativePanelWidth, relativePanelHeight],    # left, bottom, width, height
                  xlabel='Distance to Splice Site', ylabel='Bits')

panel2 = plt.axes([0.44, 0.3, relativePanelWidth, relativePanelHeight],    # left, bottom, width, height
                  xlabel='Distance to Splice Site', )

# set x and y limits
xMin = -10
xMax = 10
yMin = 0
yMax = 2

panel1.set_xlim(xMin, xMax)
panel1.set_ylim(yMin, yMax)

panel2.set_xlim(xMin, xMax)
panel2.set_ylim(yMin, yMax)

panel1.set_title("5' SS")
panel2.set_title("3' SS")

# place the tick marks and tick labels
panel1.tick_params(bottom=True, labelbottom=True,
                   left=True, labelleft=True,
                   right=False, labelright=False,
                   top=False, labeltop=False)

panel2.tick_params(bottom=True, labelbottom=True,
                   left=False, labelleft=False,
                   right=False, labelright=False,
                   top=False, labeltop=False)

panel1.plot([0,0],[0,2],color='black',linewidth=0.5,zorder=200)
panel2.plot([0,0],[0,2],color='black',linewidth=0.5,zorder=200)

# parse file data ---------------------------------------------------------------------------------------------------


# First read in Fasta file with teh goal of creating a dictionary that has key=chromosome, value= sequence as a string
# (don't want to read in the genome every single time)- need to optimize

dict0 = fastaReader(genomeFile)
dict1 = dict()

for key in dict0.keys():
    dict1['chr'+str(key)] = dict0[key]


# read bed file line by
# parse columns (column 1 is dictionary key that we use to get sequences, column 2 is coords, take 10 nucleotides before and after)
    # int(coord)-10 to int(coord)+10
number5SS = 0
number3SS = 0
chr15List = []
with open(bedFile, 'r') as file:
    for line in file:
        columns = line.rstrip().split()
        key = columns[0]
        coord = int(columns[1])
        type = int(columns[3][0])
        chr15List.append([type, coord, dict1[key][coord-10:coord+10]])
        if type == 5:
            number5SS += 1
        if type == 3:
            number3SS += 1

# use another dictionary with positions as keys and list of nucleotides at that position in all splice sites as value
    # keys for this dictionary will be positions in sequence (0 to 19) and values are empty lists
        # for each new sequence, go through index by index, use index to get that base and as a key for dict,
        # appending all bases at that position in splice sites

dict3 = dict()
dict5 = dict()

for i in range(0,20,1):
    dict3[i] = []
    dict5[i] = []

for item in chr15List:
    type = item[0]
    seq = item[2]
    if type == 3:
        comp = seq.translate(str.maketrans('ATCGN', 'TAGCN'))       # [::-1]  < add this to end of line?
        revComp = comp[::-1]
        for nuc in range(0,20,1):
            dict3[nuc].append(revComp[nuc])
    if type == 5:
        for nuc in range(0,20,1):
            dict5[nuc].append(seq[nuc])


# use .count() method to calculate nucleotide frequencies in lists
    # once you have frequencies for every position, its only thing we need to calculate y axis values

freq5 = {x: {'A':0,'T':0,'C':0,'G':0} for x in range(0,20,1)}
freq3 = {x: {'A':0,'T':0,'C':0,'G':0} for x in range(0,20,1)}

for key,value in dict3.items():
    if len(value) == 0:
        pass
    else:
        countA = value.count('A')
        countC = value.count('C')
        countT = value.count('T')
        countG = value.count('G')
        totalCount = countA + countC + countT + countG
        freq3[key]['A'] = countA/totalCount
        freq3[key]['T'] = countT/totalCount
        freq3[key]['C'] = countC/totalCount
        freq3[key]['G'] = countG/totalCount

for key, value in dict5.items():
    if len(value) == 0:
        pass
    else:
        countA = value.count('A')
        countC = value.count('C')
        countT = value.count('T')
        countG = value.count('G')
        totalCount = countA + countC + countT + countG
        freq5[key]['A'] = countA / totalCount
        freq5[key]['T'] = countT / totalCount
        freq5[key]['C'] = countC / totalCount
        freq5[key]['G'] = countG / totalCount

sumnation5 = []
sumnation3 = []
for i in range(0,20,1):
    uncertainty5 = 0
    uncertainty3 = 0
    for j in freq3[i]:
        if freq3[i][j] != 0:
            uncertainty3 += freq3[i][j] * np.log2(freq3[i][j])
    uncertainty3 *= -1
    for j in freq5[i]:
        if freq5[i][j] != 0:
            uncertainty5 += freq5[i][j] * np.log2(freq5[i][j])
    uncertainty5 *= -1
    sumnation5.append(uncertainty5)
    sumnation3.append(uncertainty3)

e3 = (1/np.log(2)) * (3/(2*number3SS))
e5 = (1/np.log(2)) * (3/(2*number5SS))

height5 = {x: {'A':0,'T':0,'C':0,'G':0} for x in range(0,20,1)}
height3 = {x: {'A':0,'T':0,'C':0,'G':0} for x in range(0,20,1)}

for i in range(0,20,1):
    infoContent5 = np.log2(4) - (sumnation5[i] + e5)
    for j in height5[i]:
        height5[i][j] = freq5[i][j] * infoContent5
    infoContent3 = np.log2(4) - (sumnation3[i] + e3)
    for j in height3[i]:
        infoContent3 = np.log2(4) - (sumnation3[i] + e3)
        height3[i][j] = freq3[i][j] * infoContent3

A = mpimg.imread(aFile)
C = mpimg.imread(cFile)
T = mpimg.imread(tFile)
G = mpimg.imread(gFile)

for index in np.arange(-10,10,1):
    height5A = height5[index + 10]['A']
    height5C = height5[index + 10]['C']
    height5T = height5[index + 10]['T']
    height5G = height5[index + 10]['G']
    height5List = [[A,height5A],[C,height5C],[T,height5T],[G,height5G]]
    height5List.sort(key=lambda x: x[1])
    previousHeight = 0
    for i in range(4):
        panel1.imshow(height5List[i][0],aspect='auto',extent=[index,index+1,previousHeight,previousHeight+height5List[i][1]])
        previousHeight += height5List[i][1]

for index in np.arange(-10,10,1):
    height3A = height3[index + 10]['A']
    height3C = height3[index + 10]['C']
    height3T = height3[index + 10]['T']
    height3G = height3[index + 10]['G']
    height3List = [[A,height3A],[C,height3C],[T,height3T],[G,height3G]]
    height3List.sort(key=lambda x: x[1])
    previousHeight = 0
    for i in range(4):
        panel2.imshow(height3List[i][0],aspect='auto',extent=[index,index+1,previousHeight,previousHeight+height3List[i][1]])
        previousHeight += height3List[i][1]

# ----------------------------------------------------------------------------------------------------------------------

plt.savefig(fname=outFile, dpi=600)



