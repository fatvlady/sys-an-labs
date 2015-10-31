__author__ = 'strike'
from copy import deepcopy
import numpy as np
from scipy import special

class Solve(object):
    '''
    {'samples': 50, 'input_file': '', 'dimentions': array([3, 1, 2, 2]), 'output_file': '', 'degrees': array([3, 3, 3]),
     'lambda_multiblock': False, 'weights': 'average', 'poly_type': 'chebyshev'}
    '''
    def __init__(self,d):
        self.n = d['samples']
        self.deg = d['dimentions']
        self.filename_input = d['input_file']
        self.dict = d['output_file']
        self.p = list(map(lambda x:x+1,d['degrees'])) # on 1 more because include 0
        self.weights = d['weights']
        self.poly_type = d['poly_type']

    def define_data(self):
        f = open(self.filename_input, 'r')
        # all data from file_input in float
        self.datas = np.matrix([list(map(lambda x:float(x),f.readline().split())) for i in range(self.n)])
        # list of sum degrees [ 3,1,2] -> [3,4,6]
        self.degf = [sum(self.deg[:i + 1]) for i in range(len(self.deg))]

    def norm_data(self):
        '''
        norm vectors value to value in [0,1]
        :return: float number in [0,1]
        '''
        n,m = self.datas.shape
        vec = np.ndarray(shape=(n,m),dtype=float)
        for j in range(m):
            minv = np.min(self.datas[:,j])
            maxv = np.max(self.datas[:,j])
            for i in range(n):
                vec[i,j] = (self.datas[i,j] - minv)/(maxv - minv)
        self.data = np.matrix(vec)

    def define_norm_vectors(self):
        '''
        buile matrix X and Y
        :return:
        '''
        X1 = self.data[:,:self.degf[0]]
        X2 = self.data[:,self.degf[0]:self.degf[1]]
        X3 = self.data[:, self.degf[1]:self.degf[2]]
        #matrix of vectors i.e.X = [[X11,X12],[X21],...]
        self.X = [X1, X2, X3]
        #number columns in matrix X
        self.mX = self.degf[2]
        # matrix, that consists of i.e. Y1,Y2
        self.Y = self.data[:, self.degf[2]:self.degf[3]]

    def built_B(self):
        def B_average(self):
            '''
            Vector B as avarage of max and min in Y. B[i] =max Y[i,:]
            :return:
            '''
            b = np.tile((self.Y.max(axis=1) + self.Y.min(axis=1))/2,(1,self.deg[3]))
            return b

        def B_scaled(self):
            '''
            Vector B  = Y
            :return:
            '''
            return deepcopy(self.Y)

        if self.weights == 'average':
            self.B = B_average()
        elif self.weights =='scaled':
            self.B = B_scaled()
        else:
            exit('B not definded')

    def poly_func(self):
        '''
        Define function to polynoms
        :return: function
        '''
        if self.poly_type =='chebyshev':
            self.poly_f = special.eval_sh_chebyt()
        elif self.poly_type == 'legendre':
            self.poly_f = special.eval_sh_legendre()
        elif self.poly_type == 'lagger':
            self.poly_f = special.eval_laguerre()
        elif self.poly_type == 'hermit':
            self.poly_f = special.eval_hermite()

    def built_A(self):
        '''
        built matrix A on shifted polynomys Chebysheva
        :param self.p:mas of deg for vector X1,X2,X3 i.e.
        :param self.X: it is matrix that has vectors X1 - X3 for example
        :return: matrix A as ndarray
        '''

        def mA():
            '''
            :param X: [X1, X2, X3]
            :param p: [p1,p2,p3]
            :return: m = m1*p1+m2*p2+...
            '''
            m = 0
            for i in range(len(self.X)):
                m+= self.X[i].shape[1]*(self.p[i]+1)
            return m


        def coordinate(v,deg):
            '''
            :param v: vector
            :param deg: chebyshev degree polynom
            :return:column with chebyshev value of coordiate vector
            '''
            c = np.ndarray(shape=(self.n,1), dtype = float)
            for i in range(self.n):
                c[i,0] = self.poly_f(deg, v[i])
            return c

        def vector(vec, p):
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

        #k = mA()
        A = np.ndarray(shape = (self.n,0),dtype =float)
        for i in range(len(self.X)):
            vec = vector(self.X[i],self.p[i])
            A = np.append(A, vec,1)
        return A



a= Solve({'samples': 50, 'input_file': 'data.txt', 'dimentions': [3, 1, 2, 2], 'output_file': '', 'degrees': [3, 3, 3],
     'lambda_multiblock': False, 'weights': 'average', 'poly_type': 'chebyshev'})
a.define_data()
a.norm_data()
a.define_norm_vectors()
a.built_B(
a.poly_func()


print(a.B_average())



