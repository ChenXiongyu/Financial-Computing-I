
# File:    hw3_1.py
# Authors: xiongyuc, hoanglov

import SinglyLinkedList as SLL

# 3_1.a
print('\n3_1.a:')
slla = SLL.SinglyLinkedList();
print('initial slla:', slla)

slla.append(5)
slla.insert('hi')
slla.append(True)
slla.insert(4.5)
print('modified slla:', slla)  # 4.5 -> hi -> 5 -> True


# 3_1.b
print('\n3_1.b:')
slla.insert(0, 'Ed')
slla.insert(3, 7)
print('after modified insert:\n\t',
          slla)    # Ed -> 4.5 -> hi -> 7 -> 5 -> True


# 3_1.c
print('\n3_1.c:')
sllb = SLL.SinglyLinkedList([3, 2, 9, 8, 1])
print('initial sllb:', sllb)  # 3 -> 2 -> 9 -> 8 -> 1
sllc = SLL.SinglyLinkedList('howdy')
print('initial sllc:', sllc)  # 'h' -> 'o' -> 'w' -> 'd' -> 'y'


# 3_1.d
print('\n3_1.d:')
slld = SLL.SinglyLinkedList()
print('len(slla):', len(slla))    # 6
print('len(sllb):', len(sllb))    # 5
print('len(sllc):', len(sllc))    # 5
print('len(slld):', len(slld))    # 0


# 3_1.e
print('\n3_1.e:')
slla.reverse()
sllc.reverse()
slld.reverse()
print('slla reversed:', slla)    # True -> 5 -> 7 -> hi -> 4.5 -> Ed
print('sllc reversed:', sllc)    # 'y' -> 'd' -> 'w' -> 'o' -> 'h'
print('slld reversed:', slld)    # (still empty)


# 3_1.f
print('\n3_1.f:')
slle = sllb.copy()
print('initial sllb:', sllb)  # 3 -> 2 -> 9 -> 8 -> 1
print('initial slle:', slle)  # 3 -> 2 -> 9 -> 8 -> 1


# 3_1.g
print('\n3_1.g:')
print('sllb == slle?', sllb == slle)   # True
print('sllb == slla?', sllb == slla)   # False
print('sllb != slle?', sllb != slle)   # False 
print('sllb != slla?', sllb != slla)   # True
sllb2 = sllb  # reference to the same object
print('sllb == sllb2?', sllb == sllb2) # True
print('sllb is sllb2?', sllb is sllb2) # True
print('sllb is slle?', sllb is slle)   # False


# 3_1.h
print('\n3_1.h:')
print('slla:', slla)
print('displaying slla using a for loop:')
for x in slla:
    print(x)
print('sllc:', sllc)
print('creating a set from sllc:')
s1 = set(sllc)
print('s1:', s1)


# 3_1.i
print('\n3_1.i:')
print('sllc:', sllc)
sllg = slla + sllc
print('sllg:', sllg)    # True -> 5 -> 7 -> hi -> 4.5 -> Ed -> y -> d -> w -> o -> h


# 3_1.j
print('\n3_1.j:')
print("'w' in sllc:", ('w' in sllc))  # True
print("'z' in sllc:", ('z' in sllc))  # False


# 3_1.k
print('\n3_1.k:')
sllb.append(3)
print('sllb:', sllb)
print('sllb.count(3):', sllb.count(3))  # 2
sllb.remove(3)
print('after remove(3), sllb.count(3):', sllb.count(3))  # 1
