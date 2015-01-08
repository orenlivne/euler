import pyximport
pyximport.install()
import rosalind.rosutil as ro, rosalind.rosalign as ra, numpy as np, time, sys
from rosalind.laff import rosalind_laff_v1 as laff

if __name__ == "__main__":
    laff.laff(sys.argv[1], debug=1)
