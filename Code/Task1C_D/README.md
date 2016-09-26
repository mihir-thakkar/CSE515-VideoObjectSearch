------------------------------------------------------
	Phase 2 Task 1 C and D Command Line Arguments
------------------------------------------------------

Execution instructions:

	1. Go inside cse515group1 directory.
	2. Add this folder and subfolders to Matlab path.
	3. Run following command in Matlab console:
		disp(TaskC_test(query_video_filename,compare_video_filename));

Example:

	disp(TaskC_test('1R.mp4','2R.mp4'))

Expected output:
	1. Euclidean distance between given two videos.
	2. An output file containing matched keypoints based on SIFT descriptor.
	3. Format of output vectors:
		<framenumber, queryx, queryy, objx, objy, euclidean_dist>

		where;
		framenumber - SIFT frame number.
		queryx, queryy - coordinates of keypoints in query frame.
		objx, objy - coordinates of keypoints in object frame.
		euclidean_dist - Euclidean distance between keypoint.