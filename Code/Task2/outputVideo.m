function outputVideo(index, vi, fi, frameCount, videoDir, outputDir)
%index-- similar priority
%vi-- video index
%fi-- start frame index
%frameCount-- sequence length
%videoDir-- original videos directory
%outputDir-- output similar videos directory
%eg. outputVideo(1, 2, 1, 10, 'Code\DataR', 'Code\DataR')

% get the video path and name
[vPath, vName] = getVideoPath(videoDir, vi);
% read the sequence from the start frame index fi and write it to a new
% video file under outputPath
originalVideo = VideoReader(vPath);
% read the similar frame sequence
% frames = read(originalVideo, [fi, fi + frameCount - 1]);
% prepare the output file name
filename = sprintf('%d_v%d_f%d_%s.mp4', index, vi, fi, vName);
outputVideo = VideoWriter(fullfile(outputDir, filename));
% the output video has the same frame rate as the original one
outputVideo.FrameRate = originalVideo.FrameRate;
open(outputVideo);
i = 1;
% the end frame index of the specified sequence
endIndex = fi + frameCount -1;
% Read and ouput the specified sequence
while hasFrame(originalVideo)
    frame = readFrame(originalVideo);
    if i >= fi && i <= endIndex
        writeVideo(outputVideo, frame)
    else i > endIndex;
         break
    end
    i = i + 1;
end
close(outputVideo);
end