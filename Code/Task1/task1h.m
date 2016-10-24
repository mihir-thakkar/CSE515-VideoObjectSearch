function sim = task1h(videoName1, videoName2)
% calculate the overall similarity with histogram Quadratic, Sift Percentage best match similarity, motion
histSimWeight = 0.4609;
siftSimWeight = 0.5157;
motionSimWeight = 0.0233;
histSim = task1b(videoName1, videoName2);
siftSim = task1c(videoName1, videoName2);   
motionSim = task1f(videoName1, videoName2);
sim = histSim * histSimWeight + siftSim * siftSimWeight + motionSim * motionSimWeight;
end