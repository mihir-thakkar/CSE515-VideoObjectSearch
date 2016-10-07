function task2(v, a, b, inFile, type, k, outputPath)
%     v = 1;
%     a = 3;
%     b = 5;
%     k = 3;
%     inFile = 'out_file.mvect.txt';
    O = dlmread(inFile);
    [row column]=size(O);
    delete ('framerange.txt');
    fid = fopen('framerange.txt', 'a');
    maxfilenumber = max(O(:,1));

    for frame=a:b
        oframe = O(find(O(:,1) == v), 1:column);
        oframe = oframe(find(oframe(:,2) == frame), 1:column);
        [newrow newcolumn]=size(oframe);
        for ROW = 1:newrow
                for COLUMN = 1:newcolumn
                    fprintf(fid, '%d ', oframe(ROW, COLUMN));
                end
                fprintf(fid, '\n');
        end
    end
    delete ('similaritycompare.txt');
    fido = fopen('similaritycompare.txt', 'a');
    
    for video=1:maxfilenumber
        if (video ~= v)
            qframe = O(find(O(:,1) == video), 1:column);
            for frame=1:max(qframe(:,2))
                delete ('queryframerange.txt');
                fidq = fopen('queryframerange.txt', 'a');
                for r=0:b-a
                     if (frame+b-a-1 <= max(qframe(:,2)) && frame >= min(qframe(:,2)))
                         newqframe = qframe(find(qframe(:,2) == frame+r), 1:column);
                         [qrow qcolumn]=size(newqframe);
                         for ROW = 1:qrow
                             for COLUMN = 1:qcolumn
                                 fprintf(fidq, '%d ', newqframe(ROW, COLUMN));
                             end
                             fprintf(fidq, '\n');
                         end

                     end
                 end
                
                %get similarity -> simivalue = task1_a() 
                if (type == 'a')
                    %%%call task1_a input 2 files : framerange.txt , queryframerange.txt
                    %%%store the return similarity value in (int)variable simivalue
                    % simivalue = task1_a() <- i dont know how to call
                elseif (type == 'b')
                    %%%call task1_b input 2 files : framerange.txt , queryframerange.txt
                    %%%store the return similarity value in (int)variable simivalue
                elseif (type == 'c')
                    %%%call task1_c input 2 files : framerange.txt , queryframerange.txt
                    %%%store the return similarity value in (int)variable simivalue
                elseif (type == 'd')
                    %%%call task1_d input 2 files : framerange.txt , queryframerange.txt
                    %%%store the return similarity value in (int)variable simivalue
                elseif (type == 'e')
                    %%%call task1_e input 2 files : framerange.txt , queryframerange.txt
                    %%%store the return similarity value in (int)variable simivalue
                elseif (type == 'f')
                    %%%call task1_f input 2 files : framerange.txt , queryframerange.txt
                    %%%store the return similarity value in (int)variable simivalue
                elseif (type == 'g')
                    %%%call task1_g input 2 files : framerange.txt , queryframerange.txt
                    %%%store the return similarity value in (int)variable simivalue
                end
                fprintf(fido, '%d %d %d %d\n', simivalue, video, frame, frame+b-a-1); %fprint the compared similarity value 

            end
        end
    end
    
    % sort the similarity value and find the k most similar video
    % frame range
    % -> output the result as video (it will create k videos)
    S = dlmread('similaritycompare.txt');
    [B,I] = sort(S(:,1),'descend');
    for kk=1:k
        matchvideo = VideoReader(list(S(I(kk), 2)).name);
        createvideofilename = [ num2str(kk) '_similar.avi'];
        outputVideo = VideoWriter(createvideofilename);
        outputVideo.FrameRate = matchvideo.FrameRate;
        
        for ii = S(I(kk), 3):S(I(kk), 4)
           img = read(matchvideo, ii);
           writeVideo(outputVideo,img)
        end
        close(outputVideo);
    end
    fclose('all');
end
