from Solve import *
from openpyxl import Workbook

a= Solve({'samples': 50, 'input_file': 'data.txt', 'dimentions': [3, 1, 2, 2], 'output_file': '', 'degrees': [7, 5, 2],
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
print(np.linalg.norm(a.F - a.Y))
print(np.linalg.norm(a.Lamb))
print(a.Fi)

wb = Workbook()
#get active worksheet
ws = wb.active

print(a.datas[0,:6].tolist()[0])
ws.append(['Input data: X'])
for i in range(a.n):
     ws.append(a.datas[i,:6].tolist()[0])
ws.append([])
ws.append(['Input data: Y'])
for i in range(a.n):
     ws.append(a.datas[i,6:8].tolist()[0])
ws.append([])

ws.append(['X normalised:'])
for i in range(a.n):
     ws.append(a.data[i,:6].tolist()[0])
ws.append([])

ws.append(['Y noralised:'])
for i in range(a.n):
     ws.append(a.data[i,6:8].tolist()[0])
ws.append([])

ws.append(['matrix B:'])
for i in range(a.n):
     ws.append(a.B[i].tolist()[0])
ws.append([])

ws.append(['matrix A:'])
for i in range(a.A.shape[0]):
     ws.append(a.A[i].tolist()[0])
ws.append([])

ws.append(['matrix Lambda:'])
for i in range(a.Lamb.shape[0]):
     ws.append(a.Lamb[i].tolist()[0])
ws.append([])

for j in range(len(a.Psi)):
     s = 'matrix Psi%i:' %(j+1)
     ws.append([s])
     for i in range(a.n):
          ws.append(a.Psi[j][i].tolist()[0])
     ws.append([])

ws.append(['matrix a:'])
for i in range(a.mX):
     ws.append(a.a[i].tolist()[0])
ws.append([])

for j in range(len(a.Fi)):
     s = 'matrix F%i:' %(j+1)
     ws.append([s])
     for i in range(a.Fi[j].shape[0]):
          ws.append(a.Fi[j][i].tolist()[0])
     ws.append([])

ws.append(['matrix c:'])
for i in range(len(a.X)):
     ws.append(a.c[i].tolist()[0])
ws.append([])

ws.append(['Y rebuilt:'])
for i in range(a.n):
     ws.append(a.F[i].tolist()[0])
ws.append([])

wb.save("protocol.xlsx")

