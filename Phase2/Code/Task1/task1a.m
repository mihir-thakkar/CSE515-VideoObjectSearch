function sim = task1a( video_file_name, compare_video_file_name)
% Calculate the Euclidean Distance
% Return an similarity between [0-1]. 
% Assuming r (resolution) is the same for both videos.  

    %Get the matrix for file one
    file_one = retriveDataforFile(video_file_name); 
        
    %Get the matrix for file two
    file_two = retriveDataforFile(compare_video_file_name);
    
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
            %
            sum_frames_front = 0; 
            for j = 0 : i-1
                sum_frames_front = sum_frames_front + distanceFunctions(file_one(j*r+1:r+j*r, :), file_two(1:r,:), 1); 
            end
            
            sum_frames_back = 0; 
            for j = 0 : difference-1-i
                sum_frames_back = sum_frames_back + distanceFunctions(file_one(f2_y+j*r+1 : f2_y+j*r+r, :), file_two(end-r+1:end,:), 1); 
            end
            
            distance_vectors(1, i+1) = (sum_frames_back + sum_frames_front + distanceFunctions(file_one(i*r+1:f2_y +i*r, :), file_two, f2_y))/(frames_f1*r);     
        end
        
        %return the min dsitance
        diff = min(distance_vectors); 
        
    elseif frames_f1 < frames_f2
        % file_two has more frames is greater than others
        
        % get the difference between frames
        difference = frames_f2 - frames_f1; 
        distance_vectors = zeros(1, difference+1);
       
        %Get size of file_one
        [f1_y, f1_x] = size(file_one);  
       
        % Get all the frames comparison
        for i=0 : difference
            
            sum_frames_front = 0; 
            for j = 0 : i-1
                sum_frames_front = sum_frames_front + distanceFunctions(file_two(j*r+1:r+j*r, :), file_one(1:r,:), 1); 
            end
            
            sum_frames_back = 0; 
            for j = 0 : difference-1-i
                sum_frames_back = sum_frames_back + distanceFunctions(file_two(f1_y+j*r+1 : f1_y+j*r+r, :), file_one(end-r+1:end,:), 1); 
            end
            
            distance_vectors(1, i+1) = (sum_frames_back + sum_frames_front + distanceFunctions(file_two(i*r+1:f1_y +i*r, :), file_one, f1_y))/(frames_f2*r);   
        end
        
        %return the min dsitance
        diff = min(distance_vectors); 
        
    else
       % They have the same frame size
       
       %Get size of file_one
       [f1_y, f1_x] = size(file_one); 
       
       diff = (distanceFunctions(file_one, file_two, f1_y)/f1_y); 
    end
    
    %compute the similarity between [1-0]
    sim = 1 - diff;  

end

function file_matrix = retriveDataforFile(file_name)
%Get the file information about a video

    %Get the index for the file
    file_number = getFileNumber(file_name); 
    
    %Get the file name
    whole_db = dlmread('Input/in_file.chst');
    file_matrix =  whole_db(whole_db(:,1) == file_number, :);
end

function [number_file] = getFileNumber(file_name)
    
    fileID = fopen('Input/in_file.index','r');
    fileIndex = textscan(fileID,'%s %d','delimiter','=','headerLines', 1);
    fclose(fileID);
    
    number_file = find(strcmp(fileIndex{1}(:,1), file_name)); 
end

function value = euclideanDistance(A, B)
% This function takes in the A and B vector to computes the Euclidean Distance
    value = norm(A - B);
end


function distance = distanceFunctions(file_one, file_two, f1_y)
%iteratire throguh all the cells and calculate the Euclidean or quadratic Distance.
    sim = 0;    
    bins = length(file_one(1, 4: end)); 
         
    for i =1 :f1_y
        %Get the max distance for the cells
        normal = normalizeCell(file_one(i, :), file_two(i, :), bins);
            
        %compute the euclidean distance for the cells
        sim = sim + (euclideanDistance(file_one(i, 4: end), file_two(i, 4: end))/normal);        
    end
    
    %take the average over all the frames
    distance = sim;
end


function max_value = normalizeCell(cell_file_one, cell_file_two, bins)
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
        
        %Get the resultion of each frame
        pixles_f1 = sum(cell_file_one(1,4:end));
        pixles_f2 = sum(cell_file_two(1,4:end));
        max_value = (pixles_f1^2 + pixles_f2^2)^(1/2);
        
    end
    
end


