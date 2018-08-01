import numpy as np
import random
import pdb

def lhsamp_model(init_pop, opt):
    m = init_pop;  # opt.initpopsize;
    n = opt["V"];

    S = np.zeros((m,n));
    pdb.set_trace()

    for i in range(0 , n):
      S[:][i] = np.transpose(np.array([random.uniform(0, 1) for i in range(1,m+1)]) + (np.random.permutation(m) - 1)) / m;

    #generate each point
    for i in range(1,m):
        S[i][:] = opt["bound"][0][:] + (opt["bound"][1][:]-opt["bound"][0][:])*S[i][:]; #low + difference*rand(0,1)
    return S;
