%Let's make some fake data with two groups
clear;
database = dlmread('output.sift');

[IDX,C] = kmeans(database(:,8:135),10); %Run k-means, asking for two groups

