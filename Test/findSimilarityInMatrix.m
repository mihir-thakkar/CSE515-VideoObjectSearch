% find histogram similarity
function sim = findSimilarityInMatrix(index1, index2, m)
         sim = m((m(:, 1) == index1) & (m(:, 2) == index2), 3);
end