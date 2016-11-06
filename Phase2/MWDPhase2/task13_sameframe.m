% Clearing workspace
clear;
oName = '3R.txt';
O = dlmread(oName);
O = O(:,2:10);
vdMat = [];
for i = 1:11
    qName = strcat(num2str(i), 'R.txt');
    Q = dlmread(qName);
    Q = Q(:,2:10);

    qframeNos = unique(Q(:,1)).';
    oframeNos = unique(O(:,1)).';
    frameMeans = [];
    for frameNo = qframeNos
        qframe = Q(find(Q(:,1) == frameNo),2:9);
        oframe = O(find(O(:,1) == frameNo),2:9);
        D = pdist2(qframe,oframe,'cosine');
        minD = min(D, [], 2);   
        meanD = mean(minD); 
        frameMeans = [frameMeans meanD];   
    end;
    vdMat = [vdMat; [i mean(frameMeans)]];    
end;
