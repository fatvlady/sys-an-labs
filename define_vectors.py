from copy import deepcopy
from input_data import read_data
import numpy as np
from scipy import special

n = 50
deg = [3,1,2,2]
datas = np.matrix(read_data())

def norm_vector(vec):
    '''
    norm vectors value to value in [0,1]
    :return: float number in [0,1]
    '''

    n,m = vec.shape
    for j in range(m):
        minv = np.min(vec[:,j])
        maxv = np.max(vec[:,j])
        for i in range(n):
            vec[i,j] = (vec[i,j] - minv)/(maxv - minv)
    return vec

data = norm_vector(datas)
degf = [sum(deg[:i+1]) for i in range(len(deg))]

X1 = data[:,:degf[0]]
X2 = data[:,degf[0]:degf[1]]
X3 = data[:, degf[1]:degf[2]]
Y = data[:, degf[2]:degf[3]]

def built_B(Y):
    '''
    built matrix B
    :param Y: Matrix Y consist of output component Y1,Y2,...
    :return: matrix B as ndarray
    '''
    n,m = Y.shape
    b = np.zeros(shape=(n,1), dtype= float)
    for i in range(n):
        b[i,0] = np.max(Y[i]) - np.min(Y[i])
    b_add = deepcopy(b)
    b = np.append(b, b_add, 1)
    return b

B = np.matrix(built_B(Y))

def built_A(X,p =[50,30,40]):
    """
    built matrix A on shifted polynomys Chebysheva
    :param p:mas of deg for vector X1,X2,X3 i.e.
    :param X: it is matrix that has vectors X1 - X3 for example
    :return: matrix A as ndarray
    """

    def cheb_coordinate(v,deg):
        '''
        :param v: vector
        :param deg: chebyshev degree polynom
        :return:column with chebyshev value of coordiate vector
        '''
        n, _ = v.shape
        c = np.ndarray(shape=(n,1), dtype = float)
        for i in range(n):
            c[i,0] = special.eval_sh_chebyt(deg, v[i])
        return c

    def cheb_vector(vec, p):
        '''
        :param vec: it is X that consist of X11, X12, ... vectors
        :param p: max degree for chebyshev polynom
        :return: part of matrix A for vector X1
        '''
        n, m = vec.shape
        a = np.ndarray(shape=(n,0),dtype = float)
        for j in range(m):
            for i in range(p):
                ch = cheb_coordinate(vec[:,j],i)
                a = np.append(a,ch,1)
        return a

    n,_ = X1.shape

    def m(X,p):
        '''
        :param X: [X1, X2, X3]
        :param p: [p1,p2,p3]
        :return: m = m1*p1+m2*p2+...
        '''
        m = len(X)
        for i in range(m):
            m+= X[i].shape[1]*p[i]
        return m

    m = m(X, p)
    A = np.ndarray(shape = (n,0),dtype =float)
    for i in range(len(X)):
        cheb = cheb_vector(X[i],p[i])
        A = np.append(A, cheb,1)
    return A

X = [X1, X2, X3]
p = [50,30,40]
A = np.matrix(built_A(X, p))

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
    while True:
        ai = float(vi.T*ri)/float(vi.T*A*vi) # alpha i
        xi1 = xi+ai*vi # x i+1
        ri1 = ri-ai*A*vi # r i+1
        betai = -float(vi.T*A*ri1)/float(vi.T*A*vi) # beta i
        vi1 = ri1+betai*vi
        if (np.max(ri1)<eps) :
            break
        else:
            xi,vi,ri = xi1,vi1,ri1
    return xi1

lamb = conjugate_gradient_method(A.T*A,A.T*B.T[0].T,0.000001)
print(lamb.shape)

