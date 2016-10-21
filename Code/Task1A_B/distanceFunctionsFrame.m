function distance = distanceFunctionsFrame(file_one, file_two, f1_y, f1_x, task_index, r)
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
        
        file_one_start_frame = file_one(1,2); 
        file_two_start_frame = file_two(1,2);
        
        for i =0 :f1_y/r -1
            
            file_one_frame = sum(file_one(file_one(:,2) == i + file_one_start_frame, :)); 
            file_two_frame = sum(file_two(file_two(:,2) == i + file_two_start_frame, :)); 
            
            %Get the max distance for the cells
            normal = normalizeFrame(file_one_frame, file_two_frame, task_index, bins);
            
            %compute the euclidean distance for the cells
            sim = sim + (euclideanDistance(file_one_frame(1, 4: end), file_two_frame(1, 4: end))/normal);        
        end
    else
        %Compute the similarity matrix
        similaritiy_matrix = similaritiyMatrix(f1_x - 3); 
        
        file_one_start_frame = file_one(1,2); 
        file_two_start_frame = file_two(1,2);
        
        for i =0 :f1_y/r -1
            
            file_one_frame = sum(file_one(file_one(:,2) == i + file_one_start_frame, :)); 
            file_two_frame = sum(file_two(file_two(:,2) == i + file_two_start_frame, :)); 
            %Get the max distance for the cells
            normal = normalizeFrame(file_one_frame, file_two_frame, task_index, bins);
             
            %compute the quadratic distance for the cells
            sim = sim + (quadraticDistance(similaritiy_matrix, file_one_frame(1, 4: end), file_two_frame(1, 4: end))/normal);        
        end
    end
    
    %take the average over all the frames
    distance = sim;
end


function max_value = normalizeFrame(frame_file_one, frame_file_two, task_index, bins)
    %return the max value possible for a cell 2 cell comparison
    
    if bins == 1
        %Get the resultion of each frame
        pixles_f1 = sum(sum(frame_file_one(1,4:end)));
        pixles_f2 = sum(sum(frame_file_two(1,4:end)));
        
        max_value = abs(pixles_f1 - pixles_f2); 
        
        if max_value == 0
            max_value = 1; 
        end
        
    else
        %If there are more than one bin
        
        %Get the resultion of each frame
        pixles_f1 = sum(sum(frame_file_one(1,4:end)));
        pixles_f2 = sum(sum(frame_file_two(1,4:end)));
        
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
