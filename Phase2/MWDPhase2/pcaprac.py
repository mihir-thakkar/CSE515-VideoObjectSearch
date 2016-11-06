import numpy as np
from scipy.spatial.distance import cdist
from sklearn.decomposition import PCA

all_samples = np.array([[1,7,4],[5,2,9],[12,6,2],[3,11,7]])
mean_vector = np.mean(all_samples,axis=0);
scatter_matrix = np.zeros((3,3))
for i in range(all_samples.shape[0]):
    scatter_matrix += (all_samples[i,:] - mean_vector).T.dot((all_samples[i,:] - mean_vector))
print('Scatter Matrix:\n', scatter_matrix)
cov_mat = np.cov(all_samples.T)
print('COV Matrix:\n', cov_mat)
pca = PCA(n_components=3)
pca.fit(all_samples)
X_new = pca.transform(all_samples);
print('X Matrix:\n', pca.components_);
print "Stop";
