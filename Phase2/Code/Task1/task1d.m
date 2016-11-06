function similarity = task1d(queryInput, objectInput)
    
    % SIFT vectors database and video names meta data
    database = dlmread('Input/in_file.sift');
    fileID = fopen('Input/in_file.index');
    fileIndex = textscan(fileID,'%s %d','delimiter','=','headerLines', 1);
    fclose(fileID);

    % Init video number for query and object videos
    % Retrieve indexes from meta data
    objectIndex = find(strcmp(fileIndex{1}(:,1), objectInput));
    queryIndex = find(strcmp(fileIndex{1}(:,1), queryInput));

    % Take only F1, D1. Discard video number, frame number and cell number
    object = database(find(database(:,1) == objectIndex),2:135);
    query = database(find(database(:,1) == queryIndex),2:135);

    % frame number array in object and query video
    qframeNos = unique(query(:,1)).';
    oframeNos = unique(object(:,1)).';

    % m - length of query video, n - length of object video
    m = length(qframeNos);
    n = length(oframeNos);

    % frameSim matrix contains distances between all frame pairs
    frameDist=zeros(m,n);

    % Generate distances between all frame pairs
    for i=1:m %queryFile.NumberOfFrames
       for j=1:n %objectFile.NumberOfFrames

           % Take only Descriptors from ith and jth frame.
           queryD2 = query(find(query(:,1) == i),7:134);
           objectD1 = object(find(object(:,1) == j),7:134); 

           distMat = pdist2(queryD2, objectD1, 'euclidean');
           score = min(distMat, [], 2);

            % Avg of euclidean distances of all best match keypoint pairs
           frameDist(i,j) = sum(score)/length(queryD2);
       end
     end

     % Calculate distance between videos using frameSim matrix
     % containing distance between each frame pair
    tic
     % initialize videoDist matrix of size (m)x(n)
     videoDist=zeros(m,n); 

     videoDist(1,1)=frameDist(1,1);

     % Initialize first column of videoDist */
     for i=2:m
         videoDist(i,1) = videoDist(i-1,1) + frameDist(i,1);
     end

     % Initialize first row of videoDist */
     for j=2:n
         videoDist(1,j) = videoDist(1,j-1) + frameDist(1,j);
     end

     % Construct rest of the videoDist array */
     for i=2:m
        for j=2:n
            videoDist(i,j) = min([videoDist(i-1,j-1),videoDist(i-1,j),videoDist(i,j-1)])+frameDist(i,j);
        end
     end
     toc
     DIST = videoDist(m,n)/(m+n);
     similarity = 1-DIST;
end