import numpy as np
import sys
from scipy.spatial.distance import cdist

def NormalEuclidean( q_height, q_width, o_height, o_width):

    max_height = max([q_height, o_height]) - 8
    max_width = max([q_width, o_width]) - 8
    max_value = np.sqrt(max_height ** 2 + max_width ** 2)

    return max_value

def DistanceFunction(objectIndex, queryIndex ,database_file):

    database = np.loadtxt(database_file, delimiter=";")
    t_database = np.column_stack((database[:, 0:3], database[:, 8] - database[:, 6], database[:, 9] - database[:, 7]))
    tr_database = t_database[(t_database[:, 3] != 0) | (t_database[:, 4] != 0), :]

    query = tr_database[tr_database[:, 0] == queryIndex, 0:5]
    qframeNos = np.transpose(np.unique(query[:, 1]))
    q_height = max(database[database[:, 0] == queryIndex, 9])
    q_width = max(database[database[:, 0] == queryIndex, 8])

    vdMat = np.array([]).reshape(0, 2)
    object = tr_database[tr_database[:, 0] == objectIndex, 0:5]
    oframeNos = np.transpose(np.unique(object[:, 1]))

    o_height = max(database[database[:, 0] == objectIndex, 9])
    o_width = max(database[database[:, 0] == objectIndex, 8])

    normal = NormalEuclidean(q_height, q_width, o_height, o_width)

    frameMeans = np.array([]).reshape(1, 0)
    for qframeNo in np.nditer(qframeNos):
        qframe = query[query[:, 1] == qframeNo, 2:5]
        frameSim = np.array([]).reshape(0, 3)
        for oframeNo in np.nditer(oframeNos):
            oframe = object[object[:, 1] == oframeNo, 2:5]

            frameD = cdist(qframe, oframe, 'euclidean')
            frameD = np.divide(frameD, normal)

            minD = np.amin(frameD, axis=1)
            meanD = np.mean(minD)
            medianD = np.median(minD)
            frameSim = np.vstack([frameSim, [oframeNo, meanD, medianD]])

        frameSim = frameSim[np.lexsort((frameSim[:, 1], frameSim[:, 2]))]

        minF = frameSim[0, :]
        frameMeans = np.column_stack((frameMeans, [minF[1]]))
    vdMat = np.vstack([vdMat, [objectIndex, np.mean(frameMeans)]])
    vdMat = vdMat[np.argsort(vdMat[:, 1])]

    return vdMat[0]

if __name__ == '__main__':
    objectIndex = int(sys.argv[1])
    queryIndex = int(sys.argv[2])
    database_file = str(sys.argv[3])
    sys.stdout.write(str(DistanceFunction(objectIndex,queryIndex, database_file)))