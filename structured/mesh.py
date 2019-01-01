import numpy as np
import math
from geom import meshtools

import matplotlib.pyplot as plt



def test():
    imax = 385
    jmax = 65
    omega = 1.5
    niter = 30
    
    X = np.zeros((imax, jmax))
    Y = np.zeros((imax, jmax))
    
    ########## I = 1 ##########
    with open('./example/i1.txt', 'r') as fp:
        lines = fp.readlines()
        
    nlines = int(lines[0])    
    assert nlines == jmax, 'WRONG NUMBER OF POINTS IN I1.TXT'
    
    for j in range(0,jmax):
        line = lines[j+1]
        xj = float(line.split()[0])
        yj = float(line.split()[1])
        
        X[0, j] = xj
        Y[0, j] = yj
        
        
    ########## IMAX ##########
    with open('./example/imax.txt', 'r') as fp:
        lines = fp.readlines()
        
    nlines = int(lines[0])
    assert nlines == jmax, 'WRONG NUMBER OF POINTS IN IMAX.TXT'
    
    for j in range(0,jmax):
        line = lines[j+1]
        xj = float(line.split()[0])
        yj = float(line.split()[1])
        
        X[imax-1, j] = xj
        Y[imax-1, j] = yj
    
    ########## J = 1 ##########
    with open('./example/j1.txt', 'r') as fp:
        lines = fp.readlines()
        
    nlines = int(lines[0])    
    assert nlines == imax, 'WRONG NUMBER OF POINTS IN J1.TXT'
    
    for i in range(0,imax):
        line = lines[i+1]
        xi = float(line.split()[0])
        yi = float(line.split()[1])
        
        X[i, 0] = xi
        Y[i, 0] = yi
        
    ########## JMAX ##########
    with open('./example/jmax.txt', 'r') as fp:
        lines = fp.readlines()
        
    nlines = int(lines[0])
    assert nlines == imax, 'WRONG NUMBER OF POINTS IN JMAX.TXT'
    
    for i in range(0,imax):
        line = lines[i+1]
        xi = float(line.split()[0])
        yi = float(line.split()[1])
        
        X[i, jmax-1] = xi
        Y[i, jmax-1] = yi
    
    X = tfi(X, imax, jmax)
    Y = tfi(Y, imax, jmax) 
    
    P, Q = initControlFunctions(X, Y, imax, jmax)
    
    make2dmesh(imax, jmax, X, Y, omega, niter) # BAD!!!!!!!!!
    
    plot(X, Y, imax, jmax)
    
    return

def plot(X, Y, imax, jmax):
    
        ########## PLOTTING #############
    # Loop over every block and plot it
    fig1 = plt.figure(1)
    ax = plt.gca()
    
    # Plot the i=const lines
    for i in range(imax):
        x = X[i,:]
        y = Y[i,:]
        
        ax.plot(x,y, "k-")
        
    # Plot the j=const lines    
    for j in range(jmax):
        x = X[:,j]
        y = Y[:,j]
        
        ax.plot(x,y, "r-")
            
    
    plt.show()

def tfi(A, imax, jmax):

    for i in range(1, imax):
        for j in range(1, jmax):
            dI = (float(imax) - float(i)) / float(imax);
            dJ = (float(jmax) - float(j)) / float(jmax);
            JJ = float(j) / float(jmax);
            II = float(i) / float(imax);
            

            A[i, j] = (dI*A[0, j] + II*A[imax-1, j] + dJ*A[i, 0] + JJ*A[i, jmax-1]) - (dI*dJ*A[0, 0] + II*dJ*A[imax-1, 0] + JJ*dI*A[0, jmax-1] + II*JJ*A[imax-1, jmax-1])

    return A

def initControlFunctions(X, Y, imax, jmax):
    
    P = np.zeros((imax, jmax))
    Q = np.zeros((imax, jmax))
    
    ########## I = 1 ##########
    for j in range(1, jmax-2):
        dxdi = (X[1, j] - X[0,j])
        dxdj = 0.5 * (X[0, j+1] - X[0,j-1])
    
        dxdi = (Y[1, j] - Y[0,j])
        dxdj = 0.5 * (Y[0, j+1] - Y[0,j-1])
        
        d2xdi2 = X[2, j  ] + X[0, j  ] - 2.0*X[1, j];
        d2xdj2 = X[0, j+1] + X[0, j-1] - 2.0*X[0, j];    

        d2ydi2 = Y[2, j  ] + Y[0, j  ] - 2.0*Y[1, j];
        d2ydj2 = Y[0, j+1] + Y[0, j-1] - 2.0*Y[0, j]; 
        
        d2xdidj = 0.5*( (X[1, j+1] - X[0, j+1]) - (X[1, j-1] - X[0, j-1]) )
        d2ydidj = 0.5*( (Y[1, j+1] - Y[0, j+1]) - (Y[1, j-1] - Y[0, j-1]) )
    
        g11 = dxdi*dxdi + dydi*dydi
        g22 = dxdj*dxdj + dydj*dydj
        g12 = dxdi*dxdj + dydi*dydj
        
        P[0, j] = -(dxdi*d2xdi2 + dydi*d2ydi2)/g11 - (dxdi*d2xdj2 + dydi*d2ydj2)/g22
        Q[0, j] = -(dxdj*d2xdj2 + dydj*d2ydj2)/g22 - (dxdj*d2xdi2 + dydj*d2ydi2)/g11
    
    ########## IMAX ##########
    for j in range(1, jmax-2):
        dxdi = (X[imax-1, j] - X[imax-2,j])
        dxdj = 0.5 * (X[imax-1, j+1] - X[imax-1,j-1])
    
        dxdi = (Y[imax-1, j] - Y[imax-2,j])
        dxdj = 0.5 * (Y[imax-1, j+1] - Y[imax-1,j-1])
        
        d2xdi2 = X[imax-1, j  ] + X[imax-3, j  ] - 2.0*X[imax-2, j];
        d2xdj2 = X[imax-1, j+1] + X[imax-1, j-1] - 2.0*X[imax-1, j];    

        d2ydi2 = Y[imax-1, j  ] + Y[imax-3, j  ] - 2.0*Y[imax-2, j];
        d2ydj2 = Y[imax-1, j+1] + Y[imax-1, j-1] - 2.0*Y[imax-1, j]; 
        
        d2xdidj = 0.5*( (X[imax-1, j+1] - X[imax-2, j+1]) - (X[imax-1, j-1] - X[imax-2, j-1]) )
        d2ydidj = 0.5*( (Y[imax-1, j+1] - Y[imax-2, j+1]) - (Y[imax-1, j-1] - Y[imax-2, j-1]) )
        
        g11 = dxdi*dxdi + dydi*dydi
        g22 = dxdj*dxdj + dydj*dydj
        g12 = dxdi*dxdj + dydi*dydj
        
        P[imax-1, j] = -(dxdi*d2xdi2 + dydi*d2ydi2)/g11 - (dxdi*d2xdj2 + dydi*d2ydj2)/g22
        Q[imax-1, j] = -(dxdj*d2xdj2 + dydj*d2ydj2)/g22 - (dxdj*d2xdi2 + dydj*d2ydi2)/g11
    
    ########## J = 1 ##########
    for i in range(1, imax-2): # GOOD HERE
        asd
        dxdi = (X[1, j] - X[0,j])
        dxdj = 0.5 * (X[0, j+1] - X[0,j-1])
    
        dxdi = (Y[1, j] - Y[0,j])
        dxdj = 0.5 * (Y[0, j+1] - Y[0,j-1])
        
        d2xdi2 = X[2, j  ] + X[0, j  ] - 2.0*X[1, j];
        d2xdj2 = X[0, j+1] + X[0, j-1] - 2.0*X[0, j];    

        d2ydi2 = Y[2, j  ] + Y[0, j  ] - 2.0*Y[1, j];
        d2ydj2 = Y[0, j+1] + Y[0, j-1] - 2.0*Y[0, j]; 
        
        d2xdidj = 0.5*( (X[1, j+1] - X[0, j+1]) - (X[1, j-1] - X[0, j-1]) )
        d2ydidj = 0.5*( (Y[1, j+1] - Y[0, j+1]) - (Y[1, j-1] - Y[0, j-1]) )
    
        g11 = dxdi*dxdi + dydi*dydi
        g22 = dxdj*dxdj + dydj*dydj
        g12 = dxdi*dxdj + dydi*dydj
        
        P[0, j] = -(dxdi*d2xdi2 + dydi*d2ydi2)/g11 - (dxdi*d2xdj2 + dydi*d2ydj2)/g22
        Q[0, j] = -(dxdj*d2xdj2 + dydj*d2ydj2)/g22 - (dxdj*d2xdi2 + dydj*d2ydi2)/g11
    
    Q = tfi(Q, imax, jmax)
    P = tfi(P, imax, jmax)
    
    return P, Q

def make2dmesh(imax, jmax, X, Y, omega, niter):
    
    X = tfi(X, imax, jmax)
    Y = tfi(Y, imax, jmax)
    
    print('Elliptic solver')
    
    for n in range(niter):
        
        print('  Iteration %d' % (n+1))
    
        for i in range(1, imax-1):
            for j in range(1, jmax-1):
                dxdi = 0.5 * (X[i+1, j] - X[i-1,j])
                dxdj = 0.5 * (X[i, j+1] - X[i,j-1])
            
                dydi = 0.5 * (Y[i+1, j] - Y[i-1,j])
                dydj = 0.5 * (Y[i, j+1] - Y[i,j-1])
                
                d2xdi2 = X[i + 1, j] + X[i - 1, j] - 2.0*X[i, j];
                d2xdj2 = X[i, j + 1] + X[i, j - 1] - 2.0*X[i, j];    

                d2ydi2 = Y[i + 1, j] + Y[i - 1, j] - 2.0*Y[i, j];
                d2ydj2 = Y[i, j + 1] + Y[i, j - 1] - 2.0*Y[i, j];
                
                d2xdidj = 0.25*(X[i + 1, j + 1] - X[i + 1, j - 1] - X[i - 1, j + 1] + X[i - 1, j - 1])
                d2ydidj = 0.25*(Y[i + 1, j + 1] - Y[i + 1, j - 1] - Y[i - 1, j + 1] + Y[i - 1, j - 1])
        
                P = 0.
                Q = 0.
                
                a = dxdj*dxdj + dydj*dydj
                g = dxdi*dxdi + dydi*dydi
                b = dxdi*dxdj + dydi*dydj
                c = 2.*(a + g)
                
        
                x_tmp = a*(d2xdi2 + P * dxdi) - 2.0*b*d2xdidj + g*(d2xdj2 + Q * dxdj);
                
                y_tmp = a*(d2ydi2 + P * dydi) - 2.0*b*d2ydidj + g*(d2ydj2 + Q * dydj)
                
                X[i, j] = X[i, j] + omega*x_tmp/c
                Y[i, j] = Y[i, j] + omega*y_tmp/c
    
    
    return X, Y

if __name__ == "__main__":
    test()    


