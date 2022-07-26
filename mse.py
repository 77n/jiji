# from sklearn.metrics import mean_squared_error
import numpy as np


def MSE(y_pred, y_true):
    return ((np.array(y_pred) - np.array(y_true))**2).mean()