# Read the graph from INPUT_FILE which is created by task 2 and output a Node rank to OUTPUT_FILE
# The output node format: vi_fi
# Usage: run the code directly, change the INPUT_FILE or OUTPUT_FILE as need.
import networkx as nx
import re
import operator
import numpy as np
import graphsim as gs

INPUT_FILE = '../Input/test.graph';


database = np.loadtxt(INPUT_FILE, delimiter = ',');
(row, column) = database.shape;
G = nx.Graph();
for i in range(row):
    G.add_edge(database[i, 0], database[i, 1], wight = database[i, 2]);
#page rank
prs = nx.pagerank(G);
sorted_prs = sorted(prs.items(), key=operator.itemgetter(1), reverse=True);
print sorted_prs;

#ascos
node_ids, sim = gs.ascos(G, c=0.85, is_weighted=True);
print sim;
(row, column) = sim.shape;
prs = {}
for i in range(row):
    inw = 0;
    for j in range(column):
        if j != i:
            inw += sim[i, j];
    w = inw / (column - 1);
    prs.update({(i+1):w});
sorted_prs = sorted(prs.items(), key=operator.itemgetter(1), reverse=True);
print sorted_prs;