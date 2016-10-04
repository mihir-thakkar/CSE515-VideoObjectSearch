% Clearing workspace
clear;
database = dlmread('output.mvect');
fileID = fopen('output.mvect.index');
fileIndex = textscan(fileID,'%s %d','delimiter','=');
fclose(fileID);
objectIndex = 1;
queryIndex = 3;
objectFile = VideoReader(strcat('DataR/',fileIndex{1}{find(fileIndex{2}(:,1) == objectIndex)}));
queryFile = VideoReader(strcat('DataR/',fileIndex{1}{find(fileIndex{2}(:,1) == queryIndex)}));


object = database(find(database(:,1) == objectIndex),2:7);
query = database(find(database(:,1) == queryIndex),2:7);
vdMat = [];

qframeNos = unique(query(:,1)).';
oframeNos = unique(object(:,1)).';

frameMeans = [];
fileID = fopen('cityblock','w');
for qframeNo = qframeNos
	frameSim = [];
    qframe = query(find(query(:,1) == qframeNo),2:6);
    CM = cov(qframe);
    for oframeNo = oframeNos
    	oframe = object(find(object(:,1) == oframeNo),2:6);
    	frameD = mahal(qframe,oframe);
    	minD = min(frameD, [], 2);
    	meanD = mean(minD); 
    	medianD = median(minD); 
    	frameSim = [frameSim; [oframeNo,meanD,medianD]];
    end;  
    %{
    [minF,I] = sort(frameSim(:,3))
    frames = [];
    for i = 1:5
    	frames = [frames, read(objectFile,frameSim(I(i,1),1))];
    end;
    %}
    [minF,I] = min(frameSim(:,3))
    frameMeans = [frameMeans, minF];
    %{
    figure
    subplot(1,2,1), imshow(read(queryFile,qframeNo)), title(strcat('QF=',num2str(qframeNo)));
	subplot(1,2,2), imshow(read(objectFile,frameSim(I,1))), title(strcat('OF=',num2str(frameSim(I,1))));
	%}
	nbytes = fprintf(fileID,'%d--->%d\n',qframeNo,frameSim(I,1));
end;
% Closing file
fclose(fileID);
vdMat = [vdMat; [i mean(frameMeans)]];    
