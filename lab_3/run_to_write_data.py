from lab_2.solve import *

a= Solve({'samples': 50, 'input_file': 'data_2.txt', 'dimensions': [3, 1, 2, 2], 'output_file': 'protocol_data.xls', 'degrees': [7, 5, 2],\
     'lambda_multiblock': False, 'weights': 'average', 'poly_type': 'chebyshev'})
a.define_data()
a.norm_data()
a.define_norm_vectors()
a.built_B()
a.poly_func()
a.built_A()
a.lamb()
a.psi()
a.built_a()
a.built_Fi()
a.built_c()
a.built_F()
a.built_F_()
a.save_to_file()
# print(np.linalg.norm(a.F - a.Y))
# print(np.linalg.norm(a.Lamb))
# print(a.Fi)



