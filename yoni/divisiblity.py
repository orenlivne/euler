'''If n is an integer from 1 to 96 (inclusive), what is the probability for
n*(n+1)*(n+2) being divisible by 8?'''

def product_divisible_probability_brute_force(n):
    return sum(1 for n in xrange(1, n+1) if n*(n+1)*(n+2) % 8 == 0)

def product_divisible_probability(n):
    '''Count all even numbers and all numbers that are -1 (mod 8) between 1 and
    n.'''
    return (n+1)/8 + n/2

if __name__ == '__main__':
    for n in xrange(80, 101):
        bf = product_divisible_probability_brute_force(n)
        fast = product_divisible_probability(n)
        print n, 'bf', bf, 'fast', fast, 'error', fast-bf
