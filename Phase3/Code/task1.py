import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

# I/O format
global INPUT_FILE, OUTPUT_FILE, SCORE_FILE
INPUT_FILE = "../Input/in_file.sift"
OUTPUT_FILE = "../Output/filename_d.spc"
SCORE_FILE = "../Output/scores.spc"

# SIFT format
global START_COL, VIDEO_NUM_COL, FRAME_NUM_COL, CELL_NUM_COL, SIFT_DES_START
START_COL = 0
VIDEO_NUM_COL = 0
FRAME_NUM_COL = 1
CELL_NUM_COL = 2
SIFT_DES_START = 7

def preprocessing():
    # Load the data
    global database
    database = np.loadtxt(INPUT_FILE, delimiter=",")

def reduce(d):

    # ALL vectors
    allVectors = database[:, SIFT_DES_START:]
    pca = PCA(n_components=d)
    pca.fit(allVectors)

    # Print the actual database
    transformedPCA = pca.transform(allVectors)
    pca_database = np.column_stack((database[:, VIDEO_NUM_COL:SIFT_DES_START], transformedPCA))
    np.savetxt(OUTPUT_FILE, pca_database, delimiter=',', fmt="%d,%d,%d" + ",%.4f" * (d+4))

    # Print the scores
    whole_list = list()
    score = pca.components_
    for i in range(0, score.shape[0]):
        score_mat = list()
        for j in range(0, score.shape[1]):
            score_mat.append((i+1, j+1, score[i, j]))

        score_mat = sorted(score_mat, key=lambda t: t[2], reverse=True)
        whole_list.append(score_mat)

    print_list = [node for score_list in whole_list for node in score_list]
    np.savetxt(SCORE_FILE, print_list, delimiter=',', fmt="%d,%d,%f")


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
