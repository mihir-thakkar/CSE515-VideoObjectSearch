import numpy as np
from sklearn.cluster import KMeans
from sklearn import preprocessing as pp

global INPUT_DB_PREFIX, INPUT_DB_MV, OUTPUT_KM_DB_MV, OUTPUT_KM_SCORE_MV
INPUT_DB_PREFIX = "../../Input/"
INPUT_DB_MV = "in_file.mvect"
OUTPUT_KM_DB_MV = "in_file_d.mkm"
OUTPUT_KM_SCORE_MV = "in_file_d.mkm.score"

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
#this will hold initially reduced database
database_ired = None
def preprocessing():
    global database, database_ired
    database = np.loadtxt(INPUT_DB_PREFIX + INPUT_DB_MV, delimiter=",", skiprows=1)
    transformedDatabase = np.column_stack((database[:, VIDEO_NUM_COL:CELL_NUM_COL + 1],
                                           database[:, MV_DSTX_COL] - database[:, MV_SRCX_COL],
                                           database[:, MV_DSTY_COL] - database[:, MV_SRCY_COL]))
    database_ired = transformedDatabase[
                    (transformedDatabase[:, MV_RX_COL] != 0) | (transformedDatabase[:, MV_RY_COL] != 0), :]
    # Scaling motion vector lengths between 0 and 1
    scaler = pp.MinMaxScaler().fit(database_ired[:, MV_RX_COL:])
    database_ired = np.column_stack((database_ired[:, 0:MV_RX_COL], scaler.transform(database_ired[:, MV_RX_COL:])))


def reduce(d):
    allVectors = database_ired[:, MV_RX_COL:]
    kmeans = KMeans(n_clusters=d)
    kmeans.fit(allVectors)
    transformedKmeans = kmeans.transform(allVectors);
    kmeans_database = np.column_stack((database_ired[:, VIDEO_NUM_COL:MV_RX_COL], transformedKmeans))
    np.savetxt(INPUT_DB_PREFIX + 'in_file_d.mkm', kmeans_database, delimiter=',', fmt="%d,%d,%d" + ",%.4f" * d)
    score = kmeans.cluster_centers_
    score_mat = np.array([]).reshape(0, 3)
    for i in range(0, score.shape[0]):
        for j in range(0, score.shape[1]):
            score_mat = np.vstack([score_mat, [i + 1, j + 1, score[i, j]]])
    np.savetxt(INPUT_DB_PREFIX + 'in_file_d.mkm.score', score_mat, delimiter=',', fmt="%d,%d,%f")

if __name__ == '__main__':
    print 'Loading and Preprocessing database......'
    preprocessing()
    flag = 1
    while flag :
        d = int(input("Enter the target dimensionality: "))
        if d <=0 :
            print 'Target Dimensionality must be positive.'
        elif d > (database_ired.shape[1]-3) :
            print 'Target Dimensionality must be less or equal to existing dimensionality.'
        else : flag = 0
    reduce(d)
