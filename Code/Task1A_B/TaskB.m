function sim = TaskB( IndexFile ,video_file_name, compare_video_file_name, database)
% Calculate the Quadratic distance between two videos.
    sim = TaskAorB(IndexFile, video_file_name, compare_video_file_name, database, 1);  
end

