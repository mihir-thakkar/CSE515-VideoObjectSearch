import numpy as np
import string
import networkx as nx
import operator

# graph file
global INPUT_FILE
INPUT_FILE = "../Output/output_t2_d_5.gspc"
global first_intput_video, first_intput_frame, \
    second_intput_video, second_intput_frame, \
    third_intput_video, third_intput_frame

def creatGraph(m):
    #creat a new graph
    G = nx.DiGraph()
    #get the database size
    (row, column) = database.shape

    personalize = {}
    for r in range(row):
        #add edge weight(similarity) btw query node and object nodes
        for c in range(column):
            if (c % 5) == 4:
                q_video_number = database[r, c - 4]
                q_frame_number = database[r, c - 3]
                o_video_number = database[r, c - 2]
                o_frame_number = database[r, c - 1]
                weight = database[r, c]
                # add nodes
                #G.add_node((int(q_video_number), int(q_frame_number)))
                # add edge weight
                G.add_edge((int(q_video_number),int(q_frame_number)), (int(o_video_number),int(o_frame_number)), weight=weight)

                if int(q_video_number) == first_intput_video and int(q_frame_number) == first_intput_frame:
                    personalize[(int(q_video_number), int(q_frame_number))] = 0.333
                elif int(q_video_number) == second_intput_video and int(q_frame_number) == second_intput_frame:
                    personalize[(int(q_video_number), int(q_frame_number))] = 0.333
                elif int(q_video_number) == third_intput_video and int(q_frame_number) == third_intput_frame:
                    personalize[(int(q_video_number), int(q_frame_number))] = 0.333
                else:
                    personalize[(int(q_video_number),int(q_frame_number))] = 0



    pr = nx.pagerank(G, alpha=0.9, personalization=personalize)
    sorted_pr = sorted(pr.items(), key=operator.itemgetter(1), reverse=True)
    printInfo(sorted_pr, m)
    print G.out_degree((1,1),weight='weight')

def printInfo(page_rank, m):
    printerFile = open("../Output/" + "output_t4_" + str(m) + ".pgr", "ab")

    M = 0
    count = 0
    while (count != m):
        node, sim = page_rank[M]
        if node != (first_intput_video, first_intput_frame) and \
                        node != (second_intput_video, second_intput_frame) and \
                        node != (third_intput_video, third_intput_frame):
            print node
            printerFile.write(str(page_rank[M]))
            printerFile.write("\n")
            count += 1;
        M += 1

    printerFile.close()

def preProcessing(m):

    # Clear the file
    transfile = open("../Input" + "trans_output_t2.gspc", "wb")
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
    m = int(input("Enter m, for the m most significant frames (relative to the input frames):"))
    first_intput_video, first_intput_frame = input("Enter first input frame:")
    second_intput_video, second_intput_frame = input("Enter second input frame:")
    third_intput_video, third_intput_frame = input("Enter third input frame:")
    preProcessing(m)
    creatGraph(m)
