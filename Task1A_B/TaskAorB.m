function sim = TaskAorB(video_file_number, compare_video_file_number, database, task_index)
% Calculate the Euclidean or Quadratic distance according to the parameter
% of task_index(task_index == 0 --> Euclidean, else --> Quadratic).
   
    %Get the matrix for file one
    file_one = retriveDataforFile(database, video_file_number); 
    
    %Get size of file_one
    [f1_y, f1_x] = size(file_one);  
    
    %Get the matrix for file two
    file_two = retriveDataforFile(database, compare_video_file_number);
    
    %iteratire throguh all the cells and calculate the Euclidean or quadratic Distance.
    sim = 0;
    
    if task_index == 0
        for i =1 :f1_y
            sim = sim + euclideanDistance(file_one(i, 4: end), file_two(i, 4: end));        
        end
    else
        %Compute the similarity matrix
        similaritiy_matrix = similaritiyMatrix(f1_x - 3); 
        for i =1 :f1_y
            sim = sim + quadraticDistance(similaritiy_matrix, file_one(i, 4: end), file_two(i, 4: end));        
        end
    end
    
    sim = sim/f1_y;  
end