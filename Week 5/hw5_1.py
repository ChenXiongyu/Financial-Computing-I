
# File:    hw5_1.py
# Authors:

import numpy as np

# Your code here

def MatrixChainMult(A_chain):
    return 600, 'A1 (A2 A3)'   # DUMMY, FOR TESTING

# Test cases

print('\n5_1.a:')   # 3 matrices
A_chain_1 = [ np.ones((20,4)), np.ones((4,10)),
              np.ones((10,5)) ]

nops, order = MatrixChainMult(A_chain_1)

print(len(A_chain_1), 'matrices')  
print('Matrix dimensions are:')
for m in range(len(A_chain_1)):
    print('A' + str(m+1) + ':', A_chain_1[m].shape)
                               # A1: (20, 4)
                               # A2: (4, 10)
                               # A3: (10, 5)
  
print('Chain requires', nops, 'operations.')  # 600

print('Ordering is:')
print(order)                   # A1 (A2 A3)


print('\n5_1.b:')   # 6 matrices
A_chain_2 = [ np.ones((10,4)), np.ones((4,20)),
              np.ones((20,8)), np.ones((8,5)),
              np.ones((5,12)), np.ones((12,3))]

nops, order = MatrixChainMult(A_chain_2)
  
print(len(A_chain_2), 'matrices')  
print('Matrix dimensions are:')
for m in range(len(A_chain_2)):
    print('A' + str(m+1) + ':', A_chain_2[m].shape)
  
print('Chain requires', nops, 'operations.')

print('Ordering is:')
print(order)


print('\n5_1.c:')   # 12 matrices
dims = [12, 4, 20, 30, 8, 3, 5, 25, 12, 8, 20, 4, 15]
A_chain_3 = [ np.ones((dims[i],dims[i+1])) for i in range(len(dims)-1) ]

nops, order = MatrixChainMult(A_chain_3)
  
print(len(A_chain_3), 'matrices')  
print('Matrix dimensions are:')
for m in range(len(A_chain_3)):
    print('A' + str(m+1) + ':', A_chain_3[m].shape)
  
print('Chain requires', nops, 'operations.')

print('Ordering is:')
print(order)


print('\n5_1.d:')   # 40 matrices
np.random.seed(4)
dims = [np.random.randint(3, 40) for i in range(41)]
A_chain_4 = [ np.ones((dims[i],dims[i+1])) for i in range(len(dims)-1) ]

nops, order = MatrixChainMult(A_chain_4)
  
print(len(A_chain_4), 'matrices')  
print('Matrix dimensions are:')
for m in range(len(A_chain_4)):
    print('A' + str(m+1) + ':', A_chain_4[m].shape)
  
print('Chain requires', nops, 'operations.')

print('Ordering is:')
print(order)

