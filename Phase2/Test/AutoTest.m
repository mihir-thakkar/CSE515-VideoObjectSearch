% Test histogram Euclidean similarity
testcaseFile = 'testcases/Test_Cases_Histogram_Latest.txt';
similarityFile = 'similarityData/hist_similarity_a.txt';
testResultFile = 'testResult/hist_euclidean_sim_test_result.txt';
automaticTestFunc(testcaseFile, similarityFile, testResultFile);

% Test histogram Quadratic similarity
similarityFile = 'similarityData/hist_similarity_b.txt';
testResultFile = 'testResult/hist_quadratic_sim_test_result.txt';
automaticTestFunc(testcaseFile, similarityFile, testResultFile);

% Test Motion Euclidean similarity
testcaseFile = 'testcases/motion_testcase_more.txt';
similarityFile = 'similarityData/motion_similarity_Euc.txt';
testResultFile = 'testResult/motion_euclidean_sim_test_result.txt';
automaticTestFunc(testcaseFile, similarityFile, testResultFile);

% Test Motion Euclidean distance
testcaseFile = 'testcases/motion_testcase_more.txt';
similarityFile = 'similarityData/motion_distance_5.txt';
testResultFile = 'testResult/motion_euclidean_distance_test_result.txt';
automaticTestFuncDistance(testcaseFile, similarityFile, testResultFile);

% Test Sift Euclidean similarity
testcaseFile = 'testcases/Test_Cases_Sift.txt';
similarityFile = 'similarityData/sift_similarity_Euc_Mihir.txt';
testResultFile = 'testResult/sift_euclidean_sim_test_result.txt';
automaticTestFunc(testcaseFile, similarityFile, testResultFile);