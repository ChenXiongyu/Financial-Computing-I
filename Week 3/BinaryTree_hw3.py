
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

    def delete(self, value):
        if self._top != None:
            if self._top._value == value:
                left = self._top._left
                right = self._top._right
                node = left
                while node._right != None:
                    node = node._right
                node._right = right
                self._top = left
            else:
                self._delete_help(self._top, value)
    def _delete_help(self, parent, value):
    
        def _right_to_left(left_node, right_node):
            node = left_node
            try:
                while node._right != None:
                    node = node._right
                node._right = right_node
            except AttributeError:
                left_node = right_node
            return left_node
                    
        if value > parent._value:
            if parent._right != None:
                if value == parent._right._value:
                    left = parent._right._left
                    right = parent._right._right
                    parent._right = _right_to_left(left, right)
                else:
                    self._delete_help(parent._right, value)
        else:
            if parent._left != None:
                if value == parent._left._value:
                    left = parent._left._left
                    right = parent._left._right
                    parent._left = _right_to_left(left, right)
                else:
                    self._delete_help(parent._left, value)
    
    def is_balanced(self):
        if self._top == None:
            return True
        else:
            node_list = [self._top]
            node_tbs = []
            while len(node_list) > 0:
                for node in node_list:
                    depth_right = self._depth_help(node._right)
                    depth_left = self._depth_help(node._left)
                    if abs(depth_left - depth_right) > 1:
                        return False
                    else:
                        if depth_left:
                            node_tbs.append(node._left)
                        if depth_right:
                            node_tbs.append(node._right)
                node_list = node_tbs
                node_tbs = []
            return True

    def _rotate_help(self, value, rotate_function):
        if self._top != None:
            if self._top._value == value:
                self._top = rotate_function(self._top)
            else:
                parent_node = self._top
                while parent_node._left != None or parent_node._right != None:
                    if value > parent_node._value:
                        if parent_node._right != None:
                            if value == parent_node._right._value:
                                parent_node._right = \
                                    rotate_function(parent_node._right)
                                break
                            parent_node = parent_node._right
                    else:
                        if parent_node._left != None:
                            if value == parent_node._left._value:
                                parent_node._left = \
                                    rotate_function(parent_node._left)
                                break
                            parent_node = parent_node._left

    def rotate_left(self, value):
        def rotate_left_help(cur_node):
            P = cur_node
            Q = cur_node._right
            try:
                B = Q._left
            except AttributeError:
                B = None
            P._right = B
            Q._left = P
            return Q
        self._rotate_help(value, rotate_left_help)
    
    def rotate_right(self, value):
        def rotate_right_help(cur_node):
            Q = cur_node
            P = cur_node._left
            try:
                B = P._right
            except AttributeError:
                B = None
            Q._left = B
            P._right = Q
            return P
        self._rotate_help(value, rotate_right_help)

    def Day_balance(self):
        if self._top != None:
            while True:
                depth = self.depth()
                node = self._top
                for i in range(depth - 1):
                    if node._left != None:
                        self.rotate_right(node._value)
                        break
                    else:
                        node = node._right
                if i == depth - 2:
                    break
            blen = self.depth() - 1
            m = blen // 2
            while m != 0:
                values = [self._top._value]
                node = self._top
                for _ in range(1, m):
                    node = node._right._right
                    values.append(node._value)
                for value in values:
                    self.rotate_left(value)
                blen = blen - m - 1
                m = blen // 2