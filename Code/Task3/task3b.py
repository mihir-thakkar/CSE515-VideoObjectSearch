import numpy as np
from sklearn.decomposition import PCA

database = None
def preprocessing():
    global database
    database = np.loadtxt('../Input/in_file.sift', delimiter=",")

def reduce(d):
    allVectors = database[:, 3:]
    pca = PCA(n_components=d)
    pca.fit(allVectors)
    transformedPCA = pca.transform(allVectors);
    pca_database = np.column_stack((database[:, 0:3], transformedPCA))
    np.savetxt('../Input/in_file_d.spca', pca_database, delimiter=',', fmt="%d,%d,%d" + ",%.4f" * d)
    score = pca.components_
    score_mat = np.array([]).reshape(0, 3)
    for i in range(0, score.shape[0]):
        for j in range(0, score.shape[1]):
            score_mat = np.vstack([score_mat, [i + 1, j + 1, score[i, j]]])
    np.savetxt('../Input/in_file_d.spca.score', score_mat, delimiter=',', fmt="%d,%d,%f")

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
