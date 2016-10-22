import numpy as np
from scipy.spatial.distance import pdist

fv = np.array([0,0,0,0,90,726,359,25,0,0])
cc = np.array([0.018189,3.843977,3.073565,2.464026,28.411075,1114.984640,45.531932,1.585691,0.083266,0.003638])

frameD = pdist(np.vstack([fv,cc]), 'euclidean');

print 'stop'