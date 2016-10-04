% Clearing workspace
clear;
database = dlmread('output.mvect');
fileID = fopen('output.mvect.index');
fileIndex = textscan(fileID,'%s %d','delimiter','=');
fclose(fileID);
objectIndex = 1;
a = 11;
b =67;
k = 3;
objectFile = VideoReader(strcat('DataR/',fileIndex{1}{find(fileIndex{2}(:,1) == objectIndex)}));

object = database(find(database(:,1) == objectIndex),2:7);
vdMat = [];

oframeNos = unique(object(:,1)).';

frameMeans = [];
frameMat = [];
fileID = fopen('cityblock','w');
for i = a:b-1
    qframe = object(find(object(:,1) == i),2:6);
    if ~isempty(qframe) 
    	frameSim = [];
		for j = i+1:b
			oframe = object(find(object(:,1) == j),2:6);
			if ~isempty(oframe) 
				frameD = pdist2(qframe,oframe,'jaccard');
				minD = min(frameD, [], 2);
				meanD = mean(minD); 
				medianD = median(minD); 
				frameSim = [frameSim; [j,meanD,medianD]];
			end;
		end;  
		frameSim = sortrows(frameSim,3)
        [r c] = size(frameMat);
        append = [i frameSim(:,1).'; i frameSim(:,3).'];
        [ar,ac] = size(append);
        append = [append NaN(2,c-ac)];
		frameMat = [frameMat; append]
    end;    
end;
% Closing file
fclose(fileID);
