function pcaConvert(inFile, outDimen, outFile)
whole_db = dlmread(inFile);
matrix = whole_db(:, 4:end);
% Get the matrix of video, frame and cell indices
vfcMatrix = whole_db(:, 1:3);
[coeff, scores, latent] = pca(matrix, 'NumComponents', outDimen);
resultMatrix = horzcat(vfcMatrix, scores);
dlmwrite(outFile, resultMatrix);
end