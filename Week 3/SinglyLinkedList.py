
# File:   SinglyLinkedList.py
# Author: xiongyuc, hoanglov
# Cover:  John K. Ostlund

class SinglyLinkedList:
   class _SLLNode:
      def __init__(self, value, next_node = None):
         self._value = value
         self._next = next_node

   def __init__(self, value=None):
      self._first = None
      if value:
         for i in value:
            self.append(i)
   def __str__(self):
      if self._first == None:
         return ''
      else:
         ret = str(self._first._value)
         _next = self._first._next
         while _next != None:
            ret += ' -> ' + str(_next._value)
            _next = _next._next
         return ret
   def __len__(self):
      if self._first == None:
         return 0
      else:
         length = 1
         _next = self._first
         while True:
            if _next._next != None:
               length += 1
               _next = _next._next
            else:
               break
         return length
   def __eq__(self, other):
      if self._first == None:
         if other._first == None:
            return True
         else:
            return False
      else:
         node_self = self._first
         node_other = other._first
         while True:
            if node_self == None or node_other == None:
               if node_self == node_other:
                  return True
               else:
                  return False
            else:
               if node_self._value == node_other._value:
                  node_self = node_self._next
                  node_other = node_other._next
               else:
                  return False
   def __add__(self, other):
      merge = self.copy()
      for i in other:
         merge.append(i)
      return merge
   def __contains__(self, value):
      if self._first == None:
         return False
      else:
         node = self._first
         while node != None:
            if value == node._value:
               return True
            else:
               node = node._next
         return False
   class _SLLIter:
      def __init__(self, sll):
         self._sll = sll
         self._len = len(sll)
         self._idx = 0
      def __next__(self):
         if self._idx < self._len:
            try:
               ret = self._sll._value
            except AttributeError:
               self._sll = self._sll._first
               ret = self._sll._value
            self._idx += 1
            self._sll = self._sll._next
            return ret
         else:
            raise StopIteration
   def __iter__(self):
      return self._SLLIter(self)

   def insert(self, *value):
      if len(value) == 1:
         self._first = SinglyLinkedList._SLLNode(value[0], self._first)
      else:
         if value[0] == 0:
            self._first = SinglyLinkedList._SLLNode(value[1], self._first)
         else:
            _next = self._first
            for _ in range(value[0] - 1):
               if _next != None:
                  _next = _next._next
               else:
                  break
            _next._next = SinglyLinkedList._SLLNode(value[1], _next._next)
   def append(self, value):
      new_node = SinglyLinkedList._SLLNode(value, None)
      if self._first == None:
         self._first = new_node
      else:
         _next = self._first
         while _next._next != None:
            _next = _next._next
         _next._next = new_node
   def reverse(self):
      if self._first != None:
         node_curr = self._first
         node_prev = None
         node_next = None
         while node_curr != None:
            node_next = node_curr._next
            node_curr._next = node_prev
            node_prev = node_curr
            node_curr = node_next
         self._first = node_prev
   def copy(self):
      if self._first != None:
         node = self._first
         value = [node._value]
         while True:
            if node._next != None:
               node = node._next
               value.append(node._value)
            else:
               break
      if value:
         return SinglyLinkedList(value)
      else:
         return SinglyLinkedList()
   def count(self, value):
      num = 0
      if self._first == None:
         return num
      else:
         node = self._first
         while node != None:
            if value == node._value:
               num += 1
            node = node._next
         return num
   def remove(self, value):
      if self._first != None:
         node = self._first
         if node._value == value:
            self._first = node._next
         else:
            while node._next != None:
               if node._next._value == value:
                  node._next = node._next._next
                  break