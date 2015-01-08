'''
============================================================
http:# projecteuler.net/problem=144

In laser physics, a "white cell" is a mirror system that acts as a delay line for the laser beam. The beam enters the cell, bounces around on the mirrors, and eventually works its way back out.

The specific white cell we will be considering is an ellipse with the equation 4x2 + y2 = 100

The section corresponding to 0.01  x  +0.01 at the top is missing, allowing the light to enter and exit through the hole.


The light beam in this problem starts at the point (0.0,10.1) just outside the white cell, and the beam first impacts the mirror at (1.4,-9.6).

Each time the laser beam hits the surface of the ellipse, it follows the usual law of reflection "angle of incidence equals angle of reflection." That is, both the incident and reflected beams make the same angle with the normal line at the point of incidence.

In the figure on the left, the red line shows the first two points of contact between the laser beam and the wall of the white cell the blue line shows the line tangent to the ellipse at the point of incidence of the first bounce.

The slope m of the tangent line at any point (x,y) of the given ellipse is: m = 4x/y

The normal line is perpendicular to this tangent line at the point of incidence.

The animation on the right shows the first 10 reflections of the beam.

How many times does the beam hit the internal surface of the white cell before exiting?
============================================================
'''
import numpy as np, matplotlib.pyplot as P

def hits((x0, y0), (x1, y1)):
    m, (x, y) = (y1 - y0) / (x1 - x0), (x1, y1)
    yield x0, y0
    yield x, y
    while (x < -0.01) or (x > 0.01) or (y <= 0):
        t = y / (4 * x)
        p = 2 * t / (1 - t * t)
        N = (p - m) / (1 + p * m) / 2
        x1 = (x * N * N - x - N * y) / (1 + N * N)
        y1 = y + 2 * N * (x1 - x)
        m, (x, y) = (y1 - y) / (x1 - x), (x1, y1)
        yield x, y

# Python translation of the C# solution of
# http:# www.mathblog.dk/project-euler-144-investigating-multiple-reflections-of-a-laser-beam/
# Mine is better - no quadratic equation needed. We factor out the x-x0 factor.
def num_hits_mathblog((xA, yA), (xO, yO)):
    yield (xA, yA)
    yield (xO, yO)
    while (xO > 0.01 or xO < -0.01 or yO < 0):
        # Calculate the slope of A
        slopeA = (yO - yA) / (xO - xA)
     
        # Calculate the slope of the ellipse tangent
        slopeO = -4 * xO / yO
     
        # Calculate the slope of B
        tanA = (slopeA - slopeO) / (1 + slopeA * slopeO)
        slopeB = (slopeO - tanA) / (1 + tanA * slopeO)
     
        # calculate intercept of line B
        interceptB = yO - slopeB * xO
     
        # solve the quadratic equation for finding
        #  the intersection of B and the ellipse
        #  a*x^2 + b*x + c = 0
        
        # Note: this is inefficient and floating-point-precision-prone.
        # Better to reduce to a linear equation as I did. Commented on Kristian's
        # mathblog and he agreed with me.
        a = 4 + slopeB * slopeB
        b = 2 * slopeB * interceptB
        c = interceptB * interceptB - 100
     
        ans1 = (-b + np.sqrt(b * b - 4 * a * c)) / (2 * a)
        ans2 = (-b - np.sqrt(b * b - 4 * a * c)) / (2 * a)
     
        xA = xO
        yA = yO
     
        # Take the solution which is furtherest from x0
        xO = ans1 if (np.abs(ans1 - xO) > np.abs(ans2 - xO)) else ans2
        yO = slopeB * xO + interceptB
        yield (xO, yO)

def plot_hit_path(r, a, crack_size, h):
    t = np.linspace(0, 2 * np.pi, 300)
    t_left, t_right = np.arcsin(-crack_size / (r * a)), np.arcsin(crack_size / (r * a))
    t_crack = np.linspace(t_left, t_right, 50)
    
    fig = P.figure()
    ax = fig.add_subplot(111, aspect='equal')
    P.hold(True)
    ax.plot(r * a * np.sin(t), r * np.cos(t), 'b-')
    ax.plot(r * a * np.sin(t_crack), r * np.cos(t_crack), 'k-', linewidth=5)
    ax.set_xlim(-1.2 * a * r, 1.2 * a * r)
    ax.set_ylim(-1.2 * r, 1.2 * r)

    for i in xrange(min(10, len(h) - 1)):
        P.plot([h[i][0], h[i + 1][0]], [h[i][1], h[i + 1][1]], 'r-')
        if i < 1:
            x1, y1 = h[i + 1]
            m = y1 / (4 * x1)
            x = np.linspace(-6, 6, 10)
            P.plot(x, y1 + m * (x - x1), 'k--')
        # time.sleep(1)
    # P.show()
          
if __name__ == "__main__":
    r, a, crack_size = 10.0, 0.5, 0.01
    h = list(hits((0, 10.1), (1.4, -9.6)))
    print len(h) - 2, h
    hh = list(num_hits_mathblog((0, 10.1), (1.4, -9.6)))
    print len(hh) - 2, hh
    print sum((np.abs(h[i][0] - hh[i][0]) + np.abs(h[i][1] - hh[i][1])) / np.abs(h[i][0] + h[i][1]) for i in xrange(len(h))) / len(h)
