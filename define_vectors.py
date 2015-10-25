from copy import deepcopy
from input_data import read_data
import numpy as np
from scipy import special

n = 50
deg = [3, 1, 2, 2]
datas = np.matrix(read_data())
degf = [sum(deg[:i + 1]) for i in range(len(deg))]
Y_ = deepcopy(datas[:, degf[2]:degf[3]])


def norm_vector(vec):
    '''
    norm vectors value to value in [0,1]
    :return: float number in [0,1]
    '''

    n, m = vec.shape
    for j in range(m):
        minv = np.min(vec[:, j])
        maxv = np.max(vec[:, j])
        for i in range(n):
            vec[i, j] = (vec[i, j] - minv) / (maxv - minv)
    return vec


data = norm_vector(datas)

X1 = data[:, :degf[0]]
X2 = data[:, degf[0]:degf[1]]
X3 = data[:, degf[1]:degf[2]]
Y = data[:, degf[2]:degf[3]]


def built_B(Y):
    '''
    built matrix B
    :param Y: Matrix Y consist of output component Y1,Y2,...
    :return: matrix B as ndarray
    '''
    n, m = Y.shape
    b = np.tile((Y.max(axis=1) + Y.min(axis=1))/2,(1,m))
    return np.matrix(b)


'''
define b ####################################################3
'''
B = built_B(Y)  # vector b for only one vector of matrix Y (Y[0])
# for i in range(deg[3] - 1):
#     b_add = deepcopy(b)
#     b = np.append(b, b_add, 1)
# B = np.matrix(b)  # full matrix B for all events


def mA(X, p):
    '''
    :param X: [X1, X2, X3]
    :param p: [p1,p2,p3]
    :return: m = m1*p1+m2*p2+...
    '''
    m = len(X)
    for i in range(m):
        m += X[i].shape[1] * p[i]
    return m


def mX(X, p):
    '''

    :param X:
    :param p:
    :return: number of vectors in X
    '''
    n = 0
    for i in range(len(X)):
        n += X[i].shape[1]
    return n


def built_A(X, p=[50, 30, 40]):
    '''
    built matrix A on shifted polynomys Chebysheva
    :param p:mas of deg for vector X1,X2,X3 i.e.
    :param X: it is matrix that has vectors X1 - X3 for example
    :return: matrix A as ndarray
    '''

    def cheb_coordinate(v, deg):
        '''
        :param v: vector
        :param deg: chebyshev degree polynom
        :return:column with chebyshev value of coordiate vector
        '''
        n, _ = v.shape
        c = np.ndarray(shape=(n, 1), dtype=float)
        for i in range(n):
            c[i, 0] = special.eval_sh_chebyt(deg, v[i])
        return c

    def cheb_vector(vec, p):
        '''
        :param vec: it is X that consist of X11, X12, ... vectors
        :param p: max degree for chebyshev polynom
        :return: part of matrix A for vector X1
        '''
        n, m = vec.shape
        a = np.ndarray(shape=(n, 0), dtype=float)
        for j in range(m):
            for i in range(p):
                ch = cheb_coordinate(vec[:, j], i)
                a = np.append(a, ch, 1)
        return a

    n, _ = X1.shape

    k = mA(X, p)
    A = np.ndarray(shape=(n, 0), dtype=float)
    for i in range(len(X)):
        cheb = cheb_vector(X[i], p[i])
        A = np.append(A, cheb, 1)
    return A


'''
define matrix A ##################################################3
'''
X = [X1, X2, X3]
p = [50, 30, 40]
A = np.matrix(built_A(X, p))


def conjugate_gradient_method(A, b, eps):
    '''
    Conjugate Gradient Method that solve equation Ax = b with given accurancy
    :param A:matrix A
    :param b:vector b
    :param eps: accurancy
    :return: solution x
    '''
    n = len(A.T)  # number column
    xi1 = xi = np.zeros(shape=(n, 1), dtype=float)
    vi = ri = b  # start condition
    while True:
        ai = float(vi.T * ri) / float(vi.T * A * vi)  # alpha i
        xi1 = xi + ai * vi  # x i+1
        ri1 = ri - ai * A * vi  # r i+1
        betai = -float(vi.T * A * ri1) / float(vi.T * A * vi)  # beta i
        vi1 = ri1 + betai * vi
        if (np.linalg.norm(ri1, np.inf) < eps):
            break
        else:
            xi, vi, ri = xi1, vi1, ri1
    return np.matrix(xi1)


'''
define lambda ####################################################3
'''
lamb = np.ndarray(shape=(A.shape[1], 0), dtype=float)
for i in range(deg[3]):
    lamb = np.append(lamb, conjugate_gradient_method(A.T * A, A.T * B[:, i], 0.000001), axis=1)

Lamb = np.matrix(lamb)  # Lamb in full events


def built_psi(A, lamb, X, p=[50, 30, 40]):
    '''
    return matrix xi1 for b1 as matrix
    :param A:
    :param lamb:
    :param p:
    :return:
    '''
    n = A.shape[0]
    m = mX(X, p)
    psi = np.ndarray(shape=(n, m), dtype=float)
    q = 0  # iterator in lamb and A
    l = 0  # iterator in columns psi
    for k in range(len(X)):  # choose X1 or X2 or X3
        for s in range(X[k].shape[1]):  # choose X11 or X12 or X13
            for i in range(X[k].shape[0]):
                psi[i, l] = A[i, q:q + p[k]] * lamb[q:q + p[k], 0]
            q += p[k]
            l += 1
    return np.matrix(psi)


'''
define psi #######################################################3
'''
psi = []  # as list because psi[i] is matrix(not vector)
for i in range(deg[3]):
    psi.append(built_psi(A, Lamb[:, i], X, p))
print(psi[0].shape)
'''
define a #########################################################3
'''
a = np.ndarray(shape=(mX(X, p), 0), dtype=float)
for i in range(deg[3]):
    a = np.append(a, conjugate_gradient_method(psi[i].T * psi[i], psi[i].T * Y[:, i], 0.000001), axis=1)


def built_F1i(psi, a, degf):
    '''

    :param psi: matrix psi (only one
    :param a: vector with shape = (6,1)
    :param degf:  = [3,4,6]//fibonachi of deg
    :return: matrix of (three) components with F1 F2 and F3
    '''
    n = X[0].shape[0]  # n=50
    m = len(X)  # m  = 3
    F1i = np.ndarray(shape=(n, m), dtype=float)
    k = 0  # point of begining columnt to multipy
    for j in range(m):  # 0 - 2
        for i in range(n):  # 0 - 49
            F1i[i, j] = psi[i, k:degf[j]] * a[k:degf[j], 0]
        k = degf[j]
    return np.matrix(F1i)


'''
define Fi #########################################################3
'''
Fi = []
for i in range(deg[3]):
    Fi.append(built_F1i(psi[i], a[:, i], degf))

'''
define c ###########################################################3
'''
c = np.ndarray(shape=(len(X), 0), dtype=float)
for i in range(deg[3]):
    c = np.append(c, conjugate_gradient_method(Fi[i].T * Fi[i], Fi[i].T * Y[:, i], 0.000001), axis=1)

'''
define F ###########################################################3
'''
F = np.ndarray(Y.shape, dtype=float)
for j in range(F.shape[1]):  # 2
    for i in range(F.shape[0]):  # 50
        F[i, j] = Fi[j][i, :] * c[:, j]
F = np.matrix(F)
# '''
# define error ########################################################3
# '''
# error = np.linalg.norm(F - Y)
# print(error)

'''
define F_ ###########################################################3
'''
F_ = np.ndarray(shape=F.shape, dtype=float)
for j in range(F_.shape[1]):
    maxY_ = float(Y_[j].max(axis=1))
    minY_ = float(Y_[j].min(axis=1))
    for i in range(F_.shape[0]):
        F_[i, j] = F[i, j] * (maxY_ - minY_) + minY_
'''
define error ###########################################################3
'''
error = np.std(F_ - Y_, axis=0)
print(error)
print(Y_.mean(axis=0))
