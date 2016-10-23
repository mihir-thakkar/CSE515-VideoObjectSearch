import numpy as np
import imageio
import os
import shutil
from scipy.spatial.distance import cdist
from sklearn import preprocessing as pp
import re

global START_COL, VIDEO_NUM_COL, FRAME_NUM_COL, CELL_NUM_COL
START_COL = 0
VIDEO_NUM_COL = 0
FRAME_NUM_COL = 1
CELL_NUM_COL = 3

global SEQ_BREAK_THRESHOLD, MIN_FRAMES_PREC
SEQ_BREAK_THRESHOLD = 5
MIN_FRAMES_PREC = 0.25

global INPUT_PREFIX, INPUT_DB_CH, INPUT_DB_INDEX, INPUT_VIDEO_PREFIX, SEQ_PREFIX
INPUT_DB_PREFIX = "../../Input/"
INPUT_DB_CH = "in_file.chst"
INPUT_DB_INDEX = "in_file.index"
INPUT_VIDEO_PREFIX = "../../Input/Videos/"
SEQ_PREFIX = "../../Output/Seq/"

def preprocessing():
    global fileIndex, revIndex, database
    # Reading database
    database = np.loadtxt(INPUT_DB_PREFIX+INPUT_DB_CH, delimiter=",")

    #Creating file index
    fileIndex = np.genfromtxt(INPUT_DB_PREFIX+INPUT_DB_INDEX, delimiter="=", dtype=None, skip_header=1)
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
        cell_distance = np.sqrt(sum((one_query_cell - two_query_cell)**2))

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
        f2_vector = np.zeros((bins, 1))
        f1_vector[0][0] = pixles_f1
        f2_vector[-1] = pixles_f2

        results = np.multiply(f1_vector, simMatrix)
        results = np.multiply(f2_vector, results)

        return np.sqrt(results[-1][0])


def computeDistance(object, query, a, b):

    # Gets the max object frames
    max_object_frames = int(object[-1, FRAME_NUM_COL])

    # Get the number for r
    res = int(object[-1, 2])

    # Gets the distance matrix
    oframeNos = np.transpose(np.unique(object[:, FRAME_NUM_COL]))
    frameToFrameIndex = np.array([]).reshape(0, oframeNos.size)
    frameToFrameDist = np.array([]).reshape(0, oframeNos.size)

    # Start frames to frames
    for i in range(a, b+1):
        one_query_frame = query[query[:, FRAME_NUM_COL] == i, :]
        frameDist = np.array([]).reshape(0, 2)

        for j in range(1, max_object_frames+1):
            two_query_frame = object[object[:, FRAME_NUM_COL] == j, :]

            # Compare the distance
            distance = getDistanceQuadratic(one_query_frame, two_query_frame, res)
            frameDist = np.vstack([frameDist, [j, distance]])

        # Sort and get frameToFrameIndex and frameToFrameDist
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
    objectIndexes = fileIndex.values(); objectIndexes.remove(queryIndex);
    for objectIndex in objectIndexes:
        object = database[database[:, VIDEO_NUM_COL] == objectIndex, 0:]
        all_seq_from_object = np.array([]).reshape(0, 4)
        # Call function here and get these two matrix
        (frameToFrameIndex, frameToFrameDist) = computeDistance(object, query, a, b)
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
                                    for conflict in range(int(r - diff + 1), r):
                                        filter = np.where((frameToFrameIndex[conflict, :] == lastFNo + 1))
                                        if (filter[0].size != 0):
                                            nearest_frame_col = filter[0][0];
                                            seq[conflict] = frameToFrameIndex[conflict, nearest_frame_col];
                                            lastFNo = seq[conflict];
                                            seqDist[conflict] = frameToFrameDist[r, nearest_frame_col];
            all_seq_from_object = np.vstack([all_seq_from_object, [objectIndex, np.mean(seqDist), seq[0], seq[-1]]])

        # Calculating top k sequences from this object and finally adding to all sequences
        # and again reducing to final k in database
        all_seq_from_object = all_seq_from_object[(all_seq_from_object[:, 3]-all_seq_from_object[:, 2]) > ((b-a+1)*MIN_FRAMES_PREC), :]
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
    saveAndShowSubsequence(queryIndex, a, b, allSeq)

def saveAndShowSubsequence(queryIndex, a, b, kseq):
    qFileName = re.sub('\.mp4$', '', revIndex[int(queryIndex)])
    seqDir = SEQ_PREFIX + qFileName + '_a_'+ `int(a)` + '_b_' + `int(b)`+ '_k_' + `int(k)` + '/'
    if not os.path.exists(seqDir):
        os.makedirs(seqDir)
    else :
        shutil.rmtree(seqDir)
        os.makedirs(seqDir)
    #Saving query seq
    objectFile = imageio.get_reader(INPUT_VIDEO_PREFIX + revIndex[int(queryIndex)], 'ffmpeg')
    writer = imageio.get_writer(seqDir + 'querySeq.mp4', fps=30)
    for i in range(int(a), int(b + 1)):
        oimage = objectFile.get_data(i)
        writer.append_data(oimage)
    writer.close()

    # Saving found seq
    for index, row in enumerate(kseq):
        objectFile = imageio.get_reader(INPUT_VIDEO_PREFIX + revIndex[int(row[0])], 'ffmpeg')
        writer = imageio.get_writer(seqDir + 'seq' + `index` + ' fn' + `int(row[2])` + '-' + `int(row[3])` + ' ' + revIndex[int(row[0])], fps=30)
        for i in range(int(row[2]), int(row[3] + 1)):
            oimage = objectFile.get_data(i)
            writer.append_data(oimage)
        writer.close()

if __name__ == '__main__':
    print 'Loading and Preprocessing database......'
    preprocessing()
    while 1:
        while 1:
            queryFileName = raw_input("Enter the query file name: ")
            if queryFileName in fileIndex:
                a = int(input("Enter the query sequence start frame num: "))
                b = int(input("Enter the query sequence end frame num: "))
                k = int(input("Enter the k : "))
                if k <= 0:
                    print 'k must be positive.'
                else:
                    break
            else:
                print 'Given file name does not exist in database.'
        findSubsequence(fileIndex[queryFileName], a, b, k)
        print "Please check sequences in Output folder."
        print "************************************************"
        print "************************************************"
        cont = raw_input("Do you want to continue, y/n: ")
        if cont == 'n':
            break