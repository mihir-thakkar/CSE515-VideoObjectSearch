function sim = TaskAorB(video_file_number, compare_video_file_number, database, task_index)
% Calculate the Euclidean or Quadratic distance according to the parameter
% Return an similarity between [0-1]. 
% of task_index(task_index == 0 --> Euclidean, else --> Quadratic).
% Assuming r (resolution) is the same for both videos. 
% Assuming missing frames are completely different, therefore they have a distance on 1. 

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
    diff = 0;
    
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
        diff = min(distance_vectors)*(frames_f2/frames_f1); 
        
        %consider number of frames into the difference, return max
        diff = diff + (difference/frames_f1); 
       
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
        diff = min(distance_vectors)*(frames_f1/frames_f2); 
        
        %consider number of frames into the difference, return max
        diff = diff + (difference/frames_f2); 
        
    else
       % They have the same frame size
       
       %Get size of file_one
       [f1_y, f1_x] = size(file_one); 
       
       diff = distanceFunctions(file_one, file_two, f1_y, f1_x, task_index); 
    end
    
    %compute the similarity between [1-0]
    sim = 1 - diff;  

end

function distance = distanceFunctions(file_one, file_two, f1_y, f1_x, task_index)
%iteratire throguh all the cells and calculate the Euclidean or quadratic Distance.
    sim = 0;
    
    %Used for frame extraction 
    %frame_number = file_one(1,2);
    %frame_file_one = file_one(file_one(:,2) == frame_number, :);
    %
    %frame_number = file_two(1,2);
    %frame_file_two = file_two(file_two(:,2) == frame_number, :);
    
    bins = length(file_one(1, 4: end)); 
    
    if task_index == 0        
        for i =1 :f1_y
            %Get the max distance for the cells
            normal = normalizeCell(file_one(i, :), file_two(i, :), task_index, bins);
            
            %compute the euclidean distance for the cells
            sim = sim + (euclideanDistance(file_one(i, 4: end), file_two(i, 4: end))/normal);        
        end
    else
        %Compute the similarity matrix
        similaritiy_matrix = similaritiyMatrix(f1_x - 3); 
        
        for i =1 :f1_y
            %Get the max distance for the cells
            normal = normalizeCell(file_one(i, :), file_two(i, :), task_index, bins);
            
            %compute the quadratic distance for the cells
            sim = sim + (quadraticDistance(similaritiy_matrix, file_one(i, 4: end), file_two(i, 4: end))/normal);        
        end
    end
    
    %take the average over all the frames
    distance = sim/f1_y;
end


function max_value = normalizeFrame(frame_file_one, frame_file_two, task_index, bins)
    %return the max value possible for a frame to frame comparison
    
    %If there is only one bin
    if bins == 1
        
        %Get the resultion of each frame
        pixles_f1 = sum(sum(frame_file_one(:,4:end)));
        pixles_f2 = sum(sum(frame_file_two(:,4:end)));
        
        max_value = abs(pixles_f1 - pixles_f2); 
        
        if max_value == 0
            max_value = 1; 
        end
    else
        %If there are more than one bin
        
        %Get the resultion of each frame
        pixles_f1 = sum(sum(frame_file_one(:,4:end)));
        pixles_f2 = sum(sum(frame_file_two(:,4:end)));
        
        % for task zero, the max is sqrt((pixles_f1-0)^2+ (0-pixles_f2)^2)
        if task_index == 0
            max_value = (pixles_f1^2 + pixles_f2^2)^(1/2); 
        else
        % for task one, the max is sqrt([pixles_f1,0]*similaritiyMatrix*[0,pixles_f2]')
            similaritiy_matrix = similaritiyMatrix(bins); 
            A = zeros(1,bins);
            B = zeros(1,bins);
             
            A(1) = pixles_f1;
            B(end) = pixles_f2;
            
            max_value = quadraticDistance(similaritiy_matrix, A, B);
        end
    end
    
end


function max_value = normalizeCell(cell_file_one, cell_file_two, task_index, bins)
    %return the max value possible for a cell 2 cell comparison
    
    if bins == 1
        %Get the resultion of each frame
        pixles_f1 = sum(cell_file_one(1,4:end));
        pixles_f2 = sum(cell_file_two(1,4:end));
        
        max_value = abs(pixles_f1 - pixles_f2); 
        
        if max_value == 0
            max_value = 1; 
        end
        
    else
        %If there are more than one bin
        
        %Get the resultion of each frame
        pixles_f1 = sum(cell_file_one(1,4:end));
        pixles_f2 = sum(cell_file_two(1,4:end));
        
        % for task zero, the max is sqrt((pixles_f1-0)^2+ (0-pixles_f2)^2)
        if task_index == 0
            max_value = (pixles_f1^2 + pixles_f2^2)^(1/2); 
        else
        % for task one, the max is sqrt([pixles_f1,0]*similaritiyMatrix*[0,pixles_f2]')
            similaritiy_matrix = similaritiyMatrix(bins); 
            A = zeros(1,bins);
            B = zeros(1,bins);
             
            A(1) = pixles_f1;
            B(end) = pixles_f2;
            
            max_value = quadraticDistance(similaritiy_matrix, A, B);
        end
    end
    
end
