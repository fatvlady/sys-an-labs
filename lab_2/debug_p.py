__author__ = 'strike'
from lab_2.solve import *

a= Solve({'samples': 50, 'input_file': 'data_2.txt', 'dimensions': [3, 1, 2, 2], 'output_file': 'data2_611_average.xlsx', 'degrees': [3, 3, 3],
     'lambda_multiblock': False, 'weights': 'average', 'poly_type': 'chebyshev'})
a.define_data()
a.norm_data()
a.define_norm_vectors()
a.built_B()
a.poly_func()

i,j,k = 6,1,1
a.p = [i+1,j+1,k+1]
a.built_A()
a.lamb()
a.psi()
a.built_a()
a.built_Fi()
a.built_c()
a.built_F()
a.built_F_()
#a.save_to_file()
print(str(i)+' '+str(j)+' '+str(k),a.norm_error)