% Clearing workspace
clear;
oName = 'object.txt';
O = dlmread(oName);
O = O(:,2:10);
oframe = O(find(O(:,1) == 2),2:9);
C = cov(oframe);
[V,D,W] = eig(C);