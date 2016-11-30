import numpy as np
from scipy.spatial.distance import cdist
from sklearn import preprocessing as pp
import math
import time;
import os
import pickle
import operator
import utils

# SIFT desc Information
global START_COL, VIDEO_NUM_COL, FRAME_NUM_COL, CELL_NUM_COL, SIFT_DES_START, MAX_DIST
START_COL = 0
VIDEO_NUM_COL = 0
FRAME_NUM_COL = 1
CELL_NUM_COL = 2
SIFT_DES_START = 5
MAX_DIST = 0

global CLUSTERS, THRESHHOLD, SIMILARITY_DIC, MAX_CLUSTER_SIZE, DICTIONARY_SAVE_INTERVAL
CLUSTERS = {}
THRESHHOLD = 0.995
MAX_CLUSTER_SIZE = 30
# Similariry dictionary save interval in seconds
DICTIONARY_SAVE_INTERVAL = 600

SIMILARITY_DIC = {}

# SIFT I/O Information
INPUT_PREFIX = "../Input/"
INPUT_FILE = "in_file_d.spc"
OUTPUT_PREFIX = "../Output/"
OUTPUT_FILE = "in_file_d_k.gspc"

# Function : genDict
# Description: This function generates all the nodes for the graph
def genNodes(k):
    # Get total number of videos
    total_number_videos = database[-1, VIDEO_NUM_COL]

    # Iter over all the frames in the query video
    for query_video_number in range(1, int(total_number_videos + 1)):

        # Get the whole video
        query_video = database[database[:, VIDEO_NUM_COL] == query_video_number, VIDEO_NUM_COL:]

        # Get the number of frames for the video
        query_frameNos = np.transpose(np.unique(query_video[:, FRAME_NUM_COL]))

        for query_frame_number in np.nditer(query_frameNos):

            #TODO: ADD
            if isFrameClustered(query_video_number, query_frame_number):
                continue

            # Get the query frame using query_frame_number
            query_frame = query_video[query_video[:, FRAME_NUM_COL] == query_frame_number, SIFT_DES_START:]
            start = time.time();
            # List of the most similar frames
            query_frame_k_values = list()

            # Iter over all the frames in the object video
            for object_video_number in range(1, int(total_number_videos + 1)):

                # Don't find similarities in the same video
                # TODO: MODIFY
                #if query_video_number != object_video_number:

                    # Get the object video and the unique number of frames
                    object_video = database[database[:, VIDEO_NUM_COL] == object_video_number, VIDEO_NUM_COL:]
                    object_frameNos = np.transpose(np.unique(object_video[:, FRAME_NUM_COL]))

                    # Iter through all the frames in the object video
                    for object_frame_number in np.nditer(object_frameNos):

                        #TODO: ADD
                        if isFrameClustered(object_video_number, object_frame_number):
                            continue

                        dic_key = (query_video_number, int(query_frame_number.item(0)),object_video_number, int(object_frame_number.item(0)))
                        dic = SIMILARITY_DIC

                        sim_value = dic.get(dic_key, None)
                        if sim_value is None:
                            # Get the object frame
                            object_frame = object_video[object_video[:, FRAME_NUM_COL] == object_frame_number,
                                           SIFT_DES_START:]

                            # Compute the similarities values for the object frame and query video
                            sim_value = 1 - computeDistance(query_frame, object_frame)
                            #TODO: ADD
                            # add to dictionary
                            dic[dic_key] = sim_value;

                        # add to list
                        query_frame_k_values.append(
                            ((object_video_number, int(object_frame_number.item(0))), sim_value))


                        # Remove if there are too many items
                        #TODO: MODIFY
                        # if len(query_frame_k_values) > k:
                        #     query_frame_k_values = sorted(query_frame_k_values, key=lambda t: t[1], reverse=True)
                        #     del query_frame_k_values[-1]

            # sort before printing
            query_frame_k_values = sorted(query_frame_k_values, key=lambda t: t[1], reverse=True)
            #TODO: ADD
            addToClusters(query_video_number, int(query_frame_number.item(0)), query_frame_k_values)

            # print to the file
            #TODO: MODIFY
            #printInfo(query_video_number, int(query_frame_number.item(0)), query_frame_k_values)
            now = time.time()
            cost = now - start;
            print "One frame cost: " + str(cost) + " seconds."
    #TODO: ADD
    outputClusters()
    outputSimilarityDic()


def knn(k):
    # Get total number of videos
    total_number_videos = database[-1, VIDEO_NUM_COL]
    TIME_COUNTER = time.time()
    # Iter over all the frames in the query video
    for query_video_number in range(1, int(total_number_videos + 1)):

        # Get the whole video
        query_video = database[database[:, VIDEO_NUM_COL] == query_video_number, VIDEO_NUM_COL:]

        # Get the number of frames for the video
        query_frameNos = np.transpose(np.unique(query_video[:, FRAME_NUM_COL]))

        for query_frame_number in np.nditer(query_frameNos):

            query_frame_number = int(query_frame_number.item(0))
            # Get the query frame using query_frame_number
            # query_frame = query_video[query_video[:, FRAME_NUM_COL] == query_frame_number, SIFT_DES_START:]
            start = time.time();
            # List of the most similar frames
            query_frame_k_values = list()

            cluster_score_dic = {}
            frame_clusters_dic = CLUSTERS
            for key in frame_clusters_dic:
                object_video_number, object_frame_number = key
                similarity = getSimilarityValue(query_video_number, query_frame_number, object_video_number,
                           object_frame_number)
                cluster_score_dic[key] = similarity
            # sort seed-score dictionary
            sorted_seed_score_dic = sorted(cluster_score_dic.items(), key=operator.itemgetter(1), reverse=True)
            for key, similarity in sorted_seed_score_dic:
                print "cluster: %s,  sim: %s" % (str(key), str(similarity))
                frames_set = frame_clusters_dic.get(key, None)
                for (object_video_number, object_frame_number) in frames_set:
                    # Do not compare frames in a same video
                    if query_video_number != object_video_number:
                        sim_value = getSimilarityValue(query_video_number, query_frame_number, object_video_number, object_frame_number)
                        # add to list
                        query_frame_k_values.append(
                            ((object_video_number, object_frame_number), sim_value))
                if len(query_frame_k_values) > k:
                    break
            # sort before printing
            query_frame_k_values = sorted(query_frame_k_values, key=lambda t: t[1], reverse=True)
            # print to the file
            # TODO: MODIFY
            printInfo(query_video_number, query_frame_number, query_frame_k_values, k)
            now = time.time()
            cost = now - start;
            print "KNN One frame cost: " + str(cost) + " seconds."
            if now - TIME_COUNTER > DICTIONARY_SAVE_INTERVAL:
                print "Begin saving similarity dictionary."
                #global TIME_COUNTER
                TIME_COUNTER = now
                outputSimilarityDic()

def getSimilarityValue(query_video_number, query_frame_number, object_video_number, object_frame_number):
    dic_key = (query_video_number, query_frame_number, object_video_number, object_frame_number)
    dic = SIMILARITY_DIC
    sim_value = dic.get(dic_key, None)
    if sim_value is None:
        query_video = database[database[:, VIDEO_NUM_COL] == query_video_number, VIDEO_NUM_COL:]
        query_frame = query_video[query_video[:, FRAME_NUM_COL] == query_frame_number, SIFT_DES_START:]
        # Get the object video and the unique number of frames
        object_video = database[database[:, VIDEO_NUM_COL] == object_video_number, VIDEO_NUM_COL:]
        # Get the object frame
        object_frame = object_video[object_video[:, FRAME_NUM_COL] == object_frame_number,
                       SIFT_DES_START:]
        sim_value = 1 - computeDistance(query_frame, object_frame)
        # add to similarity dictionary
        dic[dic_key] = sim_value
    # else:
    #     print "getSimilarityValue() find a sim in dic."
    return sim_value

#TODO: ADD
def outputClusters():
    PATH = "../Output/Clusters/"
    if not os.path.isdir(PATH):
        os.mkdir(PATH)
    # count = 0;
    for key in CLUSTERS:
     #   file_writer = open(PATH + str(count)+".cluster", "wb")
        vi, fi = key;
        cluster = CLUSTERS[key]
        with open(PATH + str(vi) + "_" + str(fi) +".cluster", "wb") as handle:
            pickle.dump(cluster, handle)

#TODO: ADD
def outputSimilarityDic():
    PATH = "../Output/SimilarityDics/"
    if not os.path.isdir(PATH):
        os.mkdir(PATH)
    now = time.time();
    with open(PATH + str(now) + ".dic", "wb") as handle:
        pickle.dump(SIMILARITY_DIC, handle)

def loadSimilarityDic():
    PATH = "../Output/SimilarityDics/"
    if not os.path.isdir(PATH):
        return
    filelist = [f for f in os.listdir(PATH)]
    if len(filelist) > 0:
        file = filelist[-1]
        with open(PATH + file, "rb") as handle:
            dic = pickle.loads(handle.read())
            if dic is not None:
                SIMILARITY_DIC.update(dic)

#TODO: ADD
def addToClusters(query_video_number, query_frame_number, query_frame_k_values, threshhold=THRESHHOLD):
    print "Left frames count: " + str(query_frame_k_values.__len__())
    cluster = set()
    query_obj = (query_video_number, query_frame_number)
    # cluster.add((query_video_number, query_frame_number))
    for object_video_info, similarity in query_frame_k_values:
        if similarity > threshhold:
            cluster.add(object_video_info)
        else:
            break
    if cluster.__len__() > 0:
        if (cluster.__len__() > MAX_CLUSTER_SIZE):
            breakAndAddCluster(cluster)
        else:
          CLUSTERS[query_obj] = cluster
    print "Clusters count: " + str(CLUSTERS.__len__())

def breakAndAddCluster(cluster):
    print "breakAndAddCluster(): start, cluster length: %s" % (str(len(cluster)))
    # get an element from the set
    for query_obj in cluster:
        break
    query_video_number, query_frame_number = query_obj
    query_frame_k_values = list()
    for obj in cluster:
        object_video_number, object_frame_number = obj
        sim_value = getSimilarityValue(query_video_number, query_frame_number, object_video_number, object_frame_number)
        # add to list
        query_frame_k_values.append(
            ((object_video_number, object_frame_number), sim_value))
    # sort before add
    query_frame_k_values = sorted(query_frame_k_values, key=lambda t: t[1], reverse=True)
    addSubClusters(query_video_number, query_frame_number, query_frame_k_values)

def addSubClusters(query_video_number, query_frame_number, query_frame_k_values):
    print "addSubClusters(): break a cluster"
    cluster1 = set()
    query_obj = (query_video_number, query_frame_number)
    # cluster.add((query_video_number, query_frame_number))
    count = 0;
    for object_video_info, similarity in query_frame_k_values:
        if count < MAX_CLUSTER_SIZE:
            cluster1.add(object_video_info)
            count += 1

    # copy the left objects
    object_list = list()
    for i in range(count, len(query_frame_k_values)):
        object_list.append(query_frame_k_values[i])
    query_frame_k_values = object_list

    if cluster1.__len__() > 0:
        CLUSTERS[query_obj] = cluster1
        print "Cluster 1 length: %s" % str(cluster1.__len__())
    cluster2 = set()
    for object_video_info, similarity in query_frame_k_values:
        cluster2.add(object_video_info)
    if len(cluster2) <= MAX_CLUSTER_SIZE:
        # Get an element
        query_obj, similarity  = query_frame_k_values[0]
        CLUSTERS[query_obj] = cluster2
        print "Cluster 2 length: %s" % str(cluster2.__len__())
    else:
        breakAndAddCluster(cluster2)
        print "Cluster 2 size %s too big, break again." % (str(len(cluster2)))
    print "addTwoPartsToCluster(): Clusters count: " + str(CLUSTERS.__len__())

# TODO: ADD
def isFrameClustered(video_index, frame_index):
    c = CLUSTERS
    for key in CLUSTERS:
        cluster = CLUSTERS[key]
        if (video_index, int(frame_index.item(0))) in cluster:
            return True
    return False

# Function : printInfo
# Description: Prints each node in the graph, print k nodes at most
def printInfo(query_video_number, query_frame_number, query_frame_k_values, k):

    # Open the file to Edit
    printerFile = open(OUTPUT_FILE, "ab")

    count = 0
    # pint to the file
    for object_video_info, similarity in query_frame_k_values:
        object_video_number, object_frame_number = object_video_info

        printerFile.write(str(query_video_number) + "," + str(query_frame_number) + "," + str(
            object_video_number) + "," + str(object_frame_number) + "," + str(similarity) + "\n")
        count += 1
        if count >= k:
            break
    # Close the file
    printerFile.close()

# Function : preProcessing
# Description: This function computes the distance between two frames
def computeDistance(qframe, oframe):
#    start = time.time();
    frameD = cdist(qframe, oframe, 'euclidean')
    minD = np.amin(frameD, axis=1)
    meanD = np.mean(minD)
    meanD = meanD / MAX_DIST
#    cost = time.time() - start;
#    print "Distance consume: " + str(cost) + " seconds."
    return meanD

# Function : preProcessing
# Description: This function loads the database and clears the input file
def preProcessing(fileName, k):

    global database, MAX_DIST, OUTPUT_FILE
    # Clear the file
    OUTPUT_FILE = OUTPUT_PREFIX + fileName + "_" + str(k) + ".gspc"
    printerFile = open(OUTPUT_FILE, "wb")
    printerFile.close()

    # Load the database
    print 'Loading database......'

    database = np.loadtxt(INPUT_FILE, delimiter=",")
    scaler = pp.MinMaxScaler().fit(database[:, SIFT_DES_START:])
    database = np.column_stack((database[:, 0:SIFT_DES_START], scaler.transform(database[:, SIFT_DES_START:])))
    MAX_DIST = math.sqrt(database.shape[1] - SIFT_DES_START)
    print 'Database loaded......'

    print 'Loading similarity dictionary......'
    loadSimilarityDic()
    print 'Similarity dictionary loaded......'

# Function : Main
# Description: Run the main program
if __name__ == '__main__':
    # TODO:M
    INPUT_FILE = raw_input("Enter the input file name(File should exist in Input directory): ")
    # INPUT_FILE = "sift_vector_10.spc"
    fileName = INPUT_FILE.split(".")[0]
    INPUT_FILE = INPUT_PREFIX + INPUT_FILE
    # Take k as an input
    flag = 1
    while flag :
        #TODO:M
        k = int(input("Enter k, for the k most similar frames: "))
        # k = 10
        if k <=0 :
            print 'K must be positive.'
        else : flag = 0

    start_time = time.time();
    # Pre-processing
    preProcessing(fileName, k)

    # generate the Nodes for the graph
    genNodes(k)
    # perform k nearest neighbor search on the clusters
    knn(k)
    #
    outputSimilarityDic()
    utils.printTime(time.time() - start_time)
    print "Done."

