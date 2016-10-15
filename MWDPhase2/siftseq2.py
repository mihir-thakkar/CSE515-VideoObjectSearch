import math
import numpy as np
from scipy.spatial.distance import cdist
import pylab
import imageio

frameToFrame = np.loadtxt('outfile.sseq', delimiter=",");

rows,columns = frameToFrame.shape

seq = np.array([])

def myseqfinder(i, j):
    no = frameToFrame[i,j]
    ngi = np.where(frameToFrame[i+1, :]>no)[0][0];
    ng = frameToFrame[i + 1, ngi]
    nei = np.where(frameToFrame[i+1, :]==no)[0][0];
    ne = frameToFrame[i+1,nei]
    nli = np.where(frameToFrame[i+1, :]<no)[0][0];
    nl = frameToFrame[i+1,nli]
    if (nli <= j):
        myseqfinder(i, j + 1)
    if(not nei<=j):
        if (j < nei and nei < ngi):
            myseqfinder(i, j + 1)




    print no;
    myseqfinder(i+1, ngi)
    print "stop"

myseqfinder(0,0)
print "stop"