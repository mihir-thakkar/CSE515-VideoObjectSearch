import numpy as np
from sklearn.cluster import KMeans

global INPUT_DB_PREFIX, INPUT_DB_SIFT, OUTPUT_KM_DB_SIFT, OUTPUT_KM_SCORE_SIFT
INPUT_DB_PREFIX = "../../Input/"
INPUT_DB_SIFT = "in_file.sift"
OUTPUT_KM_DB_SIFT = "in_file_d.skm"
OUTPUT_KM_SCORE_SIFT = "in_file_d.skm.score"

global START_COL, VIDEO_NUM_COL, FRAME_NUM_COL, CELL_NUM_COL, SIFT_DES_START
START_COL = 0
VIDEO_NUM_COL = 0
FRAME_NUM_COL = 1
CELL_NUM_COL = 2
SIFT_DES_START = 7
database = None
def preprocessing():
    global database
    database = np.loadtxt(INPUT_DB_PREFIX+INPUT_DB_SIFT, delimiter=",")

def reduce(d):
    allVectors = database[:, SIFT_DES_START:]
    kmeans = KMeans(n_clusters=d)
    kmeans.fit(allVectors)
    transformedKmeans = kmeans.transform(allVectors);
    kmeans_database = np.column_stack((database[:, VIDEO_NUM_COL:SIFT_DES_START], transformedKmeans))
    np.savetxt(INPUT_DB_PREFIX+OUTPUT_KM_DB_SIFT, kmeans_database, delimiter=',', fmt="%d,%d,%d" + ",%.4f" * d)
    score = kmeans.cluster_centers_
    score_mat = np.array([]).reshape(0, 3)
    for i in range(0, score.shape[0]):
        for j in range(0, score.shape[1]):
            score_mat = np.vstack([score_mat, [i + 1, j + 1, score[i, j]]])
    np.savetxt(INPUT_DB_PREFIX+OUTPUT_KM_SCORE_SIFT, score_mat, delimiter=',', fmt="%d,%d,%f")

if __name__ == '__main__':
    print 'Loading and Preprocessing database......'
    preprocessing()
    flag = 1
    while flag :
        d = int(input("Enter the target dimensionality: "))
        if d <=0 :
            print 'Target Dimensionality must be positive.'
        elif d > (database.shape[1]-7) :
            print 'Target Dimensionality must be less or equal to existing dimensionality.'
        else : flag = 0
    reduce(d)
