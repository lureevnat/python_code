def evaluateCV(pop_cons):

    g = pop_cons;

    for i in range(1,pop_cons.shape[1]):
        for j in range(1,pop_cons.shape[2]):
            if g[i][j]<0:
                g[i][j] = 0;

    cv = sum(g, 2);
    return cv
