import numpy as np
from scipy.spatial.distance import cdist

global START_COL, VIDEO_NUM_COL, FRAME_NUM_COL, CELL_NUM_COL, MV_DIR_COL, MV_SRCX_COL, MV_SRCY_COL, MV_DSTX_COL, MV_DSTY_COL
START_COL = 0
VIDEO_NUM_COL = 0
FRAME_NUM_COL = 1
CELL_NUM_COL = 2

global MV_RX_COL, MV_RY_COL
MV_RX_COL = 3
MV_RY_COL = 4

database = None
def preprocessing():

    global fileIndex, revIndex, database, R
    #Original database
    database = np.loadtxt('../../Input/in_file.sift.txt', delimiter=",")

    #Creating video name to video num index and reverse index
    fileIndex = np.genfromtxt('../../Input/in_file.index', delimiter="=", dtype=None, skip_header=1)
    fileIndex = dict(fileIndex)
    revIndex = {v: k for k, v in fileIndex.iteritems()}

def computeSimilarity(queryIndex, objectIndex):

    object = database[database[:, 0] == objectIndex, 0:135];
    oframeNos = np.transpose(np.unique(object[:, 1]));

    query = database[database[:, 0] == queryIndex, 0:135];
    qframeNos = np.transpose(np.unique(query[:, 1]));

    frameMeans = np.array([]).reshape(1, 0)
    for qframeNo in np.nditer(qframeNos):
        qframe = query[query[:, 1] == qframeNo, 7:135];
        frameSim = np.array([]).reshape(0, 2);
        for oframeNo in np.nditer(oframeNos):
            oframe = object[object[:, 1] == oframeNo, 7:135];
            frameD = cdist(qframe, oframe, 'euclidean');

            frameD = frameD[np.argsort(frameD, axis= 0)]
            matches = frameD[(frameD[:,1] / frameD[:,0] > 1.5)]
            sim = len(matches) / len(qframe)

            frameSim = np.vstack([frameSim, [oframeNo, sim]])
        frameSim = frameSim[np.argsort(frameSim[:, 1])]
        frameMeans = np.column_stack((frameMeans, [frameSim[0, 1]]))
    vidDistance = np.mean(frameMeans)
    return vidDistance

if __name__ == '__main__':
    print 'Loading and Preprocessing database......'
    preprocessing()
    objectName = None; queryName=None
    while 1:
        while 1:
            objectName = raw_input("Enter the object file name: ")
            if objectName in fileIndex:
                break
            else:
                print 'Given file name does not exist in database.'
        while 1:
            queryName = raw_input("Enter the query file name: ")
            if queryName in fileIndex:
                break
            else:
                print 'Given file name does not exist in database.'
        print computeSimilarity(fileIndex[queryName], fileIndex[objectName])
        cont = raw_input("Do you want to continue, y/n: ")
        if cont == 'n':
            break