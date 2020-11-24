import numpy as np 
import torch.nn as nn

class VotingClassifier(object):
    """ Implements a voting classifier for pre-trained classifiers"""

    def __init__(self, estimators):
        self.estimators = estimators

    def predict(self, X):
        # get values
        Y = np.zeros([X.shape[0],50, len(self.estimators)], dtype=int)
        for i, clf in enumerate(self.estimators):
            predict = clf(X)
            Y[:,:, i] = predict.detach().numpy()
        # apply voting 
        y = np.zeros((X.shape[0],len(self.estimators)), dtype='int64')
        pred = np.zeros([X.shape[0], 50], dtype=float)
        for i in range(len(self.estimators)):
            pred = pred + Y[:,:,i]
            for img in range(X.shape[0]):            
                y[img,i] = np.argmax(Y[img,:,i])
                
        pred = pred/len(self.estimators)
        y_max = np.zeros(X.shape[0])
        for i in range(X.shape[0]): 
            y_max[i] = np.argmax(np.bincount(y[i,:])) + 1
        print(y_max.shape, Y.shape, pred.shape)
        return y_max, Y, pred