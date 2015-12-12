__author__ = 'strike'

from lab_3.solve import *
from copy import deepcopy


def norm_data(x, a):
        """
        x: new values
        a: old values
        norm vectors value to value in [0,1]
        :return: float number in [0,1]
        """
        n, m = x.shape
        vec = np.ndarray(shape=(n, m), dtype=float)
        for j in range(m):
            minv = np.min(a.datas[:, j])
            maxv = np.max(a.datas[:, j])
            for i in range(n):
                vec[i, j] = (a.datas[i, j] - minv) / (maxv - minv)
        return np.matrix(vec)


def define_norm_vectors(data, datas, dim_integral):
    X1 = data[:, :dim_integral[0]]
    X2 = data[:, dim_integral[0]:dim_integral[1]]
    X3 = data[:, dim_integral[1]:dim_integral[2]]
    # matrix of vectors i.e.X = [[X11,X12],[X21],...]
    X = [X1, X2, X3]
    # matrix, that consists of i.e. Y1,Y2
    X_ = [datas[:, :dim_integral[0]], datas[:, dim_integral[0]:dim_integral[1]],
               datas[:, dim_integral[1]:dim_integral[2]]]
    return X,X_


def built_A():



def calc(x, a):
    '''
    :param x: input point
    :param a: solve object
    :return: F_(x)
    '''
    b = deepcopy(a)
    b.datas =np.matrix([x])
    b.n = b.datas.shape[0]
    b.data = norm_data(x, a)
    b.X,b.X_ = define_norm_vectors(b.data, b.datas, b.dim_inegral)

    


    
