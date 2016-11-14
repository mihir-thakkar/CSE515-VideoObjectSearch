# Read the graph from INPUT_FILE which is created by task 2 and output a Node rank to OUTPUT_FILE
# The output node format: vi_fi
# Usage: run the code directly, change the INPUT_FILE or OUTPUT_FILE as need.
import networkx as nx
import copy
import numpy
import math
import re
import operator
import csv

INPUT_FILE = '../Output/output_t2_d_5.gspc';
OUTPUT_FILE = '../Output/output_ranks_ascos.csv';


def ascos(G, c=0.9, max_iter=100, remove_neighbors=False, remove_self=False, dump_process=False):

    if type(G) == nx.MultiGraph or type(G) == nx.MultiDiGraph:
        raise Exception("ascos() not defined for graphs with multiedges.")

    node_ids = G.nodes()
    node_id_lookup_tbl = {}
    for i, n in enumerate(node_ids):
        node_id_lookup_tbl[n] = i
    # Use predecessors
    nb_ids = [G.predecessors(n) for n in node_ids]
    nbs = []
    for nb_id in nb_ids:
        nbs.append([node_id_lookup_tbl[n] for n in nb_id])
    del (node_id_lookup_tbl)

    n = G.number_of_nodes()
    sim = numpy.eye(n)
    sim_old = numpy.zeros(shape=(n, n))

    for iter_ctr in range(max_iter):
        if _is_converge(sim, sim_old, n, n):
            break
        sim_old = copy.deepcopy(sim)
        for i in range(n):
            if dump_process:
                print iter_ctr, ':', i, '/', n
            # Use in degree
            w_i = G.in_degree(weight='weight')[node_ids[i]]
            for j in range(n):
                if i == j:
                    continue
                s_ij = 0.0
                for n_i in nbs[i]:
                    w_ki = G[node_ids[n_i]][node_ids[i]]['weight'] if 'weight' in G[node_ids[n_i]][node_ids[i]] else 1
                    s_ij += float(w_ki) * (1 - math.exp(-w_ki)) * sim_old[n_i, j]

                sim[i, j] = c * s_ij / w_i if w_i > 0 else 0

    if remove_self:
        for i in range(n):
            sim[i, i] = 0

    if remove_neighbors:
        for i in range(n):
            for j in nbs[i]:
                sim[i, j] = 0

    return node_ids, sim


def _is_converge(sim, sim_old, nrow, ncol, eps=1e-4):
    for i in range(nrow):
        for j in range(ncol):
            if abs(sim[i, j] - sim_old[i, j]) >= eps:
                return False
    return True


def add_edges_from_line(D, p_str):
    str = re.sub('\{|\}|\(|\)|\n|,', ' ', p_str);
    str = str.strip();
    str = re.sub(' +', ' ', str);
    arr = str.split(' ');
    k = len(arr) / 5;
    for i in range(k):
        si = i * 5;
        node1 = arr[si] + '_' + arr[si + 1];
        node2 = arr[si + 2] + '_' + arr[si + 3];
        D.add_weighted_edges_from([(node1, node2, float(arr[si + 4]))]);


D = nx.DiGraph();
with open(INPUT_FILE, 'r') as ins:
    for line in ins:
        add_edges_from_line(D, line);
node_ids, sim = ascos(D);
# print node_ids;
# node ranks
prs = {}
length = len(node_ids);
for j in range(length):
    simsum = 0;
    for i in range(length):
        if i != j:
            simsum += sim[i, j];
    w = simsum / (length - 1);
    prs.update({node_ids[j]: w});
sorted_prs = sorted(prs.items(), key=operator.itemgetter(1), reverse=True);
w = csv.writer(open(OUTPUT_FILE, 'w'));
for key, val in sorted_prs:
    w.writerow([key, val]);