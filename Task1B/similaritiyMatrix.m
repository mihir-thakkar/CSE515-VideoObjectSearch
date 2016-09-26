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

