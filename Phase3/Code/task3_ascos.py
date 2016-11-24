import numpy as np
import string
import networkx as nx
import operator
import copy
import math

# graph file
global INPUT_FILE
INPUT_FILE = "../Output/output_t2_d_cell5.gspc"

def creatGraph(m):
    #creat a new graph
    G = nx.DiGraph()
    #get the database size
    (row, column) = database.shape

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

    ASCOS = ascos(G, is_weighted=True)
    sorted_ASCOS = sorted(ASCOS.items(), key=operator.itemgetter(1), reverse=True)
    print sorted_ASCOS
    printInfo(sorted_ASCOS, m)

def ascos(G, c=0.9, max_iter=100, is_weighted=False, remove_neighbors=False, remove_self=False, dump_process=False):

    if type(G) == nx.MultiGraph or type(G) == nx.MultiDiGraph:
        raise Exception("ascos() not defined for graphs with multiedges.")

    node_ids = G.nodes()

    node_id_lookup_tbl = { }
    for i, n in enumerate(node_ids):
        node_id_lookup_tbl[n] = i

    nb_ids = [G.successors(n) for n in node_ids]

    nbs = [ ]
    for nb_id in nb_ids:
        nbs.append([node_id_lookup_tbl[n] for n in nb_id])
    del(node_id_lookup_tbl)

    n = G.number_of_nodes()
    sim = np.eye(n)
    # for i in range(n):
    #     for n_i in nbs[i]:
    #         sim[i, n_i] = G[node_ids[i]][node_ids[n_i]]['weight']

    sim_old = np.zeros(shape = (n, n))
    for iter_ctr in range(max_iter):
        print iter_ctr
        if _is_converge(sim, sim_old, n, n):
            break
        sim_old = copy.deepcopy(sim)
        for i in range(n):
            if dump_process:
                print iter_ctr, ':', i, '/', n
            w_i = G.out_degree(weight='weight')[node_ids[i]]
            for j in range(n):
                if not is_weighted:
                    if i == j:
                        continue
                    s_ij = 0.0
                    for n_i in nbs[i]:
                        s_ij += sim_old[n_i, j]
                    sim[i, j] = c * s_ij / len(nbs[i]) if len(nbs[i]) > 0 else 0
                else:
                    if i == j:
                        continue
                    s_ij = 0.0
                    for n_i in nbs[i]:
                        w_ik = G[node_ids[i]][node_ids[n_i]]['weight'] if 'weight' in G[node_ids[i]][node_ids[n_i]] else 1
                        s_ij += float(w_ik) * (1 - math.exp(-w_ik)) * sim_old[n_i, j]

                    sim[i, j] = c * s_ij / w_i if w_i > 0 else 0

    if remove_self:
        for i in range(n):
            sim[i,i] = 0

    if remove_neighbors:
        for i in range(n):
            for j in nbs[i]:
                sim[i,j] = 0

    ASCOS = {}
    for nodej in range(len(node_ids)):
        totalsum = 0;
        for nodei in range(len(node_ids)):
            if nodei != nodej:
                totalsum += sim[nodei, nodej]
        totalsum = totalsum / (len(node_ids) - 1)
        ASCOS[node_ids[nodej]] = totalsum

    return ASCOS

def _is_converge(sim, sim_old, nrow, ncol, eps=1e-4):
    for i in range(nrow):
        for j in range(ncol):
            if abs(sim[i,j] - sim_old[i,j]) >= eps:
                return False
    return True

def printInfo(sorted_ASCOS, m):
    printerFile = open("../Output/" + "output_t3_" + str(m) + ".ascos", "ab")

    for M in range(m):
        printerFile.write(str(sorted_ASCOS[M]))
        printerFile.write("\n")

    printerFile.close()

def calculate_k():
    column1 = ''
    column2 = ''
    count = 0;
    with open(INPUT_FILE) as f:
        for line in f:
            a = line.split(',');
            if column1 == '' and column2 == '':
                column1 = a[0]
                column2 = a[1]
            elif column1 != a[0] or column2 != a[1]:
                break
            count += 1
    return count;

def preProcessing(m):

    # Clear the file
    transfile = open("../Input" + "trans_output_t2.gspc", "wb")
    printerFile = open("../Output/" + "output_t3_" + str(m) + ".ascos", "wb")
    printerFile.close()
    # Load the database
    print 'Loading database......'

    k = calculate_k()

    count = 0
    with open(INPUT_FILE) as f:
        for line in f:
            line = line.strip('\n')
            transfile.write(line)
            count += 1
            if count == k:
                transfile.write("\n")
                count = 0
            else:
                transfile.write(",")

    transfile.write("\n")
    transfile.close()

    global database
    database = np.loadtxt("../Input" + "trans_output_t2.gspc", delimiter=",")
    print 'Database loaded......'

# Function : Main
# Description: Run the main program
if __name__ == '__main__':
    # Take k as an input
    m = int(input("Enter m, for the m most significant frames (relative to the input frames):"))

    preProcessing(m)
    creatGraph(m)
