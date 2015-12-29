import numpy as np
from itertools import product
from multiprocessing import Pool


def determine_deg(a, p1, p2, p3):
    def pool_init(a):
        global obj
        obj = a

    def _brute(args):
        i, j, k = args
        obj.deg = [i + 1, j + 1, k + 1]
        obj.built_A()
        obj.lamb()
        obj.psi()
        obj.built_a()
        obj.built_Fi()
        obj.built_c()
        obj.built_F()
        obj.built_F_()
        return (i, j, k), np.linalg.norm(obj.norm_error, np.inf), obj.norm_error

    a.define_data()
    a.norm_data()
    a.define_norm_vectors()
    a.built_B()
    a.poly_func()
    pool = Pool(4, pool_init, (a))
    d = pool.map(_brute, product([a], p1, p2, p3))
    best = d[0]
    for i in d:
        if i[1] < best[1]:
            best = i
    return best
