function sim = TaskA(IndexFile ,video_file_name, compare_video_file_name, database)
% Calculate the Euclidean distance between two videos.
    sim = TaskAorB(IndexFile ,video_file_name, compare_video_file_name, database, 0);
end
