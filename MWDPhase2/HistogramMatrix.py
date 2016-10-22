import numpy as np
from scipy.spatial.distance import cdist

database = None
index_db = None

def preProcessing():
    global database
    database = np.loadtxt('../Input/in_file.chst', delimiter=",")
    global index_db
    index_db = np.genfromtxt('../Input/in_file.index', delimiter="=", dtype=None , skip_header=1)
    index_db = dict(index_db)

def getDistanceEuclidean( one_query_frame, two_query_frame, res):
    # type: (object, object, object) -> object
    total_distance = 0.0

    for j in range(0, res):
        one_query_cell = one_query_frame[j, 3:]
        two_query_cell = two_query_frame[j, 3:]

        normal = normalizeCellEuclidean(one_query_cell, two_query_cell, int(len(one_query_cell)))
        cell_distance = np.sqrt(sum((one_query_cell - two_query_cell)**2))

        total_distance = total_distance + cell_distance/normal

    return total_distance/res

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

def normalizeCellEuclidean(file_one, file_two, bins):

    pixles_f1 = sum(file_one)
    pixles_f2 = sum(file_two)

    if bins == 1:
        return abs(pixles_f1-pixles_f2)
    else:
        return np.sqrt(pixles_f1 ** 2 + pixles_f2 ** 2)

def normalizeCellQuadratic(file_one, file_two, simMatrix, bins):
    pixles_f1 = sum(file_one)
    pixles_f2 = sum(file_two)

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

if __name__ == '__main__':

    preProcessing()
    # will be inputs to the function
    a = 1
    b = 10
    query_number = 1
    object_file = 1

    # Get the frames to compare
    query_file = database[database[:, 0] == query_number, :]
    query_file_frames = query_file[query_file[:, 1] <= b, :]
    query_file_frames = query_file_frames[query_file_frames[:, 1] >= a, :]
    object_file = database[database[:, 0] == object_file, :]

    # Gets the max object frames
    max_object_frames = int(object_file[-1, 1])

    # Get the number for r
    res = int(object_file[-1, 2])

    # Gets the distance matrix
    distanceMatrix = list()

    # Start frames to frames
    for i in range(a, b):
        one_query_frame = query_file_frames[query_file_frames[:, 1] == i, :]
        add_list = list()

        for j in range(1, max_object_frames):
            two_query_frame = object_file[object_file[:, 1] == j, :]

            # Compare the distance
            distance = getDistanceQuadratic(one_query_frame, two_query_frame, res)

            add_list.append(distance)

        distanceMatrix.append(add_list)
