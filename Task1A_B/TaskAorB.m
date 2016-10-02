function sim = TaskAorB(video_file_number, compare_video_file_number, database, task_index)
% Calculate the Euclidean or Quadratic distance according to the parameter
% of task_index(task_index == 0 --> Euclidean, else --> Quadratic).
% Assuming r (resolution) is the same
   
    %Get the matrix for file one
    file_one = retriveDataforFile(database, video_file_number); 
        
    %Get the matrix for file two
    file_two = retriveDataforFile(database, compare_video_file_number);
    
    %frames size of the two foles
    frames_f1 = file_one(end, 2);
    frames_f2 = file_two(end, 2);
    
    % Get a r*r 
    r = file_two(end, 3);
    
    % Output equals zero
    sim = 0;
    
    if frames_f1 > frames_f2
        % file_one has more frames is greater than others
        
        % get the difference between frames
        difference = frames_f1 - frames_f2; 
        distance_vectors = zeros(1, difference+1);
       
        %Get size of file_two
        [f2_y, f2_x] = size(file_two);  
        
        % Get all the frames comparison
        % Ex: F1  F2
        %     1   6
        %     2   7 
        %     3  
        %  compare [1,2] with [6,7] and [2,3] with [6,7]
        
        for i=0 : difference
            distance_vectors(1, i+1) = distanceFunctions(file_one(i*r+1:f2_y +i*r, :), file_two, f2_y, f2_x, task_index);     
        end
        
        %return the min dsitance
        sim = min(distance_vectors); 
       
    elseif frames_f1 < frames_f2
        % file_two has more frames is greater than others
        
        % get the difference between frames
        difference = frames_f2 - frames_f1; 
        distance_vectors = zeros(1, difference+1);
       
        %Get size of file_one
        [f1_y, f1_x] = size(file_one);  
       
        % Get all the frames comparison
        for i=0 : difference
            distance_vectors(1, i+1) = distanceFunctions(file_two(i*r+1:f1_y +i*r, :), file_one, f1_y, f1_x, task_index);   
        end
        
        %return the min dsitance
        sim = min(distance_vectors); 
        
    else
       % They have the same frame size
       
       %Get size of file_one
       [f1_y, f1_x] = size(file_one); 
       
       sim = distanceFunctions(file_one, file_two, f1_y, f1_x, task_index); 
    end

end

function distance = distanceFunctions(file_one, file_two, f1_y, f1_x, task_index)
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
    
    distance = sim/f1_y;
end
