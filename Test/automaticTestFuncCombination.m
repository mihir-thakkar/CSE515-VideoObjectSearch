function automaticTestFuncCombination(testCaseFile, simFileHist, simFileSift, SimFileMotion, ouputFile)
m1 = dlmread(testCaseFile);
m2 = dlmread(simFileHist);
m3 = dlmread(simFileSift);
m4 = dlmread(SimFileMotion);
fileId = fopen(ouputFile, 'w');
[M, N] = size(m1);
total = 0;
success = 0;
fail = 0;
for i = 1 : M
    total = total + 1;
    row = m1(i, :);
    v1 = row(1);
    v2 = row(2);
    v3 = row(3);
    v4 = row(4);
    relation = row(5);
    sim12 = findCombiningSimilarity(v1, v2, m2, m3, m4);
    sim34 = findCombiningSimilarity(v3, v4, m2, m3, m4);
    
    if relation > 0
        result = (sim12 > sim34);
    elseif relation == 0
        result = abs(sim12 - sim34) < 0.05;
    else
        result = (sim12 < sim34);
    end

    if result
        resultStr = 'pass';
        success = success + 1;
    else
        resultStr = 'fail';
        fail = fail + 1;
    end
    fprintf(fileId, '%d,%d,%d,%d,%d,%f,%f,%s\n', v1, v2, v3, v4, relation, sim12, sim34, resultStr);
end
fprintf(fileId, 'Total: %d,  Success: %d,  Fail: %d', total, success, fail);
fclose(fileId);
end