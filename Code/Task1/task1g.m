function sim = task1g(videoName1, videoName2)
% calculate the overall similarity with histogram Euclidean, Sift Euclidean, motion
% similarity.
histSimWeight = 0.4609;
siftSimWeight = 0.5157;
motionSimWeight = 0.0233;
histSim = task1a(videoName1, videoName2);
siftSim = task1c(videoName1, videoName2);   
motionSim = task1e(videoName1, videoName2);
sim = histSim * histSimWeight + siftSim * siftSimWeight + motionSim * motionSimWeight;
end