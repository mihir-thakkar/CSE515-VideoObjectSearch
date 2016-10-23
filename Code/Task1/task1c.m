function similarity = task1c(queryInput, objectInput)

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

    % frameDist matrix contains similarities between all frame pairs
    frameSim=zeros(m,n);

    tic
    % Generate similarities between all frame pairs
    for i=1:m %queryFile.NumberOfFrames
       for j=1:n %objectFile.NumberOfFrames

           % Take only Descriptors from ith and jth frame.
           queryD2 = query(find(query(:,1) == i),7:134);
           D2 = queryD2.';
           objectD1 = object(find(object(:,1) == j),7:134);
           D1 = objectD1.';

           [matches] = siftmatch(D2, D1, 1.2);

            % Frame similarity is calculated by number of similar keypoints
            % with respect to query video
            frameSim(i,j) = length(matches)/length(D2);
       end
     end
    toc

     % Calculate similarity between videos using frameSim matrix
     % containing similarity between each frame pair

     % initialize videoSim matrix of size (m+1)x(n+1)
     videoSim=zeros(m,n); 

     videoSim(1,1)=frameSim(1,1);

     % Initialize first column of videoSim */
     for i=2:m
         videoSim(i,1) = videoSim(i-1,1) + frameSim(i,1);
     end

     % Initialize first row of videoSim */
     for j=2:n
         videoSim(1,j) = videoSim(1,j-1) + frameSim(1,j);
     end

     % Construct rest of the videoSim array by DP memoization */
     for i=2:m
        for j=2:n
            videoSim(i,j) = max([videoSim(i-1,j-1),videoSim(i-1,j),videoSim(i,j-1)])+frameSim(i,j);
        end
     end
    similarity = videoSim(m,n)/(m+n);

end