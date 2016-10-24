import numpy as np
from scipy.spatial.distance import cdist

global START_COL, VIDEO_NUM_COL, FRAME_NUM_COL, CELL_NUM_COL, SIFT_DES_START
START_COL = 0
VIDEO_NUM_COL = 0
FRAME_NUM_COL = 1
CELL_NUM_COL = 2
SIFT_DES_START = 7

database = None
def preprocessing():
    global fileIndex, revIndex, database, R
    #Original database
    database = np.loadtxt('../../Input/in_file.sift', delimiter=",")

    #Creating video name to video num index and reverse index
    fileIndex = np.genfromtxt('../../Input/in_file.index', delimiter="=", dtype=None, skip_header=1)
    fileIndex = dict(fileIndex)
    revIndex = {v: k for k, v in fileIndex.iteritems()}

def computeSimilarity(queryIndex, objectIndex):
    object = database[database[:, VIDEO_NUM_COL] == objectIndex, VIDEO_NUM_COL:]
    oframeNos = np.transpose(np.unique(object[:, FRAME_NUM_COL]))

    query = database[database[:, VIDEO_NUM_COL] == queryIndex, VIDEO_NUM_COL:]
    qframeNos = np.transpose(np.unique(query[:, FRAME_NUM_COL]))

    frameMeans = np.array([]).reshape(1, 0)
    for qframeNo in np.nditer(qframeNos):
        qframe = query[query[:, FRAME_NUM_COL] == qframeNo, SIFT_DES_START:]
        frameDist = np.array([]).reshape(0, 2)
        for oframeNo in np.nditer(oframeNos):
            oframe = object[object[:, FRAME_NUM_COL] == oframeNo, SIFT_DES_START:]
            frameD = cdist(qframe, oframe, 'euclidean')
            minD = np.amin(frameD, axis=1)
            meanD = np.mean(minD)
            frameDist = np.vstack([frameDist, [oframeNo, meanD]])
        frameDist = frameDist[np.argsort(frameDist[:, 1])]
        frameMeans = np.column_stack((frameMeans, [frameDist[0, 1]]))
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