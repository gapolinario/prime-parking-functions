import numpy as np
import re
from scipy.special import factorial


class Tree(object):
    # https://stackoverflow.com/a/2358075
    "Generic tree node."

    def __init__(self, name, children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    def __repr__(self):
        return self.name

    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

    def list_leaves(self):
        """
        Recursively collects all leaf nodes in the tree.

        Parameters:
            tree (Tree): The root of the tree or subtree.

        Returns:
            list: A list of leaf nodes.
        """
        if not self.children:  # If no children, this is a leaf
            return [self]

        leaves = []
        for child in self.children:
            leaves.extend(child.list_leaves())
        return leaves

    def list_leaf_names(self):
        leaves = self.list_leaves()
        names = [l.name for l in leaves]
        return names

    def get_height(self):
        if not self.children:
            return 1

        height = 1 + (self.children[0]).get_height()

        return height


def get_last_name(name):
    v = re.search(",", name)
    if v:
        m = re.search(r",(\d+)$", name)
        return m.group(1)
    else:
        m = re.search(r"^(\d+)$", name)
        return m.group(1)


def add_parking_children(tree, n):

    leaves = tree.list_leaves()

    # print(leaves)
    for leaf in leaves:
        start = int(get_last_name(leaf.name))
        for c in range(start, n):
            if c == 0:
                print(f"c=0!, {leaf}")
            leaf.add_child(Tree(leaf.name + "," + str(c)))


def to_base_n(number, base, length):
    """
    Convert a decimal number to its representation in base `base`.

    Parameters:
        number (int): The decimal number to convert.
        base (int): The target base (e.g., 2 for binary, 3 for ternary).

    Returns:
        list of int: The number represented in base `base` as a list of digits.
    """
    if number == 0:
        return [0]

    digits = []
    while number > 0:
        digits.append(number % base)
        number //= base

    rep = digits[::-1]
    if len(rep) < length:
        return np.concatenate((np.zeros(length - len(rep), dtype=int), rep))
    else:
        return rep


def brute_force_enum(n):
    """
    brute force enumeration of prime parking functions
    loops through all numbers from 0 to n^n-1 in base n
    """

    # i need some sort of gray code for this
    # complexity is n^n
    arr = np.ones(n, dtype=int)
    enum = 0
    count = 0

    while (arr != np.full(n, n)).any():
        count += 1
        if test_primePF(arr):
            enum += 1

        arr = np.array(to_base_n(count, n, n)) + 1

    if test_primePF(arr):
        enum += 1

    return enum


def analytical_enum(n):
    """
    exact result, see https://oeis.org/A000312
    """
    return (n - 1) ** (n - 1)


def tree_enum(n, prev_tree=None):

    if n == 1:
        tree = Tree("1")
        enum = 1
        return enum, tree
    
    else:
        assert prev_tree.get_height() == n - 1

        add_parking_children(prev_tree, n)

        leaves = prev_tree.list_leaves()

        enum = 0
        for l in leaves:
            enum += num_unique_perms_from_str(l.name)

        return enum, prev_tree


def num_unique_perms_from_str(name):

    arr = np.array([int(x) for x in re.split(",", name)])
    unq = set(arr)

    count = [None] * len(unq)
    for i, u in enumerate(unq):
        count[i] = len(np.argwhere(arr == u))

    num = factorial(len(arr), exact=True)
    for x in count:
        num = num // factorial(x, exact=True)

    return num


def test_primePF(f):

    f = np.sort(f)

    if f[0] != 1:
        return False

    for i, fi in enumerate(f[1:], start=2):
        if not (fi < i):
            return False

    return True

