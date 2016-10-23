import numpy as np
from sklearn.cluster import KMeans

database = None
#this will hold initially reduced database
database_ired = None
def preprocessing():
    global database, database_ired
    database = np.loadtxt('../Input/in_file.mvect', delimiter=",")
    transformedDatabase = np.column_stack((database[:, 0:3], database[:, 8] - database[:, 6], database[:, 9] - database[:, 7]))
    database_ired = transformedDatabase[(transformedDatabase[:, 3] != 0) | (transformedDatabase[:, 4] != 0), :]


def reduce(d):
    allVectors = database_ired[:, 3:]
    kmeans = KMeans(n_clusters=d)
    kmeans.fit(allVectors)
    transformedKmeans = kmeans.transform(allVectors);
    kmeans_database = np.column_stack((database[:, 0:3], transformedKmeans))
    np.savetxt('../Input/in_file_d.mkm', kmeans_database, delimiter=',', fmt="%d,%d,%d" + ",%.4f" * d)
    score = kmeans.cluster_centers_
    score_mat = np.array([]).reshape(0, 3)
    for i in range(0, score.shape[0]):
        for j in range(0, score.shape[1]):
            score_mat = np.vstack([score_mat, [i + 1, j + 1, score[i, j]]])
    np.savetxt('../Input/in_file_d.mkm.score', score_mat, delimiter=',', fmt="%d,%d,%f")

if __name__ == '__main__':
    preprocessing()
    flag = 1
    while flag :
        d = int(input("Enter the target dimensionality: "))
        if d <=0 :
            print 'Target Dimensionality must be positive.'
        elif d > (database.shape[1]-3) :
            print 'Target Dimensionality must be less or equal to existing dimensionality.'
        else : flag = 0
    reduce(d)
