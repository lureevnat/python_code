import numpy as np
import high_fidelity_evaluation


def evaluate_pop(opt, pop):

    popObj = np.zeros((pop.shape[1],opt["M"]));
    if opt.C>0:
        popCons = np.zeros((pop.shape[1],opt.C));
    else:
        popCons = np.zeros((pop.shape[1], 1));
    sz = pop.shape[1];
    for i in range(1,sz):

        [f, g] = high_fidelity_evaluation(opt, pop[i][:]);
        popObj[i][1:opt.M] = f;
        if opt["C"]>0:
            popCons[i][:] = g;
        else:
            popCons[i][1] = 0;
    return [popObj, popCons];
