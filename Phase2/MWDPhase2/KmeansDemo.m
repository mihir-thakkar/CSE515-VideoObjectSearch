%Let's make some fake data with two groups
clear;
database = dlmread('output.mvect');
fileID = fopen('output.mvect.index');
fileIndex = textscan(fileID,'%s %d','delimiter','=');
fclose(fileID);
objectIndex = 1;
queryIndex = 8;
objectFile = VideoReader(strcat('DataR/',fileIndex{1}{find(fileIndex{2}(:,1) == objectIndex)}));
queryFile = VideoReader(strcat('DataR/',fileIndex{1}{find(fileIndex{2}(:,1) == queryIndex)}));


object = database(find(database(:,1) == objectIndex),2:7);
query = database(find(database(:,1) == queryIndex),2:7);

qframeNos = unique(query(:,1)).';
oframeNos = unique(object(:,1)).';

oKD = [];
for oframeNo = oframeNos
	oframe = object(find(object(:,1) == oframeNo),2:6);
	[IDX,C]=kmeans(oframe,1); %Run k-means, asking for two groups
	oKD = [oKD;[oframeNo,C]];
end;

qKD = [];
for qframeNo = qframeNos
	qframe = query(find(query(:,1) == qframeNo),2:6);
	[IDX,C]=kmeans(qframe,1); %Run k-means, asking for two groups
	qKD = [qKD;[qframeNo,C]];
end;

frameD = pdist2(qKD,oKD,'euclidean');
[M,I] = min(frameD, [], 2);

sim = mean(M);
