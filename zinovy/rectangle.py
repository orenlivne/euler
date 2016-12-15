import math

def dilate((l,w)):
  return (w*l + 1.0)/w, w + w/(w*l + 1.0)

if __name__ == '__main__':
  d = 1.0, 1.0
  r = d[0]/d[1]
  print d
  iters = 10000000
  for i in xrange(iters):
    d = dilate(d)
    rnew = d[0]/d[1]
    if i % (iters/10) == 0:
      print d, rnew, rnew - r, math.pi/2 - rnew
    r = rnew
