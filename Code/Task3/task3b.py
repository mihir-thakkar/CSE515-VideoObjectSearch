import numpy as np
from sklearn.decomposition import PCA

global INPUT_DB_PREFIX, INPUT_DB_SIFT, OUTPUT_PCA_DB_SIFT, OUTPUT_PCA_SCORE_SIFT
INPUT_DB_PREFIX = "../../Input/"
INPUT_DB_SIFT = "in_file.sift"
OUTPUT_PCA_DB_SIFT = "in_file_d.spca"
OUTPUT_PCA_SCORE_SIFT = "in_file_d.spca.score"

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
    pca = PCA(n_components=d)
    pca.fit(allVectors)
    transformedPCA = pca.transform(allVectors);
    pca_database = np.column_stack((database[:, VIDEO_NUM_COL:(SIFT_DES_START-4)], transformedPCA))
    np.savetxt(INPUT_DB_PREFIX+OUTPUT_PCA_DB_SIFT, pca_database, delimiter=',', fmt="%d,%d,%d" + ",%.4f" * d)
    score = pca.components_
    score_mat = np.array([]).reshape(0, 3)
    for i in range(0, score.shape[0]):
        for j in range(0, score.shape[1]):
            score_mat = np.vstack([score_mat, [i + 1, j + 1, score[i, j]]])
    np.savetxt(INPUT_DB_PREFIX+OUTPUT_PCA_SCORE_SIFT, score_mat, delimiter=',', fmt="%d,%d,%f")

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
