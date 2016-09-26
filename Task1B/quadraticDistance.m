function value = quadraticDistance( similaritiy_matrix, A, B)
% This function takes in the A and B vector to computes the Quadratic Distance
    ab = (A-B)'; 
    value  = sqrt(ab'*similaritiy_matrix*ab); 
end

