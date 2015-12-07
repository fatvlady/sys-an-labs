__author__ = 'strike'
from lab_3.solve import *

pt = ['sh_cheb_doubled', 'cheb', 'sh_cheb_2']

a = Solve(
    {'samples': 45, 'input_file': 'data_u.txt', 'dimensions': [2, 2, 3, 4], 'output_file': '', 'degrees': [3, 3, 3],
     'lambda_multiblock': False, 'weights': 'average', 'poly_type': pt[0]})
a.define_data()
a.norm_data()
a.define_norm_vectors()
a.built_B()
a.poly_func()

#i,j,k = 2,15,1
#i,j,k = 6,1,1 # best for data_2.txt

i,j,k = 10,10,8
a.deg = [i+1,j+1,k+1]
a.built_A()
a.lamb()
a.psi()
a.built_a()
a.built_Fi()
a.built_c()
a.built_F()
a.built_F_()
#a.save_to_file()
print(str(i)+' '+str(j)+' '+str(k),a.norm_error,np.linalg.norm(a.norm_error))