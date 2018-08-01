import paretoFront
import numpy as np

def calculate_feasible_paretofront(opt, pop, popObj, popCV):

    #-------------FIND FEASIBLE PARETO FRONT-------------------------------
    if opt.C>0: #Feasible Pareto front of Constraint Problems
        index = np.where(popCV<=0);
    else:
        #index = (1:pop.shape[1])';
        index = np.transpose(np.array([i for i in range(1,pop.shape[1]+1)]))

    FeasibleIndex = index;

    if index.shape[1]>0: # there are some feasible solutions
        index2 = paretoFront(popObj[index][:]);
        ParetoIndex = np.transpose(index[index2]);
    else: # no feasible solution yet
        ParetoIndex = [];

    return [FeasibleIndex, ParetoIndex];
