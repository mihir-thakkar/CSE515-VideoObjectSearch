profiles = VideoWriter.getProfiles();
myMovie = VideoReader('1R.mp4');
myVideo = VideoWriter('1RM','MPEG-4');
myVideo.FrameRate = 24;
open(myVideo);
while hasFrame(myMovie)
   writeVideo(myVideo, readFrame(myMovie));
end
close(myVideo);
