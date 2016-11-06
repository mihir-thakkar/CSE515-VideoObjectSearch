import math
import numpy as np
from scipy.spatial.distance import cdist
import pylab
import imageio
import pandas as pd

#objectIndex = 1;
queryIndex = 2;

#fileIndex = np.genfromtxt('output.mvect.index', delimiter="=", dtype=None);
#fileIndex = dict(fileIndex)
#objectFile = imageio.get_reader('DataR/'+fileIndex[objectIndex],  'ffmpeg')
#queryFile = imageio.get_reader('DataR/'+fileIndex[queryIndex],  'ffmpeg')

database = np.loadtxt('output.mvect', delimiter=";");
t_database = np.column_stack((database[:,0:3],database[:,8]-database[:,6], database[:,9]-database[:,7]))
tr_database = t_database[(t_database[:,3]!=0) | (t_database[:,4]!=0),:];

#VI = np.cov(tr_database[:,2:5].T)

#df = pd.DataFrame(tr_database)
#s = df.groupby([0,1,2]).mean().reset_index();
#tr_database = s.values
query = tr_database[tr_database[:,0] == queryIndex,0:5];
qframeNos = np.transpose(np.unique(query[:,1]));

vdMat = np.array([]).reshape(0,2);
for objectIndex in range(1,14,1):
    object = tr_database[tr_database[:,0] == objectIndex,0:5];
    oframeNos = np.transpose(np.unique(object[:,1]));

    myseq1 = None;
    myseq2 = None;
    frameMeans = np.array([]).reshape(1,0);
    for qframeNo in np.nditer(qframeNos):
        qframe = query[query[:, 1] == qframeNo, 2:5];
        frameSim = np.array([]).reshape(0,3);
        for oframeNo in np.nditer(oframeNos):
            oframe = object[object[:, 1] == oframeNo, 2:5];
            frameD = cdist(qframe, oframe, 'mahalanobis');
            minD = np.amin(frameD,axis=1);
            meanD = np.mean(minD);
            medianD = np.median(minD);
            frameSim = np.vstack([frameSim, [oframeNo,meanD,medianD]])
        #frameSim = frameSim[np.argsort(frameSim[:, 2])]
        frameSim = frameSim[np.lexsort((frameSim[:, 1],frameSim[:, 2]))]
        #I = np.argmin(frameSim[:,2], axis=0)
        minF = frameSim[0,:];
        cof =  minF[0]
        frameMeans = np.column_stack((frameMeans, [minF[1]]))
        """image = queryFile.get_data(int(qframeNo))
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
        pylab.pause(0.5)
        pylab.draw()"""
        #print 'stop here1'
    vdMat = np.vstack([vdMat, [objectIndex,np.mean(frameMeans)]])
vdMat = vdMat[np.argsort(vdMat[:, 1])]
print vdMat
np.savetxt('test.csv', vdMat, delimiter=',',fmt="%d, %.4f")
print 'stop here'