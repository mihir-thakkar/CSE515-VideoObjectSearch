function similarIndices = findSimilarIndices(querySeqMatrix, videoMatrix, k, type)
% The first column of the querySeqMatrix and the videoMatrix is frame
% index. videoMatrix is the matrix for a single video. similarIndices contains the start frame index of the k most similar frame sequences. 

% k * 2 matrix whic is used to store the start frame indices of k sequences
% in the following format: (start_frame_index, distance)
similarIndices = zeros(k, 2);
similarIndeces(:, 2) = realmax;
% The frame count of query sequence matrix
qCount = size(unique(querySeqMatrix(:, 1)));
% The frame count of video matrix
vCount = size(unique(videoMatrix(:, 1))); 
for i = 1 : vCount - qCount
    distance = getDistance(querySeqMatrix(:, 3:end), videoMatrix(videoMatrix(:, 1) >= i && videoMatrix(:, 1) <= i + vCount, 3:end), type);
    if distance < similarIndeces(k, 2)
        similarIndices(k, 1) = i;
        similarIndices(k, 2) = distance;
        similarIndices = sortrows(similarIndices, 2);
    end
end
end

%TODO: use the methods in task 1 to calculate the distance of two matrices
function distance = getDistance(matrix1, matrix2, type)
    switch type
    case 'a'
        % Use distance method from task 1a
        
    case 'b'
        % Use distance method from task 1b
        
    case 'c'
        % Use distance method from task 1c
        
    case 'd'
        % Use distance method from task 1d
        
    case 'e'
        % Use distance method from task 1e
        
    case 'f'
        % Use distance method from task 1f
        
    case 'g'
        % Use distance method from task 1g
    end
end