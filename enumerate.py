"""
Enumerate prime parking functions
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
from time import time

from functions import *


def main(bfmax, nmax, verbose):

    # nmax = 7 takes 5s to run with brute force
    tree = None

    outBF = "data/timeBF.dat"
    outTR = "data/timeTR.dat"

    fBF = open(outBF, "a")
    fTR = open(outTR, "a")

    for n in range(1, min(bfmax, nmax)):
        t = time()
        enumBF = brute_force_enum(n)
        timeBF = time() - t

        t = time()
        enumTR, tree = tree_enum(n, tree)
        timeTR = time() - t

        assert enumBF == analytical_enum(n)
        assert enumTR == analytical_enum(n)
        if verbose:
            print(f"n={n}, enumBF={enumBF} enumTR={enumTR}")

        fBF.write(f"{n}, {timeBF}\n")
        fTR.write(f"{n}, {timeTR}\n")

    # from here on, no brute force evaluation
    for n in range(min(bfmax, nmax), nmax):

        t = time()
        enumTR, tree = tree_enum(n, tree)
        timeTR = time() - t

        assert enumTR == analytical_enum(n)
        if verbose:
            print(f"n={n}, enumTR={enumTR}")

        fTR.write(f"{n}, {timeTR}\n")

    fBF.close()
    fTR.close()

    print("Enumeration finished!")


def test_tree():

    tree = Tree("1")
    assert tree.list_leaf_names() == ["1"]

    tree = Tree("1", [Tree("11")])
    assert tree.list_leaf_names() == ["11"]

    tree = Tree("1", [Tree("11", [Tree("111"), Tree("112")])])
    assert tree.list_leaf_names() == ["111", "112"]

    tree = Tree(
        "1",
        [
            Tree(
                "11",
                [
                    Tree("111", [Tree("1111"), Tree("1112"), Tree("1113")]),
                    Tree("112", [Tree("1122"), Tree("1123")]),
                ],
            )
        ],
    )
    assert tree.list_leaf_names() == ["1111", "1112", "1113", "1122", "1123"]


if __name__ == "__main__":

    test_tree()

    main(8, 15, True)
    for _ in range(9):
        main(8, 15, False)
