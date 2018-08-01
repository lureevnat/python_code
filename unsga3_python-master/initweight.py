# This function is written by Dr. Aimin Zhou for generating any number of weight vectors
import numpy as np
import math


def initweight(objDim, N):
    U = math.floor(N**(1/(objDim-1)))-2;
    M = 0;
    while M<N:
        U = U+1;
        M = noweight(U, 0, objDim);
    W = np.zeros((objDim, M));
    C = 0;
    V = np.zeros((objDim, 1));
    [W, C] = setweight(W, C, V, U, 0, objDim, objDim);
    W = W / (U + 0.0);

    pos = (W < 1.0E-5);
    W[pos] = 1.0E-5;
    
    return W

##
def noweight(unit, sum, dim):

    M = 0;
    if dim == 1:
        M = 1; 
        return M
    for i in range(0,(unit-sum)+1,1):
        M = M + noweight(unit, sum + i, dim - 1);
    return M
##
def setweight(w, c, v, unit, sum, objdim, dim):
    if dim == objdim:
        v = np.zeros((objdim, 1));


    if dim == 1:
        c       = c + 1;
        v[0]    = unit - sum;
        for i in range(0,w.shape[0]):
            w[i][c-1] = v[i]
        #w[:, c-1]  = v;
        return([w,c]);
    for i in range(0,(unit-sum)+1,1):
        v[dim-1]  = i;
        [w, c]  = setweight(w, c, v, unit, sum + i, objdim, dim - 1);
    return([w,c])
