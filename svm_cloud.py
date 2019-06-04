from sklearn import svm

import numpy as np 

# -------------------- LOAD DATA HERE ---------------------
# n: number of data samples
# m: number of features
# X = data, matrix of size (n,m)
# y = target vectors, vector of size (n,1)

# Samples to be evaluated should be of size (m,1)
svc = svm.SVC(kernel='rbf', gamma = 0.7, C=1.0).fit(X,y) # This trains a SVM classifier with rbf kernel