# Read the graph from INPUT_FILE which is created by task 2 and output a Node rank to OUTPUT_FILE
# The output node format: vi_fi
# Usage: run the code directly, change the INPUT_FILE or OUTPUT_FILE as need.
import networkx as nx
import re
import operator
import csv

INPUT_FILE = '../Output/output_t2_d_5.gspc';
OUTPUT_FILE = '../Output/pageranks.csv';

def add_edges_from_line(D, p_str):
    str = re.sub('\{|\}|\(|\)|\n|,', ' ', p_str);
    str = str.strip();
    str = re.sub(' +', ' ', str);
    arr = str.split(' ');
    k = len(arr) / 5;
    for i in range(k):
        si = i * 5;
        node1 = arr[si] + '_' +arr[si + 1];
        node2 = arr[si + 2] + '_' + arr[si + 3];
        D.add_weighted_edges_from([(node1, node2, float(arr[si + 4]))]);


D = nx.DiGraph();
with open(INPUT_FILE, 'r') as ins:
    for line in ins:
        add_edges_from_line(D, line);
prs = nx.pagerank(D);
sorted_prs = sorted(prs.items(), key=operator.itemgetter(1), reverse=True);
# print sorted_prs;
w = csv.writer(open(OUTPUT_FILE, 'w'));
for key, val in sorted_prs:
    w.writerow([key, val]);