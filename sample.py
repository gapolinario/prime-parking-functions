"""
Sample uniformly from prime parking functions of given length
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

from functions import *

def main(nmax, num_samples):

    tree = None

    for n in range(1, nmax+1):    
        enumTR, tree = tree_enum(n, tree)
        assert enumTR == analytical_enum(n)

    leaves = tree.list_leaves()
    weights = np.empty(len(leaves))
    for i,l in enumerate(leaves):
        weights[i] = num_unique_perms_from_str(l.name)

    num_leaves = catalan_num(nmax-1)
    assert len(leaves) == num_leaves

    #for w,l in zip(weights,leaves):
    #    print(f"{l}: {w}")

    weights *= 1.0/np.sum(weights)

    rng = np.random.default_rng()

    for _ in range(num_samples):

        k = rng.choice(num_leaves, p=weights)
        array = re.split(',',leaves[k].name)
        sample = rng.permutation(array)

        print(f"{sample}")

if __name__ == "__main__":

    main(10, 100)
