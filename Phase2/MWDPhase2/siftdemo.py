import numpy as np
from scipy.spatial.distance import cdist

database = np.loadtxt('output.sift', delimiter=";");
objectIndex = 1;
queryIndex = 2;

object = database[database[:,0] == objectIndex,0:135];
oframeNos = np.transpose(np.unique(object[:,1]));

query = database[database[:,0] == queryIndex,0:135];
qframeNos = np.transpose(np.unique(query[:,1]));

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
    #frameSim = frameSim[np.argsort(frameSim[:, 2])]
    I = np.argmin(frameSim[:,2], axis=0)
    minF = frameSim[I,:];
    print 'stop here1'
print 'stop here'