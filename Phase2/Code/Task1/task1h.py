import numpy as np
from sklearn import preprocessing as pp
from scipy.spatial.distance import cdist

global START_COL, VIDEO_NUM_COL, FRAME_NUM_COL, CELL_NUM_COL, MV_DIR_COL, MV_SRCX_COL, MV_SRCY_COL, MV_DSTX_COL, MV_DSTY_COL, SIFT_DES_START, CH_START_COL
START_COL = 0
VIDEO_NUM_COL = 0
FRAME_NUM_COL = 1
CELL_NUM_COL = 2
MV_DIR_COL = 3
MV_SRCX_COL = 6
MV_SRCY_COL = 7
MV_DSTX_COL = 8
MV_DSTY_COL = 9

SIFT_DES_START = 7
CH_START_COL = 3

global MV_RX_COL, MV_RY_COL
MV_RX_COL = 3
MV_RY_COL = 4

global INPUT_DB_PREFIX, INPUT_DB_CH, INPUT_DB_SIFT
INPUT_DB_PREFIX = "../../Input/"
INPUT_DB_CH = "in_file.chst"
INPUT_DB_SIFT = "in_file.sift"

global CH_WGT, SIFT_WGT, MV_WGT
CH_WGT = 0.35
SIFT_WGT = 0.45
MV_WGT = 0.30

database = None
def preprocessing():
    global fileIndex, revIndex, mv_database, R, sf_database, ch_database
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
    mv_database = database_ired

    ch_database = np.loadtxt(INPUT_DB_PREFIX + INPUT_DB_CH, delimiter=",")

    sf_database = np.loadtxt(INPUT_DB_PREFIX + INPUT_DB_SIFT, delimiter=",")

    #Creating video name to video num index and reverse index
    fileIndex = np.genfromtxt('../../Input/in_file.index', delimiter="=", dtype=None, skip_header=1)
    fileIndex = dict(fileIndex)
    revIndex = {v: k for k, v in fileIndex.iteritems()}

def getDistanceQuadratic( one_query_frame, two_query_frame, res):
    total_distance = 0.0

    # Get the sim matrix
    bins = int(len(one_query_frame[1, 3:]))
    simMatrix = similaritiyMatrix(bins)

    # Compute the distance for each cell
    for j in range(0, res):
        one_query_cell = one_query_frame[j, 3:]
        two_query_cell = two_query_frame[j, 3:]

        normal = normalizeCellQuadratic(one_query_cell, two_query_cell, simMatrix, bins)
        diffMat = one_query_cell - two_query_cell
        cell_distance = np.sqrt(np.dot(diffMat.T, np.dot(simMatrix,diffMat)))

        total_distance = total_distance + cell_distance/normal

    return total_distance/res

def similaritiyMatrix (bins):

    # Initialize the similaritiy matrix
    simMatrix = np.ones((bins, bins))

    # Edges
    edges = np.ones((bins+1, 1))
    mid_edges = np.ones((bins, 1))

    # Compute the edges
    edges[0] = 0
    dis_edges = 255 / float(bins)

    for edges_i in range(1, bins+1):
        edges[edges_i] = edges[edges_i-1] + dis_edges

    # Compute the midpoints
    for mid_i in range(0, bins):
        mid_edges[mid_i] = (edges[mid_i] + edges[mid_i+1]) /2

    # Compute the Matrix
    for tall in range(0, bins):
        for wide in range(0, bins):
            simMatrix[tall][wide] = abs(mid_edges[tall] - mid_edges[wide])

    simMatrix = 1 - simMatrix / 255

    return simMatrix

def normalizeCellQuadratic(file_one, file_two, simMatrix, bins):
    pixles_f1 = sum(abs(file_one))
    pixles_f2 = sum(abs(file_two))

    if bins == 1:
        return abs(pixles_f1 - pixles_f2)
    else:
        f1_vector = np.zeros((1, bins))
        f2_vector = np.zeros((1, bins))
        f1_vector[0][0] = pixles_f1
        f2_vector[0][-1] = pixles_f2

        diffMat = f1_vector - f2_vector
        results = np.dot(np.dot(diffMat, simMatrix),diffMat.T)

        return results

def computeMVSimilarity(queryIndex, objectIndex):
    #Object
    object = mv_database[mv_database[:, VIDEO_NUM_COL] == objectIndex, :]
    oFrameNos = np.transpose(np.unique(object[:, FRAME_NUM_COL]))

    #Query
    query = mv_database[mv_database[:, VIDEO_NUM_COL] == queryIndex, :]
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
                    frameD = cdist(qFrame[qFrame[:,0]==cellNo, 1:], oFrame[oFrame[:,0]==cellNo, 1:], 'jaccard')
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

def computeSiftSimilarity(queryIndex, objectIndex):
    object = sf_database[sf_database[:, VIDEO_NUM_COL] == objectIndex, VIDEO_NUM_COL:]
    oframeNos = np.transpose(np.unique(object[:, FRAME_NUM_COL]))

    query = sf_database[sf_database[:, VIDEO_NUM_COL] == queryIndex, VIDEO_NUM_COL:]
    qframeNos = np.transpose(np.unique(query[:, FRAME_NUM_COL]))

    frameMeans = np.array([]).reshape(1, 0)
    for qframeNo in np.nditer(qframeNos):
        qframe = query[query[:, FRAME_NUM_COL] == qframeNo, SIFT_DES_START:]
        frameDist = np.array([]).reshape(0, 2)
        for oframeNo in np.nditer(oframeNos):
            oframe = object[object[:, FRAME_NUM_COL] == oframeNo, SIFT_DES_START:]
            frameD = cdist(qframe, oframe, 'cosine')
            minD = np.amin(frameD, axis=1)
            meanD = np.mean(minD)
            frameDist = np.vstack([frameDist, [oframeNo, meanD]])
        frameDist = frameDist[np.argsort(frameDist[:, 1])]
        frameMeans = np.column_stack((frameMeans, [frameDist[0, 1]]))
    vidDistance = np.mean(frameMeans)
    vidSimilarity = 1 - vidDistance
    return vidSimilarity

def computeCHSimilarity(queryIndex, objectIndex):
    object = ch_database[ch_database[:, VIDEO_NUM_COL] == objectIndex, VIDEO_NUM_COL:]
    oframeNos = np.transpose(np.unique(object[:, FRAME_NUM_COL]))

    # Get the number for r
    res = int(object[-1, 2])

    query = ch_database[ch_database[:, VIDEO_NUM_COL] == queryIndex, VIDEO_NUM_COL:]
    qframeNos = np.transpose(np.unique(query[:, FRAME_NUM_COL]))

    frameMeans = np.array([]).reshape(1, 0)
    for qframeNo in np.nditer(qframeNos):
        qframe = query[query[:, FRAME_NUM_COL] == qframeNo, :]
        frameDist = np.array([]).reshape(0, 2)
        for oframeNo in np.nditer(oframeNos):
            oframe = object[object[:, FRAME_NUM_COL] == oframeNo, :]
            distance = getDistanceQuadratic(qframe, oframe, res)
            frameDist = np.vstack([frameDist, [oframeNo, distance]])
        frameDist = frameDist[np.argsort(frameDist[:, 1])]
        frameMeans = np.column_stack((frameMeans, [frameDist[0, 1]]))
        oframeNos = oframeNos[oframeNos != frameDist[0, 0]]
        if oframeNos.size == 0:
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
        chSim = computeCHSimilarity(fileIndex[queryName], fileIndex[objectName])
        siftSim = computeSiftSimilarity(fileIndex[queryName], fileIndex[objectName])
        mvSim = computeMVSimilarity(fileIndex[queryName], fileIndex[objectName])
        ovSim = CH_WGT*chSim + SIFT_WGT*siftSim + MV_WGT*mvSim
        print ovSim
        cont = raw_input("Do you want to continue, y/n: ")
        if cont == 'n':
            break

