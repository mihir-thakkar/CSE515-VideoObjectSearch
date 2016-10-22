function distanceMatrix = distanceFrame2Frame(file_one, file_two, task_index)
    
    %frames size of the two files
    frames_f1 = file_one(end, 2);
    frames_f2 = file_two(end, 2);
    
    % Get a r*r 
    r = file_two(end, 3);
    
    %Get size of file_two
    [f2_y, f2_x] = size(file_two); 
    
    distanceMatrix = zeros(frames_f1,frames_f2);
    for i = 1 : frames_f1
        frame_file_one = file_one(file_one(:,2) == i, :);
       for j =1 :frames_f2
           frame_file_two = file_two(file_two(:,2) == j, :);
           distanceMatrix(i,j) = distanceFunctionFrame(frame_file_one, frame_file_two, r, f2_x, task_index)/r;
       end
    end

end


function distance = distanceFunctionFrame(file_one, file_two, f1_y, f1_x, task_index)
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
    distance = sim;
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

