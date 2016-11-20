import imageio
import numpy as np
import os

INPUT_VIDEO_PATH = '../Input/Videos/'
INPUT_INDEX = '../Input/in_file.index'
OUTPUT_PATH = '../Output/Frames/'

def output_frame(video_index, frame_index, output_name):

    #Creating video name to video num index and reverse index
    fileIndex = np.genfromtxt(INPUT_INDEX, delimiter="=", dtype=None, skip_header=1)
    fileIndex = dict(fileIndex)
    revIndex = {v: k for k, v in fileIndex.iteritems()}

    # Creating output path if not exist
    if not os.path.isdir(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    video_name = revIndex[int(video_index)];
    objectFile = imageio.get_reader(INPUT_VIDEO_PATH + video_name, 'ffmpeg')
    oimage = objectFile.get_data(int(frame_index))
    imageio.imwrite(OUTPUT_PATH + output_name, oimage)


def output_a_frame(vi_fi, prefix, rank=None):
    a = str(vi_fi).split('_');
    if rank is not None:
        output_name = prefix + '_' + vi_fi + '_rank' + rank + '.png';
    else:
        output_name = prefix + '_' + vi_fi + '.png';
    output_frame(a[0], a[1], output_name);