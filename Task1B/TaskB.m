function sim = TaskB( video_file_number, compare_video_file_number, database)
    
    %Get the matrix for file one
    file_one = retriveDataforFile(database, video_file_number); 
    
    %Get size of file_one
    [f1_y, f1_x] = size(file_one);  
    
    %Get the matrix for file two
    file_two = retriveDataforFile(database, compare_video_file_number);
    
    %Compute the similarity matrix
    similaritiy_matrix = similaritiyMatrix(f1_x - 3); 
    
    %iteratire throguh all the cells and calculate the quadratic Distance.
    sim = 0; 
    
    for i =1 :f1_y
        sim = sim + quadraticDistance(similaritiy_matrix, file_one(i, 4: end), file_two(i, 4: end));        
    end
    
    sim = sim/f1_y;  
end

