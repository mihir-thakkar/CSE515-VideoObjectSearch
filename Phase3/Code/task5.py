import numpy as np
from nearpy import Engine
from nearpy.hashes import RandomBinaryProjections
from nearpy.distances import CosineDistance

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
INPUT_FILE = "../Input/in_file.sift"

# Function : LSH
# Description: This function hashes the SIFT vectors
# Arguments: layers = number of hash forests/layers, K = 2^K buckets in each layer
def LSH(Layers, K):

    lsh_vectors = database[:, LSH_VECT_START_COL:]
    video_data = database[:, 0:5]

    num_rows, num_cols = lsh_vectors.shape
    dimension = num_cols

    rbp = list()
    for i in range(Layers):
        rbp.append(RandomBinaryProjections(str(i), K))

    # Create engine with pipeline configuration
    engine = Engine(dimension, lshashes=rbp)

    # Index 1000000 random vectors (set their data zo a unique string)
    for index in range(num_rows):
        v = lsh_vectors[index, :]

        meta_data = str(index)+',' + str(int(video_data[index, 0])) + ', ' + str(int(video_data[index, 1])) + ', ' + str(int(video_data[index, 2])) \
                    + ', ' + str(video_data[index, 3]) + ', ' + str(video_data[index, 4])

        engine.store_vector(v, meta_data)

    printOutput(engine.storage.buckets)

    print 'stop'

def printOutput(buckets):
    # Open the file to Edit
    printerFile = open("../Output/" + "filename_d.lsh", "wb")

    for layers in buckets.keys():
        current_layer= buckets[layers]
        for new_buckets in current_layer.keys():
            current_bucket = current_layer[new_buckets]
            for current_point in current_bucket:
                printerFile.write( layers + ', ' + new_buckets + ', ' + current_point[1])
                printerFile.write("\n")

    printerFile.close()

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
    K = 2 ** K
    # Pre-processing
    preProcessing()

    # Hash the vectors
    LSH(L,K)