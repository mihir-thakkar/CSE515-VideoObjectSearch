import math
import numpy as np
from scipy.spatial.distance import cdist
import pylab
import imageio

global START_COL, VIDEO_NUM_COL, FRAME_NUM_COL, CELL_NUM_COL, SEQ_BREAK_THRESHOLD, SIFT_VECTOR_START_COL
START_COL = 0
VIDEO_NUM_COL = 0
FRAME_NUM_COL = 1
CELL_NUM_COL = 3
SEQ_BREAK_THRESHOLD = 5
SIFT_VECTOR_START_COL = 7



def preprocessing():
    global fileIndex, revIndex, database
    # Reading database
    database = np.loadtxt('output.sift', delimiter=";")

    #Creating file index
    fileIndex = np.genfromtxt('output.sift.index', delimiter="=", dtype=None)
    fileIndex = dict(fileIndex)
    revIndex = dict([i.reverse() for i in fileIndex])

def myMethod(object, query):
    oframeNos = np.transpose(np.unique(object[:, FRAME_NUM_COL]))
    qframeNos = np.transpose(np.unique(query[:, FRAME_NUM_COL]))
    frameToFrameIndex = np.array([]).reshape(0, oframeNos.size)
    frameToFrameDist = np.array([]).reshape(0, oframeNos.size)
    for qframeNo in np.nditer(qframeNos):
        qframe = query[query[:, 1] == qframeNo, SIFT_VECTOR_START_COL:]
        frameDist = np.array([]).reshape(0, 3)
        for oframeNo in np.nditer(oframeNos):
            oframe = object[object[:, 1] == oframeNo, SIFT_VECTOR_START_COL:];
            frameD = cdist(qframe, oframe, 'euclidean');
            minD = np.amin(frameD, axis=1);
            meanD = np.mean(minD);
            medianD = np.median(minD);
            frameDist = np.vstack([frameDist, [oframeNo, meanD, medianD]])
        frameDist = frameDist[np.argsort(frameDist[:, 1])]
        frameToFrameIndex = np.vstack([frameToFrameIndex, frameDist[:, 0].T])
        frameToFrameDist = np.vstack([frameToFrameDist, frameDist[:, 1].T])
    return (frameToFrameIndex, frameToFrameDist)

def findSubsequence(queryIndex, a, b, k):
    # Reading query object
    query = database[database[:, VIDEO_NUM_COL] == queryIndex, 0:]
    # Reading query sequence from query object and saving to query var
    query = query[(a <= query[:, FRAME_NUM_COL]) & (query[:, FRAME_NUM_COL] <= b), 0:]

    # Will store all sequences in this
    allSeq = np.array([]).reshape(0, 4)
    #Other objects
    objectIndexes = fileIndex.values().remove(queryIndex)
    for objectIndex in objectIndexes:
        object = database[database[:, VIDEO_NUM_COL] == objectIndex, 0:]
        all_seq_from_object = np.array([]).reshape(0, 4)
        # Call function here and get these two matrix
        (frameToFrameIndex, frameToFrameDist) = myMethod(object, query)
        (rowLen, colLen) = frameToFrameIndex.shape
        for c in range(0, colLen):
            seq = np.array([])
            seqIndex = np.array([])
            seqDist = np.array([])
            for r in range(0, rowLen):
                if r == 0:
                    seq = np.append(seq, frameToFrameIndex[r, c])
                    seqIndex = np.append(seqIndex, r)
                    seqDist = np.append(seqDist, frameToFrameDist[r, c])
                else:
                    # Checking for only greater and equal frames from sequence perspective
                    filter = np.where((frameToFrameIndex[r, :] >= (seq[-1])))
                    if (filter[0].size != 0):
                        nextFrames = frameToFrameIndex[r, filter][0]
                        # Nearest frame initial assignment which has least distance
                        nearest_frame = nextFrames[0]
                        # Initial assignment of nearest frame and same frame index
                        nearest_frame_idx = 0;
                        same_frame_idx = 0
                        for fIndex, f in enumerate(nextFrames):
                            if (f == seq[-1]):
                                same_frame_idx = fIndex
                                break
                            if (f > seq[-1] and f < nearest_frame):
                                nearest_frame = f
                                nearest_frame_idx = fIndex

                        # If nearest frame breaking sequence, sticking to same frame
                        if ((nearest_frame - seq[-1]) > SEQ_BREAK_THRESHOLD):
                            nearest_frame_idx = same_frame_idx
                        nearest_frame_col = filter[0][nearest_frame_idx];
                        seq = np.append(seq, frameToFrameIndex[r, nearest_frame_col]);
                        seqDist = np.append(seqDist, frameToFrameDist[r, nearest_frame_col]);
                        if (seq[-1] != seq[-2]):
                            seqIndex = np.append(seqIndex, r)
                            # Found different frame with sequence jumping
                            # Trying to balance similarity with adding missed frames distance if possible
                            if ((seqIndex[-1] - seqIndex[-2]) > 1):
                                start = seq[-2]
                                end = seq[-1]
                                diff = seq[-1] - seq[-2]
                                # Frame similarity can only be balanced if enough space is present
                                if ((r - diff + 1) > 0):
                                    lastFNo = start
                                    for k in range(int(r - diff + 1), r):
                                        filter = np.where((frameToFrameIndex[k, :] == lastFNo + 1))
                                        if (filter[0].size != 0):
                                            nearest_frame_col = filter[0][0];
                                            seq[k] = frameToFrameIndex[k, nearest_frame_col];
                                            lastFNo = seq[k];
                                            seqDist[k] = frameToFrameDist[r, nearest_frame_col];
            all_seq_from_object = np.vstack([allSeq, [objectIndex, np.mean(seqDist), seq[0], seq[-1]]])

        # Calculating top k sequences from this object and finally adding to all sequences
        # and again reducing to final k in database
        all_seq_from_object = all_seq_from_object[np.argsort(all_seq_from_object[:, 1])]
        final_seq_from_object = np.array([]).reshape(0, 4);
        for v in np.unique(all_seq_from_object[:, 3]):
            firstLSeq = (all_seq_from_object[all_seq_from_object[:, 3] == v, :])[0, :]
            final_seq_from_object = np.vstack([final_seq_from_object, firstLSeq])
        final_seq_from_object = final_seq_from_object[np.argsort(final_seq_from_object[:, 1])]
        final_seq_from_object = final_seq_from_object[0:k,:]
        allSeq = np.vstack([allSeq, final_seq_from_object])
        allSeq = allSeq[np.argsort(allSeq[:, 1])]
        allSeq = allSeq[0:k, :]
    saveAndShowSubsequence(allSeq)

def saveAndShowSubsequence(kseq):
    for index, row in enumerate(kseq):
        objectFile = imageio.get_reader('DataR/' + revIndex[int(row[1])], 'ffmpeg')
        writer = imageio.get_writer('seq' + `index` + ' fn' + `int(row[2])` + '-' + `int(row[3])` + ' ' + `revIndex[int(row[1])]`, fps=30)
        for i in range(int(row[2]), int(row[3] + 1)):
            oimage = objectFile.get_data(i)
            writer.append_data(oimage)
        writer.close();

if __name__ == '__main__':
    preprocessing()
    flag = 1
    while flag :
        d = int(input("Enter the target dimensionality: "))
        if d <=0 :
            print 'Target Dimensionality must be positive.'
        elif d > (database.shape[1]-3) :
            print 'Target Dimensionality must be less or equal to existing dimensionality.'
        else : flag = 0
    reduce(d)


