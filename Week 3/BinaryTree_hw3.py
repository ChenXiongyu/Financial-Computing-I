
# File: BinaryTree_hw3.py
# Author(s):

class BinaryTree:
    class _BTNode:
        def __init__(self, value, left = None, right = None):
            self._value = value
            self._left = left
            self._right = right
    def __init__(self):
        self._top = None
    def insert(self, value):
        if self._top == None:
            self._top = BinaryTree._BTNode(value)
        else:
            self._insert_help(self._top, value)
    def _insert_help(self, cur_node, value):
        if value < cur_node._value:
            if cur_node._left == None:
                cur_node._left = BinaryTree._BTNode(value)
            else:
                self._insert_help(cur_node._left, value)
        elif value > cur_node._value:
            if cur_node._right == None:
                cur_node._right = BinaryTree._BTNode(value)
            else:
                self._insert_help(cur_node._right, value)
    def __str__(self):
        return self._str_help(self._top)
    def _str_help(self, cur_node):
        if cur_node == None:
            return '';
        else:
            left_str = self._str_help(cur_node._left)
            right_str = self._str_help(cur_node._right)
            ret = str(cur_node._value)
            if left_str:
                ret = left_str + ' ' + ret
            if right_str:
                ret = ret + ' ' + right_str
            return ret
    def sum(self):
        return self._sum_help(self._top)
    def _sum_help(self, cur_node):
        if cur_node == None:
            return 0;
        else:
            return (self._sum_help(cur_node._left)
                    + cur_node._value
                    + self._sum_help(cur_node._right))
    def size(self):
        return self._size_help(self._top)
    def _size_help(self, cur_node):
        if cur_node == None:
            return 0;
        else:
            return (self._size_help(cur_node._left)
                    + 1
                    + self._size_help(cur_node._right))
    def print_pretty(self):
        return self._print_pretty_help(self._top, 0)
    def _print_pretty_help(self, cur_node, indent_level):
        if cur_node == None:
            return
        else:
            self._print_pretty_help(cur_node._right, indent_level + 1)
            print(' ' * indent_level * 8, cur_node._value)
            self._print_pretty_help(cur_node._left, indent_level + 1)
    def depth(self):
        return self._depth_help(self._top)
    def _depth_help(self, cur_node):
        if cur_node == None:
            return 0;
        else:
            left_d = self._depth_help(cur_node._left)
            right_d = self._depth_help(cur_node._right)
            return 1 + (left_d if left_d > right_d else right_d)
    def __eq__(self, other):
        return str(self) == str(other)
    def min(self):
        if self._top == None:
            return None
        else:
            # the minimum is the left-most value
            cur_node = self._top
            while cur_node._left != None:
                cur_node = cur_node._left
            return cur_node._value
    def max(self):
        if self._top == None:
            return None
        else:
            # the maximum is the right-most value
            cur_node = self._top
            while cur_node._right != None:
                cur_node = cur_node._right
            return cur_node._value
    def mean(self):
        if self._top == None:
            return None
        else:
            return self.sum() / self.size()
    def __contains__(self, value):
        if self._top == None:
            return False
        else:
            return self._contains_help(self._top, value)
    def _contains_help(self, cur_node, value):
        if cur_node == None:
            return False
        elif cur_node._value == value:
            return True
        elif cur_node._value < value:
            return self._contains_help(cur_node._right, value)
        else:    # cur_node._value > value
            return self._contains_help(cur_node._left, value)
    def copy(self):
        bt_new = BinaryTree()
        bt_new._top = self._copy_help(self._top)
        return bt_new
    def _copy_help(self, cur_node):
        if cur_node == None:
            return None
        else:
            return BinaryTree._BTNode(cur_node._value,
                                      self._copy_help(cur_node._left),
                                      self._copy_help(cur_node._right))
    def negate(self):
        if self._top != None:
            self._negate_help(self._top)
    def _negate_help(self, cur_node):
        if cur_node == None:
            return
        else:
            cur_node._value *= -1
            self._negate_help(cur_node._left)
            self._negate_help(cur_node._right)
            cur_node._left, cur_node._right = cur_node._right, cur_node._left

