import math
import numpy as np
from scipy.spatial.distance import cdist
import pylab
import imageio


objectIndex = 3;
queryIndex = 1;
a = 1;
b = 25;

fileIndex = np.genfromtxt('output.sift.index', delimiter="=", dtype=None);
fileIndex = dict(fileIndex)
objectFile = imageio.get_reader('DataR/'+fileIndex[objectIndex],  'ffmpeg')
queryFile = imageio.get_reader('DataR/'+fileIndex[queryIndex],  'ffmpeg')
myseq1 = None;
myseq2 = None;

frameToFrame = np.loadtxt('outfile.sseq', delimiter=",");
frameToFrameDist = np.loadtxt('outfile.smseq', delimiter=",");

rows,columns = frameToFrame.shape




for j in range(8, columns):
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
                for v in values:
                    if(v==seq[-1]):
                        break;
                    if(v>seq[-1] and v<mmv):
                        mmv = v
                        idx = counter;
                    counter = counter + 1;
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
    #print "stop"
    print seq

    """for i in range(a - 1, b):
        image = queryFile.get_data(i)
        fig1 = pylab.figure(1)
        if myseq1 is None:
            myseq1 = pylab.imshow(image)
        else:
            myseq1.set_data(image)
        fig1.suptitle('Qimage #{}'.format(i), fontsize=20)

        fig2 = pylab.figure(2)
        oimage = objectFile.get_data(int(seq[i]))
        if myseq2 is None:
            myseq2 = pylab.imshow(oimage)
        else:
            myseq2.set_data(oimage)
        fig2.suptitle('Oimage #{}'.format(int(seq[i])), fontsize=20)
        pylab.pause(0.04)
        pylab.draw()"""

print 'stop here1'
