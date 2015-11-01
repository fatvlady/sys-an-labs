__author__ = 'strike'
import numpy as np

def conjugate_gradient_method(A, b, eps):
    '''
    Conjugate Gradient Method that solve equation Ax = b with given accurancy
    :param A:matrix A
    :param b:vector b
    :param eps: accurancy
    :return: solution x
    '''
    n = len(A.T) # number column
    xi1 = xi = np.zeros(shape=(n,1), dtype = float)
    vi = ri = b # start condition
    i = 0 #loop for number iteration
    N = 1000 #maximum of iteration
    while True:
        try:
            i+= 1
            ai = float(vi.T*ri)/float(vi.T*A*vi) # alpha i
            xi1 = xi+ai*vi # x i+1
            ri1 = ri-ai*A*vi # r i+1
            betai = -float(vi.T*A*ri1)/float(vi.T*A*vi) # beta i
            vi1 = ri1+betai*vi
            if (np.linalg.norm(ri1,np.inf)<eps) :
                break
            else:
                xi,vi,ri = xi1,vi1,ri1
            if i==N:
                raise NameError('Over index: many iterations')
        except NameError:
            print("conjugate_gradient_method is in 100 iteration")
    return np.matrix(xi1)