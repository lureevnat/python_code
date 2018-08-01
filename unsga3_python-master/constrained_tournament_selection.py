import numpy as np
import lex_dominate
import random


def constrained_tournament_selection(opt, pop, popObj, popCV):
    N = opt["N"]; # pop size

    #----TOURNAMENT CANDIDATES-------------------------------------------------

    tour1 = np.random.permutation(N);
    tour2 = np.random.permutation(N);

    #----START TOURNAMENT SELECTION--------------------------------------------


    selected_pop = np.zeros((N, opt.V)); # Only the design variables of the selected members

    for i in range(1,N):
        p1 = tour1(i);
        p2 = tour2(i);

        if (popCV(p1)<=0 and popCV(p2)<=0):#both are feasible

            obj1 = popObj[p1][:];
            obj2 = popObj[p2][:];
            d = lex_dominate(obj1, obj2);

            if d == 1: #p1 dominates p2
                selected_pop[i][:] = pop[p1][1:opt["V"]];
            elif d == 3: # p2 dominates p1
                selected_pop[i][:] = pop[p2][1:opt["V"]];
            else: # d == 2
                # check crowding distance
                if(opt["CD"][p1]>opt["CD"][p2]):
                    selected_pop[i][:] = pop[p1][1:opt["V"]];
                elif (opt["CD"][p1]<opt["CD"][p2]):
                    selected_pop[i][:] = pop[p1][1:opt["V"]];
                else: #randomly pick any solution
                    if(random.uniform(0,1) <= 0.5):
                        pick = p1;
                    else:
                        pick = p2;

                    selected_pop[i][:] = pop[pick][1:opt["V"]];
        else:
            if(popCV(p1) < popCV(p2)): #p1 less constraint violation
                selected_pop[i][:] = pop[p1][1:opt["V"]];
            else:
                if (popCV[p2] < popCV[p1]):
                    selected_pop[i][:] = pop[p1][1:opt["V"]]; #p2 has less constraint violation
                else: #randomly pick any solution
                    if(random.uniform(0,1) <= 0.5):
                        pick = p1;
                    else:
                        pick = p2;

                    selected_pop[i][:] = pop[pick][1:opt["V"]];#initially p1 was randomly choosen
    return selected_pop;
