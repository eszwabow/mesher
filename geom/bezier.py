import numpy as np

import matplotlib.pyplot as plt
def test():
    print('TESTING BEZIER.PY')
    
    xp = np.array([0.3, 0.1, 0.21, 0.5, 0.55, 0.75, 0.9, 0.91])
    yp = np.array([.15, .3, .85, .75, .35, .18, .42, .7])
    
    x,y = bezier_curve(xp, yp)
    
    plt.plot(x,y)
    plt.show()
    
    return

def bezier_curve(xp, yp):
    x, y = build_curve(list(zip(xp, yp))).T
    
    return x, y

from scipy.special import binom
def bernstein_poly(n, k):
   
    coeff = binom(n, k)

    def _bern_poly(x):
        return coeff * x ** k * (1 - x) ** (n - k)

    return _bern_poly

def build_curve(points, num=200):

    N = len(points)
    t = np.linspace(0, 1, num=num)
    curve = np.zeros((num, 2))
    for i, point in enumerate(points):
        curve += np.outer(bernstein_poly(N - 1, i)(t), point)
    return curve

if __name__ == "__main__":
    test()    
