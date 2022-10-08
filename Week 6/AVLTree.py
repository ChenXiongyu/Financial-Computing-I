
# File: AVLTree.py
# Starting file for FC I Homework 6
# Authors: Xiongyu Chen (xiongyuc), Sidan Chen (sidanc)

class AVLTree:
   class _AVLnode:
      def __init__(self, value, left = None,
                                right = None):
         self._value = value
         self._left = left
         self._right = right
         self._BF = 0  # a new node has _BF == 0

   def __init__(self):
      self._top = None

   def insert(self, v):
      if self._top == None:
         self._top = AVLTree._AVLnode(v)
      else:
         self._insert_help([self._top], v)  # list of parents and value
         
   def _insert_help(self, pars, v):
      if v < pars[0]._value:
         if pars[0]._left == None:
            pars[0]._left = AVLTree._AVLnode(v)
            self._update([pars[0]._left] + pars)
         else:
            self._insert_help([pars[0]._left] + pars, v)
      elif v > pars[0]._value:
         if pars[0]._right == None:
            pars[0]._right = AVLTree._AVLnode(v)
            self._update([pars[0]._right] + pars)
         else:
            self._insert_help([pars[0]._right] + pars, v)

   def is_AVLTree(self):
      if self._top == None:
         return True
      else:
         return self._is_AVLTree_help(self._top)
   
   def _is_AVLTree_help(self, node):
      if abs(node._BF) > 1:
         return False
      else:
         if node._left != None:
            if node._left._value >= node._value:
               return False
            else:
               is_left = self._is_AVLTree_help(node._left)
         else:
            is_left = True
         if node._right != None:
            if node._right._value <= node._value:
               return False
            else:
               is_right = self._is_AVLTree_help(node._right)
         else:
            is_right = True
         if is_left and is_right:
            return True
         else:
            return False
         
   def _update(self, pars): # N: new node, P: N's parent,
                            # G: grandparent of N
      p = 0  # work upward through ancestors
      while p < len(pars) - 1:
         N = pars[p]
         P = pars[p+1]
         if N == P._left:   # left child
            P._BF += 1
            if P._BF > 1:   # P is left heavy: rotate
               if N._BF < 0:  # N right heavy: LR
                  self._LR_rotate(p-1, pars)
               else:          # N not right heavy: R 
                  self._R_rotate(p-1, pars)
         else:              # right child
            P._BF -= 1
            if P._BF < -1:  # P is right heavy: rotate
               if N._BF > 0:  # N left heavy: RL
                  self._RL_rotate(p-1, pars)
               else:          # N not left heavy: L 
                  self._L_rotate(p-1, pars)
         if P._BF == 0:
             break  # no need to go higher
         p += 1

   def _R_rotate(self, p, pars): # N: node, P: parent
                                 # G: grandparent
      if p < len(pars) - 2:  # grandparent exists
         N = pars[p]
         P = pars[p+1]
         G = pars[p+2]
         if N != P._left or P != G._left:
            return   # called for wrong case
         if G == self._top:
            self._top = P
            G._left = P._right
            P._right = G
         else:  # handle case where G != self._top
            GG = pars[p+3]  # great grandparent
            if G == GG._left:
                GG._left = P
            else:
                GG._right = P
            G._left = P._right
            P._right = G
         P._BF -= 1
         G._BF -= 2
         pars.pop(p+1)   # P is now parent of G

   def _L_rotate(self, p, pars): # N: node, P: parent
                                 # G: grandparent
      if p < len(pars) - 2:  # grandparent exists
         N = pars[p]
         P = pars[p+1]
         G = pars[p+2]
         if N != P._right or P != G._right:
            return   # called for wrong case
         if G == self._top:
            self._top = P
            G._right = P._left
            P._left = G
         else:  # handle case where G != self._top
            GG = pars[p+3]  # great grandparent
            if G == GG._right:
                GG._right = P
            else:
                GG._left = P
            G._right = P._left
            P._left = G
         P._BF += 1
         G._BF += 2
         pars.pop(p+1)   # P is now parent of G

   def _LR_rotate(self, p, pars): # N: node, P: parent
                                 # G: grandparent
      if p < len(pars) - 2:  # grandparent exists
         N = pars[p]
         P = pars[p+1]
         G = pars[p+2]
         if N != P._right or P != G._left:
            return   # called for wrong case
         
         P._right = N._left
         P._BF += 1
         N._left = P
         N._BF += 1
         G._left = N
         N, P = P, N
         pars[p], pars[p+1], pars[p+2] = N, P, G
         
         if G == self._top:
            self._top = P
            G._left = P._right
            P._right = G
         else:  # handle case where G != self._top
            GG = pars[p+3]  # great grandparent
            if G == GG._left:
                GG._left = P
            else:
                GG._right = P
            G._left = P._right
            P._right = G
         P._BF -= 1
         G._BF -= 2
         pars.pop(p+1)   # P is now parent of G

   def _RL_rotate(self, p, pars): # N: node, P: parent
                                 # G: grandparent
      if p < len(pars) - 2:  # grandparent exists
         N = pars[p]
         P = pars[p+1]
         G = pars[p+2]
         if N != P._left or P != G._right:
            return   # called for wrong case
         
         P._left = N._right
         P._BF -= 1
         N._right = P
         N._BF -= 1
         G._right = N
         N, P = P, N
         pars[p], pars[p+1], pars[p+2] = N, P, G

         if G == self._top:
            self._top = P
            G._right = P._left
            P._left = G
         else:  # handle case where G != self._top
            GG = pars[p+3]  # great grandparent
            if G == GG._right:
                GG._right = P
            else:
                GG._left = P
            G._right = P._left
            P._left = G
         P._BF += 1
         G._BF += 2
         pars.pop(p+1)   # P is now parent of G
   
   def print_pretty(self):
      self._print_pretty_levels(self._top, 0)

   def _print_pretty_levels(self, cur, level):
      if cur != None:
         self._print_pretty_levels(cur._right, level + 1)
         print(' ' * 4 * level + str(cur._value) + ' (' + str(cur._BF) + ')')
         self._print_pretty_levels(cur._left, level + 1)


if __name__ == '__main__':

   t1 = AVLTree()
   for k in range(200, -1, -10):
       t1.insert(k)
       print('after t1.insert(' + str(k) + ')')
       t1.print_pretty()
       
