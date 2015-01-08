'''
============================================================
http://projecteuler.net/problem=170

Take the number 6 and multiply it by each of 1273 and 9854:

6 x 1273 = 7638
6 x 9854 = 59124

By concatenating these products we get the 1 to 9 pandigital 763859124. We will call 763859124 the "concatenated product of 6 and (1273,9854)". Notice too, that the concatenation of the input numbers, 612739854, is also 1 to 9 pandigital.

The same can be done for 0 to 9 pandigital numbers.

What is the largest 0 to 9 pandigital 10-digit concatenated product of an integer with two or more other integers, such that the concatenation of the input numbers is also a 0 to 9 pandigital 10-digit number?
============================================================
'''
import itertools as it, time

'''Notation: we split a pandigital number into a|b1|...|bn s.t. c1|...|cn is also
pandigital, where ci = a*bi.'''

NUM_DIGITS = 10
DIGIT_LIST = range(NUM_DIGITS)
DIGIT_SET = set(DIGIT_LIST)

def digits_of(x):
    '''Number to digit list.'''
    return map(int, str(x))

def num_of(digits):
    '''Digit list to num.'''
    return int(''.join(map(str, digits)))

def b_options(a, b_digits, c_digits, take_all):
    '''Given a and sets of b-digits and c-digits to choose from, yield all possible pairs (B,C),
    where B = list of digits of a possible b and C = list of digits of a*b. If take_all=True,
    then B,C must contain all elements of b_digits,c_digits, respectively. If take_all=False,
    B and C must have at least one element less than b_digits, c_digits, respectively.'''
    for B in (B for m in xrange(len(b_digits) if take_all else 1, len(b_digits) + (1 if take_all else 0))
              for B in it.permutations(b_digits, m)
              if (len(B) == 1 or B[0] != 0)):
        C = digits_of(a * num_of(B))
        C_set = set(C)
        if ((len(C) == 1) or C[0] != 0) and len(C) == len(C_set) and (not take_all or len(C) == len(c_digits)) and (C_set <= c_digits):
            yield B, C

def b_options_of_a(a, take_all):
    '''Yield all (B,C) pairs of a fixed a.'''
    return b_options(a, DIGIT_SET - set(digits_of(a)), DIGIT_SET, take_all)

def b_options_of_a_range(k_min, k_max, take_all):
    '''Yield all options (a, A, B, C) for all a with k digits, where k_min <= k < k_max. A is the digit
    list of a. B and C are the digit lists of b and c. If take_all=True, B must used all digits not used by a
    and C must use all digits (the case n=1). a must be divisible by 3.'''
    return ((a, A, B, C)  # @UndefinedVariable
            for A, a in ((A, num_of(A)) for k in xrange(k_min, k_max) 
                         for A in it.permutations(DIGIT_LIST, k) 
                         if A[0] != 0 and sum(A) % 3 == 0)
            for B, C in b_options_of_a(a, take_all))

def solutions_n1():
    '''Return all solutions (a,b,c) for n = 1. Note that by symmetry, we only need to check the cases
    a <= b, since (b,a,c) is also a solution. So a can have at most 5 digits.'''
    return ((a, b, c)
            for a, b, c in ((a, num_of(B), num_of(C)) for a, _, B, C in b_options_of_a_range(1, NUM_DIGITS / 2 + 1, True))
            if a <= b)

def solutions_n2():
    '''Return all solutions (a,(b1,b2),(c1,c2)) for n = 2. a must have k=2 digits.'''
    # Note: b1 cannot be 0 since the concatenated c-number cannot started with 0.''' 
    for a, A, B1, C1 in ((a, A, B, C)
                       for a, A, B, C in b_options_of_a_range(2, 3, False)
                       if B != (0,)):
        for B2, C2 in b_options(a, DIGIT_SET - set(A) - set(B1), DIGIT_SET - set(C1), True): 
            yield a, map(num_of, (B1, B2)), map(num_of, (C1, C2)), num_of(C1 + C2)

def max_concat_prod():
    s2 = list(solutions_n2())
    m2 = max((c, A, B, C) for A, B, C, c in s2)
    print 'n=2', 'max', (m2[1], m2[2], m2[3], m2[0]), '#solutions', len(s2)

    s1 = list(solutions_n1())
    m1 = max((c, a, b) for a, b, c in s1)
    print 'n=1', 'max', (m1[1], m1[2], m1[0]), '#solutions', len(s1)

    c = max(m1[0], m2[0])
    print 'Overall max', c, 'out of', len(s1) + len(s2), 'solutions'  
    return c

if __name__ == "__main__":
    start = time.time()
    max_concat_prod()
    print time.time() - start, 'sec'
