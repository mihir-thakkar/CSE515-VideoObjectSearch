function task2(v, a, b, inFile, type, k, outputPath)
%     v = 1;
%     a = 3;
%     b = 5;
%     k = 3;
    inFile = 'out_file.mvect.txt';
    O = dlmread(inFile);
    [row column]=size(O);

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
                %fprintf(fidq, '%d\n', max(qframe(:,2)));
                fprintf(fidq, '\n');
                
                %%%%%%%%%similarity
                if (type == 'a')
                    
                end

            end
        end
    end
end