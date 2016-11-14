import numpy as np
import string
import networkx as nx
import operator

# graph file
global INPUT_FILE
INPUT_FILE = "../Output/output_t2_d_5.gspc"

def creatGraph(m):
    #creat a new graph
    G = nx.DiGraph()

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
                # add node
                G.add_node((int(q_video_number), int(q_frame_number)))
                # add edge weight
                G.add_edge((int(q_video_number),int(q_frame_number)), (int(o_video_number),int(o_frame_number)), weight=weight)

    #calculate page_rank
    pr = nx.pagerank(G)
    # SORT edge weight
    sorted_pr = sorted(pr.items(), key=operator.itemgetter(1), reverse=True)
    printInfo(sorted_pr, m)

def printInfo(page_rank, m):
    printerFile = open("../Output/" + "output_t3_" + str(m) + ".pgr", "ab")

    for M in range(m):
        printerFile.write(str(page_rank[M]))
        printerFile.write("\n")

    printerFile.close()

def preProcessing(m):

    # Clear the file
    transfile = open("../Input/" + "trans_output_t2.gspc", "wb")
    printerFile = open("../Output/" + "output_t3_" + str(m) + ".pgr", "wb")
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
