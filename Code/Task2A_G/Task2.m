function Task2(v, a, b, inFile, type, k, outputPath)
% v-- video index
% a-- start query frame index
% b-- end query frame index
% inFile-- input file such as in_file.chst
% type-- the method will be used to compute the distance
% k-- the number of ouput sequences
% outputPath-- the path for output videos

wholeMatrix = dlmread(inFile);
% get the query video matrix
vMatrix = wholeMatrix(wholeMatrix(:,1) == v, :);
% get the query sequences matrix
querySeqMatrix = vMatrix(vMatrix(:, 2) >= a && vMatrix(:, 2) <= b, 2:end);
% the matrix of remaining videos other than the one used as query matrix
remainVideosMatrix = wholeMatrix(wholeMatrix(:,1) ~= v, :);
% the indices of remaining videos
remainVideoIndices = unique(remainVideosMatrix(:, 1));
% the count of remaining videos
remainVideoCount = size(remainVideoIndices);
% the matrix used to store indices for k sequences in the following form:
% (video_index, start_frame_index, distance)
similarSeqIndices = zeros(k, 3);
similarSeqIndices(:, 3) = realmax;
for i = 1 : remainVideoCount
    vIndex = remainVideoIndices(i);
    vMatrix = remainVideosMatrix(remainVideosMatrix(:, 1) == vIndex, 2:end);
    similarIndices = findSimilarIndices(querySeqMatrix, vMatrix, k, type);
    % concatenate video index to similarIndices
    vIndexColumn = zeros(k, 1);
    vIndexColumn(:, 1) = vIndex;
    % m is in the same format as similarSeqIndices
    m = horzcat(vIndexColumn, similarIndices);
    % put the two k * 3 matrix together vertically to select the k most
    % similar sequences
    n = vertcat(similarIndices, m);
    % sort m according to the distance column
    n = sortrows(n, 3);
    %select the k most similar sequences
    similarSeqIndices = n(1:k, :);
end
% the length of query sequence
seqLength = b - a + 1;
% Create and output videos according to the similar sequence indices
for i = 1 : k
    writeVideo(similarSeqIndices(i, 1), similarSeqIndices(i, 2), seqLength, outputPath);
end
end

function writeVideo(vi, fi, frameCount, outputPath)
vPath = getVideoPath(vi);
% TODO: read the sequence from the start frame index of fi and write it to a new
% video file under outputPath
end