% Clearing workspace
clear;
database = dlmread('output.mvect');
fileID = fopen('output.mvect.index');
fileIndex = textscan(fileID,'%s %d','delimiter','=');
fclose(fileID);
objectIndex = 12;
object = database(find(database(:,1) == objectIndex),2:7);
oframeNos = unique(object(:,1)).';

vdMat = [];
for queryIndex = 1:13 
	query = database(find(database(:,1) == queryIndex),2:7);
	qframeNos = unique(query(:,1)).';

	frameMeans = [];
	for qframeNo = qframeNos
		frameSim = [];
		qframe = query(find(query(:,1) == qframeNo),2:6);
		for oframeNo = oframeNos
			oframe = object(find(object(:,1) == oframeNo),2:6);
			frameD = pdist2(qframe,oframe,'hamming');
			minD = min(frameD, [], 2);
			meanD = mean(minD); 
			medianD = median(minD); 
			frameSim = [frameSim; [oframeNo,meanD,medianD]];
		end;  
		[minF,I] = min(frameSim(:,3))
		frameMeans = [frameMeans, minF];
	end;
	vdMat = [vdMat; [queryIndex, mean(frameMeans)]];    
end;




