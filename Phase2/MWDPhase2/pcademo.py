import numpy as np
from scipy.spatial.distance import cdist
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

database = np.loadtxt('output.mvect', delimiter=";");
t_database = np.column_stack((database[:,0:3],database[:,8]-database[:,6], database[:,9]-database[:,7]))
tr_database = t_database[(t_database[:,3]!=0) | (t_database[:,4]!=0),:];

myVec = tr_database[:,3:5]
pca = PCA(n_components=1)
pca.fit(myVec)
X_pca = pca.transform(myVec);
pca_database = np.column_stack((tr_database[:,0:3], X_pca))
np.savetxt('outfile.mpca', pca_database, delimiter=',',fmt="%d,%d,%d,%.4f")

kmeans = KMeans(n_clusters=1)
kmeans.fit(myVec)
X_km = kmeans.transform(myVec)
kmeans_database = np.column_stack((tr_database[:,0:3], X_km))
np.savetxt('outfile.mkm', pca_database, delimiter=',',fmt="%d,%d,%d,%.4f")

print "Stop";