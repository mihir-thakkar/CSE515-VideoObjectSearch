function sim = task1b( video_file_name, compare_video_file_name)
% Calculate the Quadratic Distance
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
                sum_frames_front = sum_frames_front + distanceFunctions(file_one(j*r+1:r+j*r, :), file_two(1:r,:), 1,f2_x); 
            end
            
            sum_frames_back = 0; 
            for j = 0 : difference-1-i
                sum_frames_back = sum_frames_back + distanceFunctions(file_one(f2_y+j*r+1 : f2_y+j*r+r, :), file_two(end-r+1:end,:), 1,f2_x); 
            end
            
            distance_vectors(1, i+1) = (sum_frames_back + sum_frames_front + distanceFunctions(file_one(i*r+1:f2_y +i*r, :), file_two, f2_y,f2_x))/(frames_f1*r);     
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
                sum_frames_front = sum_frames_front + distanceFunctions(file_two(j*r+1:r+j*r, :), file_one(1:r,:), 1,f1_x); 
            end
            
            sum_frames_back = 0; 
            for j = 0 : difference-1-i
                sum_frames_back = sum_frames_back + distanceFunctions(file_two(f1_y+j*r+1 : f1_y+j*r+r, :), file_one(end-r+1:end,:), 1,f1_x); 
            end
            
            distance_vectors(1, i+1) = (sum_frames_back + sum_frames_front + distanceFunctions(file_two(i*r+1:f1_y +i*r, :), file_one, f1_y,f1_x))/(frames_f2*r);   
        end
        
        %return the min dsitance
        diff = min(distance_vectors); 
        
    else
       % They have the same frame size
       
       %Get size of file_one
       [f1_y, f1_x] = size(file_one); 
       
       diff = (distanceFunctions(file_one, file_two, f1_y,f1_x)/f1_y); 
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

function value = quadraticDistance( similaritiy_matrix, A, B)
% This function takes in the A and B vector to computes the Quadratic Distance
    ab = (A-B)'; 
    value  = sqrt(ab'*similaritiy_matrix*ab); 
end

function matrix = similaritiyMatrix( input )
%This function computes the similaritiy matrix for grayscale histograms

    % Initialize the similaritiy matrix
    matrix = zeros(input, input); 

    % Edges
    edges = 0: 255/input: 255; 
    mid_edges = zeros(input, 1);  

    % Compute the midpoints
    for i = 1 : input
        mid_edges(i) = (edges(i)+ edges(i+1))/2; 
    end

    % Compute the matrix 
    for i = 1 : input
        current_row = zeros(input, 1); 
        for j = 1 : input
            current_row(j)= abs(mid_edges(i) - mid_edges(j));
        end
        matrix(:, i) =  current_row; 
    end
    
    % Normalize the number
    matrix = 1 - matrix/255;
    
end

function distance = distanceFunctions(file_one, file_two, f1_y, f1_x)
%iteratire throguh all the cells and calculate the Quadratic Distance.
    sim = 0;    
    bins = length(file_one(1, 4: end)); 
         
    similaritiy_matrix = similaritiyMatrix(f1_x - 3); 
        
    for i =1 :f1_y
        %Get the max distance for the cells
        normal = normalizeCell(file_one(i, :), file_two(i, :), bins);
            
        %compute the quadratic distance for the cells
        sim = sim + (quadraticDistance(similaritiy_matrix, file_one(i, 4: end), file_two(i, 4: end))/normal);        
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
        %If there are more than one bin
        
        %Get the resultion of each frame
        pixles_f1 = sum(cell_file_one(1,4:end));
        pixles_f2 = sum(cell_file_two(1,4:end));
        
        % for task one, the max is sqrt([pixles_f1,0]*similaritiyMatrix*[0,pixles_f2]')
        similaritiy_matrix = similaritiyMatrix(bins); 
        A = zeros(1,bins);
        B = zeros(1,bins);
             
        A(1) = pixles_f1;
        B(end) = pixles_f2;
            
        max_value = quadraticDistance(similaritiy_matrix, A, B);
        
    end
    
end
