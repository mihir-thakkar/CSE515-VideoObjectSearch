function [path, name] = getVideoPath(videoDir, vi)
% find the video path and name (without suffix)with the given video index vi.
% eg. [path, name] = getVideoPath('Code\DataR', 1)
files = dir(fullfile(videoDir, '*.mp4'));
path = fullfile(videoDir, files(vi).name);
a = strsplit(files(vi).name, '.');
name = a{1};
end