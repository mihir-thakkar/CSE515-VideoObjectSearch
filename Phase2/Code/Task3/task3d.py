import numpy as np
from sklearn.cluster import KMeans

global INPUT_DB_PREFIX, INPUT_DB_CH, OUTPUT_KM_DB_CH, OUTPUT_KM_SCORE_CH
INPUT_DB_PREFIX = "../../Input/"
INPUT_DB_CH = "in_file.chst"
OUTPUT_KM_DB_CH = "in_file_d.ckm"
OUTPUT_KM_SCORE_CH = "in_file_d.ckm.score"

global START_COL, VIDEO_NUM_COL, FRAME_NUM_COL, CELL_NUM_COL, CH_VC_START
START_COL = 0
VIDEO_NUM_COL = 0
FRAME_NUM_COL = 1
CELL_NUM_COL = 2
CH_VC_START = 3

database = None
def preprocessing():
    global database
    database = np.loadtxt(INPUT_DB_PREFIX+INPUT_DB_CH, delimiter=",")

def reduce(d):
    allVectors = database[:, CH_VC_START:]
    kmeans = KMeans(n_clusters=d)
    kmeans.fit(allVectors)
    transformedKmeans = kmeans.transform(allVectors);
    kmeans_database = np.column_stack((database[:, VIDEO_NUM_COL:CH_VC_START], transformedKmeans))
    np.savetxt(INPUT_DB_PREFIX+OUTPUT_KM_DB_CH, kmeans_database, delimiter=',', fmt="%d,%d,%d" + ",%.4f" * d)
    score = kmeans.cluster_centers_
    score_mat = np.array([]).reshape(0, 3)
    for i in range(0, score.shape[0]):
        for j in range(0, score.shape[1]):
            score_mat = np.vstack([score_mat, [i + 1, j + 1, score[i, j]]])
    np.savetxt(INPUT_DB_PREFIX+OUTPUT_KM_SCORE_CH, score_mat, delimiter=',', fmt="%d,%d,%f")

if __name__ == '__main__':
    print 'Loading and Preprocessing database......'
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
