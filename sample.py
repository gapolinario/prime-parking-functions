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

    #for w,l in zip(weights,leaves):
    #    print(f"{l}: {w}")

    weights *= 1.0/np.sum(weights)

    rng = np.random.default_rng()

    for _ in range(num_samples):

        k = rng.choice(len(leaves), p=weights)
        array = re.split(',',leaves[k].name)
        sample = rng.permutation(array)

        print(f"{sample}")

if __name__ == "__main__":

    main(10, 100)
