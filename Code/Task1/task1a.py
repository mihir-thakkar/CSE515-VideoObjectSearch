import numpy as np

global CELL_NUM_COL, VIDEO_NUM_COL, FRAME_NUM_COL
CELL_NUM_COL = 2
VIDEO_NUM_COL = 0
FRAME_NUM_COL = 1

def preprocessing():

    global fileIndex, database, R
    #Original database
    database = np.loadtxt('../../Input/in_file.chst', delimiter=",")
    R = int(np.max(database[:, CELL_NUM_COL]))

    # Creating video name to video num index and reverse index
    fileIndex = np.genfromtxt('../../Input/in_file.index1', delimiter="=", dtype=None, skip_header=1)
    fileIndex = dict(fileIndex)

def normalizeCellEuclidean(file_one, file_two, bins):

    pixles_f1 = sum(file_one)
    pixles_f2 = sum(file_two)

    if bins == 1:
        return abs(pixles_f1-pixles_f2)
    else:
        return np.sqrt(pixles_f1 ** 2 + pixles_f2 ** 2)

def distanceFunctions(object, query, size_y, size_x):
    bins = size_x-3
    diff = 0

    for j in range(0, size_y):
        one_query_cell = query[j][3:]
        one_object_cell = object[j][3:]

        normal = normalizeCellEuclidean(one_object_cell, one_query_cell, bins)
        diff = diff + np.sqrt(sum((one_query_cell - one_object_cell)**2))/normal

    return diff


def computeSimilarity(queryIndex, objectIndex):

    # Get object
    object = database[database[:, VIDEO_NUM_COL] == objectIndex, :]
    # Get Query
    query = database[database[:, VIDEO_NUM_COL] == queryIndex, :]

    # Get frame numbers
    object_frame_number = object[-1,FRAME_NUM_COL]
    query_frame_number = query[-1, FRAME_NUM_COL]

    if object_frame_number > query_frame_number:
        difference = int(object_frame_number - query_frame_number)
        query_y, query_x = query.shape

        all_values = list()

        for i in range(0, int(difference+1)):
            sum_frames_front = 0.0
            for j in range(0, i):
                dis = distanceFunctions(object[((j) * R ):(R + (j) * R),:], query[0:R,:], R, query_x)
                sum_frames_front += dis

            sum_frames_end = 0.0
            for j in range(0, int(difference-i)):
                sum_frames_end = sum_frames_end + distanceFunctions(object[query_y+(j * R ): query_y+(R + j * R),:],
                                                                        query[query_y - R:query_y, :], R, query_x)

            distance_current = distanceFunctions(object[((i) * R ):(query_y + (i) * R)-1,:], query, query_y-1, query_x)

            all_values.append(((distance_current+sum_frames_front+sum_frames_end)/(object_frame_number*R)))

        diff = min(all_values)

    elif object_frame_number < query_frame_number:
        difference = query_frame_number - object_frame_number

    else:
        object_y, object_x = query.shape
        diff = (distanceFunctions(object, query, object_y, object_x) / object_y)

    return 1 -diff

if __name__ == '__main__':
    print 'Loading and Preprocessing database......'
    preprocessing()

    objectName = None;
    queryName = None
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
