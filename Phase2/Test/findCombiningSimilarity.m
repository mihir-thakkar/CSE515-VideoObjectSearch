    function sim = findCombiningSimilarity(index1, index2, histSimMatrix, siftSimMatrix, motionSimMatrix)
    histSimWeight = 0.4609;
    siftSimWeight = 0.5157;
    motionSimWeight = 0.0233;
    histSim = findSimilarityInMatrix(index1, index2, histSimMatrix);
    siftSim = findSimilarityInMatrix(index1, index2, siftSimMatrix);
    motionSim = findSimilarityInMatrix(index1, index2, motionSimMatrix);
    sim = histSim * histSimWeight + siftSim * siftSimWeight + motionSim * motionSimWeight;
    end