import math
import numpy as np
from scipy.spatial.distance import cdist
import pylab
import imageio

objectIndex = 3;
queryIndex = 1;
a = 25;
b = 50;
k = 1;

fileIndex = np.genfromtxt('output.sift.index', delimiter="=", dtype=None);
fileIndex = dict(fileIndex)
objectFile = imageio.get_reader('DataR/'+fileIndex[objectIndex],  'ffmpeg')
queryFile = imageio.get_reader('DataR/'+fileIndex[queryIndex],  'ffmpeg')

database = np.loadtxt('output.sift', delimiter=";");

object = database[database[:,0] == objectIndex,0:135];
oframeNos = np.transpose(np.unique(object[:,1]));

query = database[database[:,0] == queryIndex, 0:135];
query = query[(a<=query[:,1]) & (query[:,1]<=b), 0:135];
qframeNos = np.transpose(np.unique(query[:,1]));

myseq1 = None;
myseq2 = None;
frameToFrameSimIndex = np.array([]).reshape(0,oframeNos.size);
frameToFrameSimDis = np.array([]).reshape(0,oframeNos.size);
for qframeNo in np.nditer(qframeNos):
    qframe = query[query[:, 1] == qframeNo, 7:135];
    frameSim = np.array([]).reshape(0,3);
    for oframeNo in np.nditer(oframeNos):
        oframe = object[object[:, 1] == oframeNo, 7:135];
        frameD = cdist(qframe, oframe, 'euclidean');
        minD = np.amin(frameD,axis=1);
        meanD = np.mean(minD);
        medianD = np.median(minD);
        frameSim = np.vstack([frameSim, [oframeNo,meanD,medianD]])
    frameSim = frameSim[np.argsort(frameSim[:, 1])]
    #frameSim = frameSim[np.lexsort((frameSim[:, 1],frameSim[:, 2]))]
    frameToFrameSimIndex = np.vstack([frameToFrameSimIndex, frameSim[:,0].T])
    frameToFrameSimDis = np.vstack([frameToFrameSimDis, frameSim[:, 1].T])
    #I = np.argmin(frameSim[:,2], axis=0)
    """minF = frameSim[0,:];
    cof =  minF[0]
    image = queryFile.get_data(int(qframeNo))
    fig1 = pylab.figure(1)
    if myseq1 is None:
        myseq1 = pylab.imshow(image)
    else:
        myseq1.set_data(image)
    fig1.suptitle('Qimage #{}'.format(int(qframeNo)), fontsize=20)

    fig2 = pylab.figure(2)
    oimage = objectFile.get_data(int(cof))
    if myseq2 is None:
        myseq2 = pylab.imshow(oimage)
    else:
        myseq2.set_data(oimage)
    fig2.suptitle('Oimage #{}'.format(int(cof)), fontsize=20)
    pylab.pause(1)
    pylab.draw()
    print 'stop here1'"""
print 'stop here'
np.savetxt('outfile.sseq', frameToFrameSimIndex, delimiter=',',fmt="%d")
np.savetxt('outfile.smseq', frameToFrameSimDis, delimiter=',',fmt="%.4f")