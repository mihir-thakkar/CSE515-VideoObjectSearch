import math
import numpy as np
from scipy.spatial.distance import cdist
import pylab
import imageio

objectIndex = 1;
queryIndex = 5;

fileIndex = np.genfromtxt('output.hist.index', delimiter="=", dtype=None);
fileIndex = dict(fileIndex)
objectFile = imageio.get_reader('DataR/'+fileIndex[objectIndex],  'ffmpeg')
queryFile = imageio.get_reader('DataR/'+fileIndex[queryIndex],  'ffmpeg')

tr_database = np.loadtxt('histogram.txt', delimiter=",");
#t_database = np.column_stack((database[:,0:3],database[:,8]-database[:,6], database[:,9]-database[:,7]))
#tr_database = t_database[(t_database[:,3]!=0) | (t_database[:,4]!=0),:];


object = tr_database[tr_database[:,0] == objectIndex,0:13];
oframeNos = np.transpose(np.unique(object[:,1]));

query = tr_database[tr_database[:,0] == queryIndex,0:13];
qframeNos = np.transpose(np.unique(query[:,1]));

myseq1 = None;
myseq2 = None;
for qframeNo in np.nditer(qframeNos):
    qframe = query[query[:, 1] == qframeNo, 3:13];
    frameSim = np.array([]).reshape(0,3);
    for oframeNo in np.nditer(oframeNos):
        oframe = object[object[:, 1] == oframeNo, 3:13];
        frameD = np.array([]).reshape(0,1);
        for i in range(0,16,1):
            frameD = np.vstack([frameD, cdist([qframe[i,:]], [oframe[i,:]], 'euclidean')])
            print "Stop"
        #frameD = cdist(qframe, oframe, 'euclidean');
        #minD = np.amin(frameD,axis=1);
        meanD = np.mean(frameD);
        medianD = np.median(frameD);
        frameSim = np.vstack([frameSim, [oframeNo,meanD,medianD]])
    #frameSim = frameSim[np.argsort(frameSim[:, 2])]
    frameSim = frameSim[np.lexsort((frameSim[:, 1],frameSim[:, 2]))]
    #I = np.argmin(frameSim[:,2], axis=0)
    minF = frameSim[0,:];
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
    print 'stop here1'
print 'stop here'