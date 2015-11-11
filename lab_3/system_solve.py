__author__ = 'strike'
import numpy as np

def conjugate_gradient_method(A, b, eps):
    '''
    Conjugate Gradient Method that solve equation Ax = b with given accuracy
    :param A:matrix A
    :param b:vector b
    :param eps: accuracy
    :return: solution x
    '''
    n = len(A.T) # number column
    xi1 = xi = np.zeros(shape=(n,1), dtype=float)
    vi = ri = b # start condition
    i = 0 #loop for number iteration
    N = 10000 #maximum of iteration
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
            print("conjugate_gradient_method is in 1000 iteration")
    return np.matrix(xi1)

def conjugate_gradient_method_v2(A, b, eps):
    '''
    Conjugate Gradient Method that solve equation Ax = b with given accuracy
    :param A:matrix A
    :param b:vector b
    :param eps: accuracy
    :return: solution x
    '''
    n = len(A.T) # number column
    xi1 = xi = np.zeros(shape=(n,1), dtype=float)
    vi = ri = b # start condition
    i = 0 #loop for number iteration\
    while True:
        i+= 1
        ai = float(vi.T*ri)/float(vi.T*A*vi) # alpha i
        xi1 = xi+ai*vi # x i+1
        ri1 = ri-ai*A*vi # r i+1
        betai = -float(vi.T*A*ri1)/float(vi.T*A*vi) # beta i
        vi1 = ri1+betai*vi
        if (np.linalg.norm(ri1,np.inf)<eps) or i > 3 * n:
            break
        else:
            xi,vi,ri = xi1,vi1,ri1
    return np.matrix(xi1)

def conjugate_gradient_method_v3(A, b, eps):
    '''
    Conjugate Gradient Method that solve equation Ax = b with given accuracy
    :param A:matrix A
    :param b:vector b
    :param eps: accuracy
    :return: solution x
    '''
    x = np.zeros((A.shape[0],1))
    p = rnext = rcur = b - A * x
    while np.linalg.norm(rcur) > eps:
        rcur = rnext
        alpha = np.linalg.norm(rcur)**2 / float(p.T * A * p)
        x = x + alpha * p
        rnext = rcur - alpha * (A * p)
        if np.linalg.norm(rnext) > eps:
            beta = np.linalg.norm(rnext)**2 / np.linalg.norm(rcur)**2
            p = rnext + beta * p
    return np.matrix(x)