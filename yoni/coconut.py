def is_solution(x, num_piles, num_people):
    '''Returns true if and only if x = the original number of coconuts satisfies
    the conditions of the problem with num_people repeating the stealing
    operation.'''
    for _ in xrange(num_people):
        if x % num_piles != 1:
            return False
        x = (num_piles-1)*((x-1)/num_piles)
    return True #x > 0

if __name__ == '__main__':
    for num_piles in xrange(1, 6):
        for num_people in xrange(1, 6):
            prospective_min_solution = num_piles**num_people - num_piles + 1
            for x in xrange(1, prospective_min_solution+1):
                if is_solution(x, num_piles, num_people):
                    print num_piles, num_people, x, prospective_min_solution
