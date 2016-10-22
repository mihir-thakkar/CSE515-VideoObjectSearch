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
