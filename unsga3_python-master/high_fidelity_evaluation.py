import math
import numpy as np
import sys


def high_fidelity_evaluation(opt,x):
    problem = opt["objfunction"].lower();
    g = []#extra
    f = []
    if list(problem) ==  list('c2dtlz2'):
            n=x.shape[2];
            nfunc = opt["M"];
            k = n - nfunc + 1;
            g = 0;
            for i in range(nfunc,n):
                g = g +  (x[i]-0.5)**2;

            fit = np.zeros((1,nfunc));
            for i in range(1,nfunc):
                h = 1 + g;
                for j in range(1,nfunc - i):
                    h =h * math.cos( x[j] * 3.141592654 / 2);
                if (i > 1):
                    h = h*math.sin( x[(nfunc - i + 1)] * 3.141592654 / 2);
                fit[i] = h;

            f[1] = fit[1];
            f[2] = fit[2];
            f[3] = fit[3];

            #now calculate constraints
            if(nfunc>3):
                r = 0.5;
            else:
                r = 0.4;
            v1 = sys.float_info.max;
            v2 = 0.0;
            for i in range(1, nfunc):
                sum1 = (f[i]-1.0)** 2.0;
                for j in range(1, nfunc):
                    if i != j:
                        sum1 = sum1 + (f[j])** 2.0;
                v1 = min(v1, sum1 - (r**2.0));
                v2 = v2 + (f[i] -  (1.0 / math.sqrt(nfunc)))** 2.0;
            c = min(v1, v2 - (r** 2.0));
            g[1] = c
            if c<=0:
                g[1]=c
            else:
                g[1]=c

    else:
            print('Function defition is not found inside high fidelity evaluation');

    #for unconstraint problem
    if opt["C"]==0:
       g = [];
    return [f,g];
