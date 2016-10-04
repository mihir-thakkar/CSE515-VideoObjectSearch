objectFile = VideoReader('DataR/1R.mp4');
for oframeNo = [20 41]
    figure
    imshow(read(objectFile,oframeNo)), title(strcat('QF=',num2str(oframeNo)));
end;
