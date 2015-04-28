def sub(a, b): return [x-y for x, y in zip(a, b)]

def shot(w0, w1, u0, u1):
  u = sub(u1, u0)
  w = sub(w0, w1)
  z = sub(w0, u0)
  d = float(u[0] * w[1] - u[1] * w[0])
  if abs(d) < 1e-15: return -1
  a = (w[1] * z[0] - w[0] * z[1]) / d
  b = (u[0] * z[1] - u[1] * z[0]) / d
  return -1 if a < 0 or b < 0 or b > 1 else int(round(100 * (1 - abs(2 * b - 1))))

if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert shot((2, 2), (5, 7), (11, 2), (8, 3)) == 100, "1st case"
    assert shot((2, 2), (5, 7), (11, 2), (7, 2)) == 0, "2nd case"
    assert shot((2, 2), (5, 7), (11, 2), (8, 4)) == 29, "3th case"
    assert shot((2, 2), (5, 7), (11, 2), (9, 5)) == -1, "4th case"
    assert shot((2, 2), (5, 7), (11, 2), (10.5, 3)) == -1, "4th case again"
    assert shot((2,2),(5,7),(8,3),(11,2)) == -1, 'reverse'
    assert shot((10,10),(10,90),(50,90),(50,50)) == -1, 'vertical'
