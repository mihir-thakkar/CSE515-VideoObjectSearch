import numpy as np
import string
import networkx as nx
import operator

# graph file
global INPUT_FILE
INPUT_FILE = "../Output/output_t2_d_5.gspc"

VIDEO_NUM_COL = 0
FRAME_NUM_COL = 1

QUERY_VIDEO_NUM_COL = 0
QUERY_FRAME_NUM_COL = 1
OBJECT_VIDEO_NUM_COL = 2
OBJECT_FRAME_NUM_COL = 3
SIMILARITY_COL = 4

def creatGraph(m):
    #creat a new graph
    G = nx.DiGraph()

    total_number_videos = database[-1, VIDEO_NUM_COL]
    for query_video_number in range(1, int(total_number_videos + 1)):
        query_video = database[database[:, VIDEO_NUM_COL] == query_video_number, VIDEO_NUM_COL:]

        # Get the number of frames for the video
        query_frameNos = np.transpose(np.unique(query_video[:, FRAME_NUM_COL]))

        for query_frame_number in np.nditer(query_frameNos):
            #print query_video_number, ",", query_frame_number, "\n"
            G.add_node((int(query_video_number),int(query_frame_number)))

    #get the database size
    (row, column) = database.shape

    for r in range(row):
        totalweight = 0

        for c in range(column):
            if (c % 5) == 4:
                #calculate the total similarity between the query frames and its k similar object frames
                totalweight += database[r, c]

        #add edge weight(similarity) btw query node and object nodes
        for c in range(column):
            if (c % 5) == 4:
                q_video_number = database[r, c - 4]
                q_frame_number = database[r, c - 3]
                o_video_number = database[r, c - 2]
                o_frame_number = database[r, c - 1]

                #weight = similarity/total_similarity -> normalize
                weight = database[r, c]/totalweight

                # add edge weight
                G.add_edge((int(q_video_number),int(q_frame_number)), (int(o_video_number),int(o_frame_number)), weight=weight)

    #calculate page_rank
    pr = nx.pagerank(G, alpha=0.9)
    # SORT edge weight
    sorted_pr = sorted(pr.items(), key=operator.itemgetter(1), reverse=True)
    printInfo(sorted_pr, m)

def printInfo(page_rank, m):
    printerFile = open("../Output/" + "output_t4_" + str(m) + ".pgr", "ab")

    for M in range(m):
        printerFile.write(str(page_rank[M]))
        printerFile.write("\n")

    printerFile.close()

def preProcessing(m):

    # Clear the file
    transfile = open("../Input/" + "trans_output_t2.gspc", "wb")
    printerFile = open("../Output/" + "output_t4_" + str(m) + ".pgr", "wb")
    printerFile.close()

    # Load the database
    print 'Loading database......'

    with open(INPUT_FILE) as f:
        for line in f:
            translation_table = string.maketrans("{()},", "     ")
            splitline = line.translate(translation_table).split()
            transfile.write(splitline[0])
            for l in range(1, len(splitline)):
                transfile.write(","+splitline[l])
            transfile.write("\n")

    transfile.write("\n")
    transfile.close()

    global database
    database = np.loadtxt("../Input/" + "trans_output_t2.gspc", delimiter=",")

    print 'Database loaded......'

# Function : Main
# Description: Run the main program
if __name__ == '__main__':

    # Take k as an input
    m = int(input("Enter m, for the m most significant frames:"))

    preProcessing(m)
    creatGraph(m)
