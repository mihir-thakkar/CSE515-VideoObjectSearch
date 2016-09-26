function EuclideanDist = TaskC_test(query_video, compare_video_file)

    % Read the vidoes
    file1 = dir(strcat('Code/DataR/',query_video));
    file2 = dir(strcat('Code/DataR/',compare_video_file));
    query = VideoReader(file1.name);
    object = VideoReader(file2.name);
    
    % Delete output file if already exists
    if exist('Output/output_phase2_task1c.txt', 'file')==2
        delete('Output/output_phase2_task1c.txt');
    end
    
    % Close all files
    fclose('all');
    
    Frame = 1;
    EuclideanDist = 0;
    
    fid = fopen('Output/output_phase2_task1c.txt','a+');
    fprintf(fid,'%s, ','framenumber','query_x','query_y','objx','objy');
    fprintf(fid,'distance\n');
        
    while hasFrame(query) || hasFrame(object)
        q = readFrame(query);
        o = readFrame(object);
        
        qframe = single(rgb2gray(q)); % Conversion to single is recommended
        oframe = single(rgb2gray(o)); % in the documentation
        
        [F1,D1] = sift(qframe);
        [F2,D2] = sift(oframe);
        
        fid = fopen('Output/output_phase2_task1c.txt','a+');
        % Where 1.5 = ratio between euclidean distance of NN2/NN1
        [matches,score] = siftmatch(D1,D2,1.5);
        for k=1:length(matches)
            fprintf(fid,'%d, ',Frame);
            fprintf(fid,'%f, ',[F1(1,matches(1,k)),F1(2,matches(1,k)),F2(1,matches(2,k)),F2(2,matches(2,k))]);
            fprintf(fid,'%f\n',score(k));
            EuclideanDist = EuclideanDist+score(k);
        end
        Frame = Frame + 1;
        fclose('all');
    end
end