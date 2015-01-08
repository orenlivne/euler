'''
============================================================
Other Topics Chapter in Programming Exposed Book.
============================================================
'''
def num_ones(x, size=32):
    if x >= 0:  # count 1's
        s = 0
        while x:
            s += (x & 1)
            x = (x >> 1)
        return s
    else:
        s = size
        while x != -1:
            s -= (0 if x & 1 else 1)
            x = (x >> 1)
        return s

def num_ones_faster(x, size=32): # Got this to work only for positive x so far
    s = 0
    while x:
        x &= (x - 1)
        s += 1
    return s
    
if __name__ == "__main__":
    print num_ones(1234)  # 5
    print num_ones(-1234)  # 27
    print num_ones_faster(1234)  # 5
    #print num_ones_faster(-1234)  # Broken, will run forever
