import numpy as np
from scipy.spatial.distance import cdist
from sklearn.neighbors import LSHForest
from nearpy import Engine
from nearpy.hashes import RandomBinaryProjections

# SIFT desc Information
global START_COL, VIDEO_NUM_COL, FRAME_NUM_COL, CELL_NUM_COL, SIFT_DES_START
START_COL = 0
VIDEO_NUM_COL = 0
FRAME_NUM_COL = 1
LSH_VECT_START_COL = 5
CELL_NUM_COL = 2
SIFT_DES_START = 7


# SIFT I/O Information
global INPUT_FILE
INPUT_FILE = "../Input/in_file.sift_phase1.txt"

# Function : LSH
# Description: This function hashes the SIFT vectors
# Arguments: layers = number of hash forests/layers, K = 2^K buckets in each layer
def LSH(Layers, K):

    lsh_vectors = database[:, LSH_VECT_START_COL:]
    video_frame_cell_nums = database[:, 0:2]

    # Dimension of our vector space
    num_rows, num_cols = lsh_vectors.shape
    dimension = num_cols

    # Random binary projection list
    rbp = list()
    for i in range(Layers):
        rbp.append(RandomBinaryProjections(str(i), K))

    # Create engine with pipeline configuration
    engine = Engine(dimension, lshashes=rbp)

    # Index 1000000 random vectors (set their data zo a unique string)
    for index in range(num_rows):
        v = np.random.randn(dimension)
        #engine.store_vector(v, 'data_%d' % index)
        ",".join(str(bit) for bit in video_frame_cell_nums)
        engine.store_vector(v, )

    print 'stop'

# Function : preProcessing
# Description: This function loads the database and clears the input file
def preProcessing():

    # Clear the file
    # printerFile = open("../Output/" + "output_t2_d_" + str(K) + ".gspc", "wb")
    # printerFile.close()

    # Load the database
    print 'Loading database......'

    global database
    database = np.loadtxt(INPUT_FILE, delimiter=",")

    print 'Database loaded......'


# Function : Main
# Description: Run the main program
if __name__ == '__main__':

    # Take k as an input
    L = int(input("Enter L, for L layers of LSH: "))
    K = int(input("Enter K, for 2^K buckets in each hash layer: "))

    # Pre-processing
    preProcessing()

    # Hash the vectors
    LSH(L,K)