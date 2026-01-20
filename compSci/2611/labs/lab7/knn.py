import random

import numpy as np
from scipy.spatial import distance
from scipy import stats
import math

class KNN:
    """
    Implementation of the k-nearest neighbors algorithm for classification.
    """
    def __init__(self, k):
        """
        Takes one parameter.  k is the number of nearest neighbors to use
        to predict the output variable's value for a query point.
        """
        self.k = k
        
    def fit(self, X, y):
        """
        Stores the reference points (X) and their known output values (y).
        """
        self.X = X
        self.y = y
        
    def predict_loop(self, X):
        """
        Predicts the output variable's values for the query points X using loops.
        
        """
        n_samples = X.shape[0]
        pred_y = np.zeros(n_samples, dtype=self.y.dtype)
        n_ref = self.X.shape[0]
        n_dim = X.shape[1]

        for i in range(n_samples):
            # compute distances from X[i] to all reference points using explicit loops
            distances = [0.0] * n_ref
            for j in range(n_ref):
                s = 0.0
                for d in range(n_dim):
                    diff = float(self.X[j, d]) - float(X[i, d])
                    s += diff * diff
                    distances[j] = math.sqrt(s)

            # get the indices of the k nearest neighbors using Python sorting
            idxs = list(range(n_ref))
            sorted_idxs = sorted(idxs, key=lambda idx: distances[idx])
            knn_indices = sorted_idxs[:self.k]

            # count labels of k nearest neighbors using a dict (explicit loop)
            counts = {}
            for idx in knn_indices:
                lbl = self.y[idx]
                counts[lbl] = counts.get(lbl, 0) + 1

            # pick the most common label; break ties by choosing the smallest label (like scipy.stats.mode)
            best_label = None
            best_count = -1
            for lbl, cnt in counts.items():
                if cnt > best_count or (cnt == best_count and (best_label is None or lbl < best_label)):
                    best_label = lbl
                    best_count = cnt

            pred_y[i] = best_label

        return np.asarray(pred_y)
