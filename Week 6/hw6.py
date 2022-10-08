
# File: hw6.py
# Authors: Xiongyu Chen (xiongyuc), Sidan Chen (sidanc)

import numpy as np
import AVLTree as avl

# test left side inserts
t1 = avl.AVLTree()
for k in range(100, -1, -10):
    t1.insert(k)
    # print('after t1.insert(' + str(k) + ')')
    # t1.print_pretty()

# 1.a
# test whether the tree is an AVL tree
print('t1 is an AVL tree:', t1.is_AVLTree())
t1b = avl.AVLTree()
t1b.insert(10)
t1b.insert(20)
t1b.insert(30)
t1b._top._left._BF = 2  # not an AVL tree!
print('t1b is an AVL tree:', t1b.is_AVLTree())
t1c = avl.AVLTree()
t1c.insert(10)
t1c.insert(20)
t1c.insert(30)
t1c._top._left, t1c._top._right = \
    t1c._top._right, t1c._top._left # not an AVL tree!
print('t1c is an AVL tree:', t1c.is_AVLTree())

# 1.b
# test right side inserts
t2 = avl.AVLTree()
for k in range(0, 101, 10):
    t2.insert(k)
    print('after t2.insert(' + str(k) + ')')
    t2.print_pretty()
print('t2 is an AVL tree:', t2.is_AVLTree())

# 1.c
# test random inserts
t3 = avl.AVLTree()
np.random.seed(0)
for j in range(1,51):
    k = np.random.randint(-100, 100)
    t3.insert(k)
    if j % 10 == 0:
        print('after t3.insert(' + str(k) + ')')
        t3.print_pretty()
print('t3 is an AVL tree:', t3.is_AVLTree())
