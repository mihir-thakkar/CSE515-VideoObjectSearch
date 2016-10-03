function file_matrix = retriveDataforFile(database, file_number)

    whole_db = dlmread(database);
    file_matrix =  whole_db(whole_db(:,1) == file_number, :);
end

