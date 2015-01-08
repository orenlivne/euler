'''
============================================================
Arrays and strings.
============================================================
'''
MINUS_ONE = -1

def first_nonrepeated_char(s):
    '''O(n)-average run time, where n=len(s).'''
    d = {}
    for i, c in enumerate(s): d[c] = (-1 if d.has_key(c) else i)
    return min((i, c) for c, i in d.iteritems() if i >= 0)[1]

def first_nonrepeated_char2(s):
    '''O(n)-average run time, where n=len(s).'''
    d = {}
    for i, c in enumerate(s):
        v = d.get(c)
        if v:
            if v != MINUS_ONE: d[c] = MINUS_ONE
        else: d[c] = i
    return min((i, c) for c, i in d.iteritems() if i >= 0)[1]

if __name__ == "__main__":
    print first_nonrepeated_char('total')  # 'o'
    print first_nonrepeated_char('teeter')  # 'r

    print first_nonrepeated_char2('total')  # 'o'
    print first_nonrepeated_char2('teeter')  # 'r
