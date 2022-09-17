
# File:   SinglyLinkedList.py
# Author: John K. Ostlund

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
         node = self._first
         value = [node._value]
         while True:
            if node._next != None:
               node = node._next
               value.append(node._value)
            else:
               break
         value.reverse()
         node = self._first
         for i in value:
            node._value = i
            node = node._next
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