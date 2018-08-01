import numpy as np
import random
def sbx(pop_selection, p_cross, nrealcross, eta_c, Xmin, Xmax, epsilon):

    [N, nreal] = pop_selection.shape; # Population size & Number of variables
    pop_crossover = np.zeros( pop_selection.shape );#Child population


    if N%2 != 0: #check if N is odd
        pop_crossover[N][:] = pop_selection[np.randint(1,N)][:];#pick a random element for last solution if N is odd
        N = N - 1;
    p = np.random.permutation(N);
    for ind in range(1,N,2):

        p1 = p(ind);
        p2 = p(ind+1);
        parent1 = pop_selection[p1][:];
        parent2 = pop_selection[p2][:];
        child1 = np.zeros(1, nreal);
        child2 = np.zeros(1, nreal);
        if random.uniform(0,1) <= p_cross:
            nrealcross = nrealcross+1;
            for i in range(1,nreal):
                if random.uniform(0,1) <= 0.5:
                    if abs( parent1(i)-parent2(i) ) > epsilon:
                        if parent1(i) < parent2(i):
                            y1 = parent1(i);
                            y2 = parent2(i);
                        else:
                            y1 = parent2(i);
                            y2 = parent1(i);

                        yl = Xmin(i);
                        yu = Xmax(i);
                        beta = 1.0 + (2.0*(y1-yl)/(y2-y1));
                        alpha = 2.0 - beta^(-(eta_c+1.0));
                        rand_var = random.uniform(0,1);
                        if rand_var <= (1.0/alpha):
                            betaq = (rand_var*alpha)**(1.0/(eta_c+1.0));
                        else:
                            betaq = (1.0/(2.0 - rand_var*alpha))**(1.0/(eta_c+1.0));

                        c1 = 0.5*((y1+y2) - betaq*(y2-y1));
                        beta = 1.0 + (2.0*(yu-y2)/(y2-y1));
                        alpha = 2.0 - beta^(-(eta_c+1.0));
                        if rand_var <= (1.0/alpha):
                            betaq = (rand_var*alpha)**(1.0/(eta_c+1.0));
                        else:
                            betaq = (1.0/(2.0 - rand_var*alpha))**(1.0/(eta_c+1.0));

                        c2 = 0.5*((y1+y2)+betaq*(y2-y1));
                        if (c1 < yl):
                            c1 = yl;
                        if (c2 < yl):
                            c2 = yl;
                        if (c1 > yu):
                            c1 = yu;
                        if (c2 > yu):
                            c2 = yu;
                        if random.uniform(0,1) <= 0.5:
                            child1[i] = c2;
                            child2[i] = c1;
                        else:
                            child1[i] = c1;
                            child2[i] = c2;

                    else:
                        child1[i] = parent1[i];
                        child2[i] = parent2[i];
                else:
                    child1[i] = parent1[i];
                    child2[i] = parent2[i];


        else:
            child1 = parent1;
            child2 = parent2;

        pop_crossover[ind][:] = child1;
        pop_crossover[ind+1][:] = child2;
    return [pop_crossover, nrealcross]


