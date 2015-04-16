COLORS = ['blue', 'green', 'red', 'white', 'yellow']
PETS = ['cat', 'bird', 'dog', 'fish', 'horse']
BEVERAGES = ['beer', 'coffee', 'milk', 'tea', 'water']
CIGARETTES = ['Rothmans', 'Dunhill', 'Pall Mall', 'Winfield', 'Marlboro']
NATIONALITY = ['Brit', 'Dane', 'German', 'Norwegian', 'Swede']
NUMBERS = ['1', '2', '3', '4', '5']
QUESTIONS = ["number", "color", "nationality", "beverage", "cigarettes", "pet"]

matrix = [COLORS, PETS, BEVERAGES, CIGARETTES, NATIONALITY, NUMBERS]
flattenmatrix = [item for sublist in matrix for item in sublist]

def answer(relations, question):
    def f7(seq):
        seen = set()
        seen_add = seen.add
        return [ x for x in seq if not (x in seen or seen_add(x))]
    
    def makematches(alpha, beta):
        inplace = []
        for i in alpha:
            for j in beta:
                if i == j:
                    inplace = sorted(alpha + beta)
                    return f7(inplace)
          
    def more(llist):                                
        matches = []
        madematch = []
        toappend = []
        for i in llist:
            for j in llist:
                if i != j:
                    if makematches(i, j) and makematches(i, j) not in matches:
                        matches.append(makematches(i, j))
                        madematch.append(i)
                        madematch.append(j)
        if matches:
            for i in llist:
                if i not in madematch:
                    toappend.append(i)
            return matches + toappend
        else:
            return llist
    
    def rule(x, y):
        count = 0
        for i in x:
            for j in y:
                if i == j:
                    count = count + 1
                    if count == 2:
                        return False
        return True

    def superrule(x, y):
        for i in x:
            for j in y:
                if not rule(i, j):
                    return False
        else:
            return True
              
    def category(x, y):
        if x in y:
            return True
        else:
            return False
    
    def missingcategory(x, y):
        count = 0
        for i in x:
            if i in y:
                count = count + 1
        if count == 0:
            return True
        else:
            return False

    hh = list(relations)
    new = []

    for i in hh:
        new_str = i.replace('-', ' ')
        new.append(new_str)

    hhh = []
    for i in new:
        g = i.split()
        hhh.append(g)
    
    while len(more(hhh)) != len(hhh):
        hhh = more(hhh)
    
    flat_hhh = [item for sublist in hhh for item in sublist]
    leftovers = []
    
    for i in flattenmatrix:
        if i not in flat_hhh:
            leftovers.append(i)
        
    helper = []
    for i in hhh:
        for j in hhh:
            if len(i + j) < 7:
                count = 0
                for n in matrix:
                    if rule(i + j, n):
                        count = count + 1
                        if count == 6:
                            helper.append(i + j)
                            hhh.remove(i)
                            hhh.remove(j)


    for i in helper:
        hhh.append(sorted(i))  
        
        
    for i in leftovers:
        for j in hhh:
            for k in matrix:
                if missingcategory(j, k) and category(i, k):
                    j.append(i)
                           
    newanswer = question.replace('-', ' ')
    gv = newanswer.split()
    if gv[1] != 'nationality':
        if gv[1] != 'cigarettes':
            nexter = gv[1].upper() + 'S'
            gv.remove(gv[1])
            gv.append(nexter)
            
        if gv[1] == 'cigarettes':
            nexter = gv[1].upper()
            gv.remove(gv[1])
            gv.append(nexter)
    if gv[1] == 'nationality':
        nexter = gv[1].upper()
        gv.remove(gv[1])
        gv.append(nexter)
        
    for i in hhh:
        if gv[0] in i:
            for j in i:
                if j in eval(gv[1]):
                    return j        


if __name__ == '__main__':
    assert answer(('Norwegian-Dunhill', 'Marlboro-blue', 'Brit-3',
                   'German-coffee', 'beer-white', 'cat-water',
                   'horse-2', 'milk-3', '4-Rothmans',
                   'dog-Swede', 'Norwegian-1', 'horse-Marlboro',
                   'bird-Brit', '4-green', 'Winfield-beer',
                   'Dane-blue', '5-dog', 'blue-horse',
                   'yellow-cat', 'Winfield-Swede', 'tea-Marlboro'),
                  'fish-color') == 'green'  # What is the color of the house where the Fish lives?
    assert answer(('Norwegian-Dunhill', 'Marlboro-blue', 'Brit-3',
                   'German-coffee', 'beer-white', 'cat-water',
                   'horse-2', 'milk-3', '4-Rothmans',
                   'dog-Swede', 'Norwegian-1', 'horse-Marlboro',
                   'bird-Brit', '4-green', 'Winfield-beer',
                   'Dane-blue', '5-dog', 'blue-horse',
                   'yellow-cat', 'Winfield-Swede', 'tea-Marlboro'),
                  'tea-number') == '2'  # What is the number of the house where tea is favorite beverage?
    assert answer(('Norwegian-Dunhill', 'Marlboro-blue', 'Brit-3',
                   'German-coffee', 'beer-white', 'cat-water',
                   'horse-2', 'milk-3', '4-Rothmans',
                   'dog-Swede', 'Norwegian-1', 'horse-Marlboro',
                   'bird-Brit', '4-green', 'Winfield-beer',
                   'Dane-blue', '5-dog', 'blue-horse',
                   'yellow-cat', 'Winfield-Swede', 'tea-Marlboro'),
                  'Norwegian-beverage') == 'water'  # What is the favorite beverage of the Norwegian man?
