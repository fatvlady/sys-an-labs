from lab_3.solve import *

def determine_deg(a, p1, p2, p3):
    a.define_data()
    a.norm_data()
    a.define_norm_vectors()
    a.built_B()
    a.poly_func()
    d = list()
    for i in p1:
        for j in p2:
            for k in p3:
                a.deg = [i + 1, j + 1, k + 1]
                a.built_A()
                a.lamb()
                a.psi()
                a.built_a()
                a.built_Fi()
                a.built_c()
                a.built_F()
                a.built_F_()
                # d[str(i)+' '+str(j)+' '+str(k)] = [np.linalg.norm(a.F - a.Y), np.std(a.F_ - a.Y_, axis=0),\
                #                   np.linalg.norm(a.F_ - a.Y_)]
                d.append( ((i,j,k), np.linalg.norm(a.norm_error), a.norm_error) )
    best = d[0]
    for i in d:
        if i[1] < best[1]:
            best = i
    return best
