import numpy as np
import math
def bos(objective):

    if objective.size:
       R = [];
       F = [];
       return [R,F];
    elif objective.shape[1]==1:
        R = 1;
        F = [{}]
        F[0]['f'] = 1;
        return [R,F];

    #--------INITIALIZATION---------------
    [n,m]= objective.shape;
    R = np.ones((n,1));

    if(m<4):
        m1 = m;
    else:
        m1 = math.floor(min(math.ceil(math.log2(n)),m));
    #---------SORTING PART-----------------
    Q = np.zeros((n, m1));
    lex_order = np.zeros((n,1));

    #--------FIND LEX ORDER----------------
    #objective[objective[:,0].argsort(),]
    [_,Q[:,1]] = objective[objective[:,0].argsort(),];

    for i in range(1,n):
        lex_order[Q(i,1)] = i;


    for i in range(2,m1):
       #H = horzcat(objective(:,i), lex_order);#in case of tie use lex order
       H = np.concatenate(objective[:][i], np.transpose(objective[:][1]),axis=1);
       [_,Q[:][i]] = H[H[:,0].argsort(),];




    #-------RANKING PART-------------------
    done = np.zeros((n, 1));
    total = 0;
    totalfront = 1;
    L = [[[]]*n]*m1
    #L = cell(m1, n);
    for i in range( 1,n):
        for j in range(1,m1):
            s  = Q(i,j);
            if done(s) == 1:
                L[j][R(s)] = np.concatenate(s, np.transpose(np.array(L[j][R(s)])),axis=1);
                continue;

            total = total + 1;
            done[s] = 1;


            for k in range(1, totalfront): #for all front
                d = 0;
                sz = np.array(L[j][k]).shape[2];
                for l in range(1,sz): # for all elements
                    d = lex_dominate(objective(L[j][k][l][:]), objective[s][:]);
                    if d == 1:
                       break;

                if d == 0: #not dominates
                    R[s] = k;
                    L[j][k] = np.concatenate(s, np.transpose(L[j][k]),axis=1);
                    break;

                elif d==1 and k==totalfront:
                    totalfront = totalfront + 1;
                    R[s] = totalfront;
                    L[j][totalfront] = np.concatenate(s, np.transpose(np.array(L[j][totalfront])),axis=1);
                    break;


            if total==n:
               break
    F = []
    F[n]["f"] = [];

    for i in range(1,n):
        F[R[i]]["f"] = [F[R[i]]["f"],i];
    return [R,F]
# checks lexicographical domination of two solutions
def lex_dominate(obj1, obj2):


    equal = 1;
    d = 1;
    sz = obj1.shape[2];
    for i in range(1,sz):
        if obj1(i) > obj2(i):
            d = 0;
            break;
        elif(equal==1 and obj1(i) < obj2(i)):
            equal = 0;
    if d ==1 and equal==1: #check if both solutions are equal
        d = 0;

    return [d];
