'''
============================================================
http://projecteuler.net/problem=102

Three distinct points are plotted at random on a Cartesian plane, for which -1000  x, y  1000, such that a triangle is formed.

Consider the following two triangles:

A(-340,495), B(-153,-910), C(835,-947)

X(-175,41), Y(-421,-714), Z(574,-645)

It can be verified that triangle ABC contains the origin, whereas triangle XYZ does not.

Using triangles.txt (right click and 'Save Link/Target As...'), a 27K text file containing the co-ordinates of one thousand "random" triangles, find the number of triangles for which the interior contains the origin.

NOTE: The first two examples in the file represent the triangles in the example given above.
============================================================
'''
line = lambda (x1, y1), (x2, y2): (y1 - y2, x2 - x1, (x2 - x1) * y1 - (y2 - y1) * x1)
line_eval = lambda (a, b), (x, y): a * x + b * y

def same_side(A, B, C):
    '''Is C and the origin on the same side of the line passing through A,B?'''
    a, b, c = line(A, B)
    # print 'line', l, (line_eval(tuple(l[:2]), A), line_eval(tuple(l[:2]), B), line_eval(tuple(l[:2]), C))
    return c * (c - a * C[0] - b * C[1]) > 0

origin_in_triangle = lambda A, B, C: same_side(A, B, C) and same_side(C, A, B) and same_side(B, C, A)
read_lines = lambda file_name: (((x[0], x[1]), (x[2], x[3]), (x[4], x[5])) for x in (map(int, x.rstrip('\r\n').rstrip('\n').split(',')) for x in open(file_name, 'rb')))

if __name__ == "__main__":
    print sum(origin_in_triangle(A, B, C) for A, B, C in read_lines('problem102.dat'))
