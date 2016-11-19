import networkx as nx
import re
import operator
import csv

INPUT_FILE = '../Output/output_t2_d_5.gspc';
OUTPUT_FILE = '../Output/pageranks_personalized.csv';

node_dict = {}
array = raw_input("please input three query frames: ");     #input format:1_44 1_46 1_47
m = int(input("please input the most significant m frames (relative to the input frames): "))
input_frames = array.split(' ');
print(input_frames);

def add_edges_from_line(D, p_str):
    str = re.sub('\{|\}|\(|\)|\n|,', ' ', p_str);
    str = str.strip();
    str = re.sub(' +', ' ', str);
    arr = str.split(' ');
#    print arr;
    k = len(arr) / 5;
    for i in range(k):
        si = i * 5;
        node1 = arr[si] + '_' +arr[si + 1];
        if node1 == input_frames[0] or node1 == input_frames[1] or node1 == input_frames[2]:
            node_dict[node1] = float(1)/3;
        else:
            node_dict[node1] = 0;
#        print node1
        node2 = arr[si + 2] + '_' + arr[si + 3];
#            if node2 == input_frames[0] or node2 == input_frames[1] or node2 == input_frames[2]:
#                node_dict[node2] = float(1)/3;
#            else:
#                node_dict[node2] = 0;
        D.add_weighted_edges_from([(node1, node2, float(arr[si + 4]))]);

D = nx.DiGraph();
with open(INPUT_FILE, 'r') as ins:
    for line in ins:
        add_edges_from_line(D, line);

prs = nx.pagerank(D, personalization=node_dict);
sorted_prs = sorted(prs.items(), key=operator.itemgetter(1), reverse=True);
print sorted_prs;
#print prs
w = csv.writer(open(OUTPUT_FILE, 'w'));
k = 1;
for key, val in sorted_prs:
    w.writerow([key, val]);
    k = k + 1;
    if k > m:
        break;
