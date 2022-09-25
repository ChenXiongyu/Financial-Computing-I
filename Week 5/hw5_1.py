
# File:    hw5_1.py
# Authors: xiongyuc

import numpy as np


def _multiplication(order, left, right):
    if len(order) == 1:
        return 'A%d A%d' % (left, right)
    num = int(order[-1]) + 1
    if num < left or num >= right:
        return _multiplication(order[:-1], left, right)
    elif num == left:
        eq = ('A%d (' % left) + \
            _multiplication(order[:-1], left + 1, right) + ')'
    elif num + 1 == right:
        eq = '(' + _multiplication(order[:-1], left, right - 1) + \
            (') A%d' % right)
    else:
        eq = '(' + _multiplication(order[:-1], left, num) + ')' + \
            '(' + _multiplication(order[:-1], num + 1, right) + ')'
    return eq


def MatrixChainMult(A_chain):
    num = len(A_chain)
    C = np.zeros((num, num), dtype=int)
    Order = [[[] for _ in range(num)] for _ in range(num)]
    for j in range(1, num):
        for i in range(num - j):
            C_ij = []
            for k in range(i, i + j):
                comp = A_chain[i].shape[0] * A_chain[k].shape[1] * A_chain[i + j].shape[1]
                C_ij.append(C[i, k] + comp + C[k + 1, i + j])
            C[i, i + j], pos = min(C_ij), np.argmin(C_ij) + i
            Order[i][i + j].extend(Order[i][pos] + Order[pos + 1][i + j] + [pos])
    return C[0, num - 1], _multiplication(Order[0][num - 1], 1, num)


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
  
print('Chain requires', nops, 'operations.')  # 1140

print('Ordering is:')
print(order)                   # A1 (A2 (A3 (A4 (A5 A6))))


print('\n5_1.c:')   # 12 matrices
dims = [12, 4, 20, 30, 8, 3, 5, 25, 12, 8, 20, 4, 15]
A_chain_3 = [ np.ones((dims[i],dims[i+1])) for i in range(len(dims)-1) ]

nops, order = MatrixChainMult(A_chain_3)
  
print(len(A_chain_3), 'matrices')  
print('Matrix dimensions are:')
for m in range(len(A_chain_3)):
    print('A' + str(m+1) + ':', A_chain_3[m].shape)
  
print('Chain requires', nops, 'operations.')  # 5907

print('Ordering is:')
print(order)                   # (A1 (A2 (A3 (A4 A5))))((((((A6 (A7 A7)) A8) A9) A10) A11) A12)


print('\n5_1.d:')   # 40 matrices
np.random.seed(4)
dims = [np.random.randint(3, 40) for i in range(41)]
A_chain_4 = [ np.ones((dims[i],dims[i+1])) for i in range(len(dims)-1) ]

nops, order = MatrixChainMult(A_chain_4)
  
print(len(A_chain_4), 'matrices')  
print('Matrix dimensions are:')
for m in range(len(A_chain_4)):
    print('A' + str(m+1) + ':', A_chain_4[m].shape)
  
print('Chain requires', nops, 'operations.')  # 51180

print('Ordering is:')
print(order)

