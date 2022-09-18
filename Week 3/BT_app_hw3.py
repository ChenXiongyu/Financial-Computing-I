
# File BT_app_hw3.py
# Author(s): xiongyuc, hoanglov

import BinaryTree_hw3 as bt

# 1.a
bt1 = bt.BinaryTree()     # an empty BinaryTree
bt1.insert(12)
bt1.insert(7)
bt1.insert(22)
bt1.insert(-4)
bt1.insert(3)
bt1.insert(6)
bt1.insert(15)
bt1.insert(18)

bt2 = bt.BinaryTree()     # an empty tree

print('bt1:', bt1)        # bt1: -4 3 6 7 12 15 18 22
print('bt2:', bt2)        # bt2:

print('bt1.sum():', bt1.sum())   # bt1.sum(): 79

print('bt1.size():', bt1.size())    # should display 8
print('bt2.size():', bt2.size())    # should display 0

print('\nbt1.print_pretty():')
bt1.print_pretty()      # should display:
            #         22
            #                         18
            #                 15
            # 12
            #         7
            #                                 6
            #                         3
            #                 -4
print('\nbt2.print_pretty():')
bt2.print_pretty()      # should display no output

print('bt1.depth():', bt1.depth())    # should display 5
print('bt2.depth():', bt2.depth())    # should display 0


# 1.b
bt1.delete(6)
print('\nafter bt1.delete(6): bt1.print_pretty():')
bt1.print_pretty()      # should display:
            #         22
            #                         18
            #                 15
            # 12
            #         7
            #                         3
            #                 -4
bt1.delete(15)
print('\nafter bt1.delete(15): bt1.print_pretty():')
bt1.print_pretty()      # should display:
            #         22
            #                 18
            # 12
            #         7
            #                         3
            #                 -4
bt1.delete(8)           # there is no 8: nothing should happen
print('\nafter bt1.delete(8): bt1.print_pretty():')
bt1.print_pretty()      # should display:
            #         22
            #                 18
            # 12
            #         7
            #                         3
            #                 -4
bt1.delete(12)
print('\nafter bt1.delete(12): bt1.print_pretty():')
bt1.print_pretty()      # should display:
            #         22
            #                 18
            # 7
            #                 3
            #         -4


# 1.c
bt3 = bt.BinaryTree()
bt3.insert(8)
bt3.insert(14)
bt3.insert(12)
bt3.insert(19)
bt3.insert(15)
print('\nbt3.print_pretty():')
bt3.print_pretty()      # should display:
            #                 19
            #                         15
            #         14
            #                 12
            # 8

print('\nbt1.is_balanced():', bt1.is_balanced())  # True
print('\nbt2.is_balanced():', bt2.is_balanced())  # True
print('\nbt3.is_balanced():', bt3.is_balanced())  # False


# 1.d
print('\nbt1.print_pretty():')
bt1.print_pretty()      # should display:
            #         22
            #                 18
            # 7
            #                 3
            #         -4
bt1.rotate_left(-4)
print('\nafter bt1.rotate_left(-4): bt1.print_pretty():')
bt1.print_pretty()
      # should display:
            #         22
            #                 18
            # 7
            #         3
            #                 -4
bt1.rotate_left(7)
print('\nafter bt1.rotate_left(7): bt1.print_pretty():')
bt1.print_pretty()
      # should display:
            # 22
            #                 18
            #         7
            #                 3
            #                         -4
bt1.rotate_left(2)    # nothing happens
print('\nafter bt1.rotate_left(2): bt1.print_pretty():')
bt1.print_pretty()
      # should display:
            # 22
            #                 18
            #         7
            #                 3
            #                         -4
print('\nbt1.is_balanced():', bt1.is_balanced())  # False


# 1.e

print('\nbt1.print_pretty():')
bt1.print_pretty()
      # should display:
            # 22
            #                 18
            #         7
            #                 3
            #                         -4
bt1.rotate_right(2)    # nothing happens
print('\nafter bt1.rotate_right(2): bt1.print_pretty():')
bt1.print_pretty()
      # should display:
            # 22
            #                 18
            #         7
            #                 3
            #                         -4
bt1.rotate_right(22)
print('\nafter bt1.rotate_right(22): bt1.print_pretty():')
bt1.print_pretty()
      # should display:
            #         22
            #                 18
            # 7
            #         3
            #                 -4
bt1.rotate_right(3)
print('\nafter bt1.rotate_right(3): bt1.print_pretty():')
bt1.print_pretty()
      # should display:
            #         22
            #                 18
            # 7
            #                 3
            #         -4
print('\nbt1.is_balanced():', bt1.is_balanced())  # True


# 1.f
print('\nbt3.print_pretty():')
bt3.print_pretty()      # should display:
            #                 19
            #                         15
            #         14
            #                 12
            # 8
print('\nbt3.is_balanced():', bt3.is_balanced())  # False
bt3.Day_balance()
print('\nafter bt3.Day_balance(): bt3.print_pretty():')
bt3.print_pretty()
print('\nbt3.is_balanced():', bt3.is_balanced())  # True

bt4 = bt.BinaryTree()
for j in range(20):
    bt4.insert(j)
print('\nbt4.print_pretty():')
bt4.print_pretty()
print('\nbt4.is_balanced():', bt4.is_balanced())  # False
bt4.Day_balance()
print('\nafter bt4.Day_balance(): bt4.print_pretty():')
bt4.print_pretty()
print('\nbt4.is_balanced():', bt4.is_balanced())  # True
