function file_matrix = retriveDataforFile(file_name)
%Get the file information about a video

    %Get the index for the file
    file_number = getFileNumber(file_name); 
    
    %Get the file name
    whole_db = dlmread('in_file.chst');
    file_matrix =  whole_db(whole_db(:,1) == file_number, :);
end

function [number_file] = getFileNumber(file_name)
    
    fileID = fopen('in_file_index.chst','r');
    number_file = 0; 
    while ~feof(fileID)
        number_file = number_file +1;
        current_file = textscan(fileID,'%s',1,'Delimiter','\n');
        if strcmp(file_name,current_file{1})
           fclose(fileID);  
           return
        end
    end
    
    fclose(fileID);  
end

