% Clearing workspace
clear;
O = dlmread('output1R.txt');
Q = dlmread('output1RR.txt');
O = O(:,2:10);
Q = Q(:,2:10);

qframeNos = unique(Q(:,1)).';
oframeNos = unique(O(:,1)).';
firstFrame = true;
frameMeans = [];
for frameNo = qframeNos
    frameD = [];
    qframe = Q(find(Q(:,1) == frameNo),2:9);
    if firstFrame 
       for oframeNo = oframeNos
        oframe = O(find(O(:,1) == oframeNo),2:9);
        D = pdist2(qframe,oframe,'euclidean');
        minD = min(D, [], 2);   
        meanD = mean(minD); 
        frameD = [frameD; [frameNo oframeNo meanD]];        
       end;
       [minFD,I] = min(frameD(:,3));
       onextFrame = frameD(I,2)+1;
       firstFrame = false;
       frameMeans = [frameMeans minFD];
       return;
    else
        oframe = O(find(O(:,1) == onextFrame),2:9);
        D = pdist2(qframe,oframe,'euclidean');
        minD = min(D, [], 2);   
        meanD = mean(minD); 
        onextFrame = onextFrame+1;
        frameMeans = [frameMeans meanD];
    end;    
end;