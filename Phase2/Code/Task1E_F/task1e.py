import numpy as np
from sklearn import preprocessing as pp
from scipy.spatial.distance import cdist

global START_COL, VIDEO_NUM_COL, FRAME_NUM_COL, CELL_NUM_COL, MV_DIR_COL, MV_SRCX_COL, MV_SRCY_COL, MV_DSTX_COL, MV_DSTY_COL
START_COL = 0
VIDEO_NUM_COL = 0
FRAME_NUM_COL = 1
CELL_NUM_COL = 2
MV_DIR_COL = 3
MV_SRCX_COL = 6
MV_SRCY_COL = 7
MV_DSTX_COL = 8
MV_DSTY_COL = 9

global MV_RX_COL, MV_RY_COL
MV_RX_COL = 3
MV_RY_COL = 4

database = None
def preprocessing():
    global fileIndex, revIndex, database, R
    #Original database
    original_database = np.loadtxt('../../Input/in_file.mvect', delimiter=",", skiprows=1)
    R = np.max(original_database[:, CELL_NUM_COL])
    transformedDatabase = original_database
    #Removed source, width, height and converted srcx, srcy, dstx, dsty to vector x and y magnitude
    transformedDatabase = np.column_stack((transformedDatabase[:, VIDEO_NUM_COL:CELL_NUM_COL+1], transformedDatabase[:, MV_DSTX_COL] - transformedDatabase[:, MV_SRCX_COL], transformedDatabase[:, MV_DSTY_COL] - transformedDatabase[:, MV_SRCY_COL]))
    #Removed zero motion vectors
    database_ired = transformedDatabase[(transformedDatabase[:, MV_RX_COL] != 0) | (transformedDatabase[:, MV_RY_COL] != 0), :]
    #Scaling motion vector lengths between 0 and 1
    scaler = pp.MinMaxScaler().fit(database_ired[:, MV_RX_COL:])
    database_ired = np.column_stack((database_ired[:, 0:MV_RX_COL], scaler.transform(database_ired[:, MV_RX_COL:])))
    database = database_ired

    #Creating video name to video num index and reverse index
    fileIndex = np.genfromtxt('../../Input/in_file.index', delimiter="=", dtype=None, skip_header=1)
    fileIndex = dict(fileIndex)
    revIndex = {v: k for k, v in fileIndex.iteritems()}

def computeSimilarity(queryIndex, objectIndex):
    #Object
    object = database[database[:, VIDEO_NUM_COL] == objectIndex, :]
    oFrameNos = np.transpose(np.unique(object[:, FRAME_NUM_COL]))

    #Query
    query = database[database[:, VIDEO_NUM_COL] == queryIndex, :]
    qFrameNos = np.transpose(np.unique(query[:, FRAME_NUM_COL]))

    frameMeans = np.array([]).reshape(1, 0)
    for qFrameNo in np.nditer(qFrameNos):
        qFrame = query[query[:, 1] == qFrameNo, CELL_NUM_COL:]
        qCellNos = np.transpose(np.unique(qFrame[:, 0]))
        frameSim = np.array([]).reshape(0, 2)
        for oFrameNo in np.nditer(oFrameNos):
            oFrame = object[object[:, 1] == oFrameNo, CELL_NUM_COL:]
            oCellNos = np.transpose(np.unique(oFrame[:, 0]))
            meanD = 0
            for cellNo in range(1, int(R+1)):
                qcExist = cellNo in oCellNos
                ocExist = cellNo in qCellNos
                #Calculating distance for cells which exist in both frames
                #Else distance is 1 as because one cell has motion and other has none
                if qcExist and ocExist:
                    #Euclidean distance comparison
                    frameD = cdist(qFrame[qFrame[:,0]==cellNo, 1:], oFrame[oFrame[:,0]==cellNo, 1:], 'euclidean')
                    #Most similar vectors
                    minD = np.amin(frameD, axis=1)
                    meanD += np.mean(minD)
                elif qcExist or ocExist:
                    meanD += 1
            meanD /= R
            frameSim = np.vstack([frameSim, [oFrameNo, meanD]])
        frameSim = frameSim[np.argsort(frameSim[:, 1])]
        frameMeans = np.column_stack((frameMeans, [frameSim[0, 1]]))
        oFrameNos = oFrameNos[oFrameNos != frameSim[0, 0]]
        if oFrameNos.size == 0 :
            break
    vidDistance = np.mean(frameMeans)
    vidSimilarity = 1 - vidDistance
    return vidSimilarity

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

