import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
import imageio

# SIFT desc Information
global START_COL, VIDEO_NUM_COL, FRAME_NUM_COL, CELL_NUM_COL, SIFT_DES_START
START_COL = 0
VIDEO_NUM_COL = 3
FRAME_NUM_COL = 4
CELL_NUM_COL = 5
LSH_HASH_COL = 1
LSH_BUCKET_COL = 0
DATA_INDEX_COL = 2
X_COL = 6
Y_COL = 7


# SIFT I/O Information
global INPUT_FILE
INPUT_FILE = "../Output/filename_d.lsh"

# Function : preProcessing
# Description: This function loads the database and clears the input file
def preProcessing():

    # Clear the file
    # printerFile = open("../Output/" + "output_t2_d_" + str(K) + ".gspc", "wb")
    # printerFile.close()

    # Load the database
    print 'Loading database......'

    global database, databasePD
    database = np.loadtxt("../Input/in_file.sift", delimiter=",")
    databasePD = pd.read_csv(INPUT_FILE,header=None,names=['b','h','i','v','f','c','x','y'])

    print 'Database loaded......'

def search(N,V,F,X1,Y1,X2,Y2):
    samples = databasePD[(databasePD.v == V) & (databasePD.f == F) & (databasePD.x>=X1) & (databasePD.x<=X2) & (databasePD.y>=Y1) & (databasePD.y<=Y2)]
    selIndexes = samples['i']
    selIndexes = selIndexes.drop_duplicates()
    sampleArray = database[selIndexes,:]
    samples = samples[['b', 'h']]
    result = pd.merge(samples, databasePD, how='inner', on=['b', 'h'])
    result = result[(result.v != V)]
    overallSiftVectors = result.shape[0]
    result = result.drop_duplicates('i')
    result = result.sort_values('i')
    uniqueSiftVectors = result.shape[0]
    prunedData = database[result['i'],:]

    videoNos = np.transpose(np.unique(prunedData[:, 0]))
    frameSim = np.array([]).reshape(0, 3)
    for videoNo in np.nditer(videoNos):
        videoData = prunedData[prunedData[:, 0] == videoNo, :]
        frameNos = np.transpose(np.unique(videoData[:, 1]))
        for frameNo in np.nditer(frameNos):
            frameD = cdist(videoData[videoData[:, 1] == frameNo, 5:], sampleArray[:, 5:], 'euclidean')
            # Most similar vectors
            minD = np.amin(frameD, axis=1)
            meanD = np.mean(minD)
            frameSim = np.vstack([frameSim, [videoNo, frameNo, meanD]])
    frameSim = frameSim[np.argsort(frameSim[:, 2])]

    for i in range(0,N):
        print 'Video No: %s Frame No: %s' % (str(frameSim[i:0]), str(frameSim[i:1]))
    print 'done'

# Function : Main
# Description: Run the main program
if __name__ == '__main__':


    # Pre-processing
    preProcessing()
    while 1:
        # Take k as an input
        N = int(input("Enter n, for number of frames: "))
        (V,F,X1,Y1,X2,Y2) = map(int, raw_input("Enter Video, Frame No and 2 points seperated by space (V F X1 Y1 X2 Y2): ").split())
        search(N, V, F, X1, Y1, X2, Y2)

