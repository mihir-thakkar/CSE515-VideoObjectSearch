function file_matrix = retriveDataforFile(database, file_number)

    whole_db = dlmread(database);
    index = find(whole_db(:,1) == file_number); 
    file_matrix =  whole_db(index, :);
end

