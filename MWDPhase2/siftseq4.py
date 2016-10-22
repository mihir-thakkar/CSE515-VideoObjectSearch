import math
import numpy as np
from scipy.spatial.distance import cdist
import pylab
import imageio


objectIndex = 3
queryIndex = 1
a = 1
b = 10

fileIndex = np.genfromtxt('output.sift.index', delimiter="=", dtype=None)
fileIndex = dict(fileIndex)
objectFile = imageio.get_reader('DataR/'+fileIndex[objectIndex],  'ffmpeg')
queryFile = imageio.get_reader('DataR/'+fileIndex[queryIndex],  'ffmpeg')
myseq1 = None
myseq2 = None

frameToFrame = np.loadtxt('outfile.sseq', delimiter=",");
frameToFrameDist = np.loadtxt('outfile.smseq', delimiter=",");

rows,columns = frameToFrame.shape


allSeq = np.array([]).reshape(0,3);

for j in range(0, columns):
    seq = np.array([])
    seqIndex = np.array([])
    seqSim = np.array([])
    for i in range(0, rows):
        if i == 0:
            seq = np.append(seq, frameToFrame[i, j]);
            seqIndex = np.append(seqIndex, i);
            seqSim = np.append(seqSim, frameToFrameDist[i, j]);
        else:
            indexes = np.where((frameToFrame[i, :] >= (seq[-1])))
            if (indexes[0].size != 0):
                values = frameToFrame[i, indexes]
                values = values[0]
                mmv = values[0];
                idx = 0;counter =0;
                eidx = 0;
                for v in values:
                    if(v==seq[-1]):
                        eidx = counter;
                        break;
                    if(v>seq[-1] and v<mmv):
                        mmv = v
                        idx = counter;
                    counter = counter + 1;
                if((mmv-seq[-1]) > 4):
                    idx = eidx;
                ngi = indexes[0][idx];
                seq = np.append(seq, frameToFrame[i, ngi]);
                seqSim = np.append(seqSim, frameToFrameDist[i, ngi]);
                if (seq[-1] != seq[-2]):
                    seqIndex = np.append(seqIndex, i);
                    if ((seqIndex[-1] - seqIndex[-2]) > 1):
                        sp = seq[-2]
                        ep = seq[-1]
                        rsp = seq[-1] - seq[-2];
                        if ((i - rsp + 1) > 0):
                            lastFNo = sp
                            for k in range(int(i - rsp + 1), i):
                                indexes = np.where((frameToFrame[k, :] == lastFNo + 1))
                                if (indexes[0].size != 0):
                                    ngi = indexes[0][0];
                                    seq[k] = frameToFrame[k, ngi];
                                    lastFNo = seq[k];
                                    seqSim[k] = frameToFrameDist[i, ngi];
    allSeq = np.vstack([allSeq, [np.mean(seqSim), seq[0], seq[-1]]])
    #print "stop"
    print seq



allSeq = allSeq[np.argsort(allSeq[:, 0])]
#allSeq = allSeq[np.lexsort((allSeq[:, 1],allSeq[:, 2]))]
finalSeq = np.array([]).reshape(0,3);
for v in np.unique(allSeq[:, 2]):
    firstLSeq = (allSeq[allSeq[:,2]==v,:])[0,:]
    finalSeq = np.vstack([finalSeq, firstLSeq])
finalSeq = finalSeq[np.argsort(finalSeq[:, 0])]

for row in finalSeq:
    print 'Next'
    for i in range(int(row[1]), int(row[2] + 1)):
        fig2 = pylab.figure(1)
        oimage = objectFile.get_data(i)
        if myseq2 is None:
            myseq2 = pylab.imshow(oimage)
        else:
            myseq2.set_data(oimage)
        fig2.suptitle('Oimage #{}'.format(i), fontsize=20)
        pylab.pause(0.04)
        pylab.draw()

print 'stop here1'
