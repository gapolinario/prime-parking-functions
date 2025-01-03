"""
Auxiliary functions to enumerate prime parking functions
Copyright (C) 2024, Gabriel B. Apolinario

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import numpy as np
import re
from scipy.special import factorial, comb
from collections.abc import Hashable
from functools import partial


class memoized(object):
    """Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).

    source: https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
    """

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return partial(self.__call__, obj)


@memoized
def exact_factorial(n):
    return factorial(n, exact=True)


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


def catalan_num(n):
    return comb(2 * n, n, exact=True) // (n + 1)


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

    arr = np.array([int(x) for x in name.split(",")])
    unique, counts = np.unique(arr, return_counts=True)
    
    total_perms = exact_factorial(len(arr))
    for x in counts:
        total_perms //= exact_factorial(x)

    return total_perms


def test_primePF(f):

    f = np.sort(f)

    if f[0] != 1:
        return False

    for i, fi in enumerate(f[1:], start=2):
        if not (fi < i):
            return False

    return True
