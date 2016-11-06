
fileindex = dlmread('videopairs.txt');
[row column]=size(fileindex);
path = fullfile('D:\Courses\CSE 515 Multimedia Database\ProjectPhase1\Code\DataR', '*.mp4');
list = dir(path);
fid = fopen('siftTask1C_similarity.txt', 'a');

database = dlmread('D:\Courses\CSE 515 Multimedia Database\phase2code\cse515group1\Input\in_file.sift');

for X=1:row
    fprintf(fid, '%d,%d,%f\n', fileindex(X, 1), fileindex(X, 2), task1c(list(fileindex(X, 1)).name, list(fileindex(X, 2)).name, database));
end
