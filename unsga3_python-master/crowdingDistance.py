import numpy as np

def crowdingDistance(opt, f, objective):
    CDF=[]
    if f.shape[2]==1:
        CDF = opt.Inf;
    elif f.shape[2]==2:
        CDF[1] = opt.Inf;
        CDF[2] = opt.Inf;
    else:
        [M1, I1] = np.min(objective);
        [M2, I2] = np.max(objective);

        I = np.concatenate(I1, np.transpose(I2),axis=1);
        I = np.unique(I);


        CDF = np.zeros((f.shape[2],1));
        for i in range(1,objective.shape[2]):

            [_,index] = objective[:][i].sort(axis=1);
            for j in range( 2,index.shape[1]-1):
                if (abs(M2(i)-M1(i)) > opt.Epsilon):
                    CDF[index(j)] = CDF(index(j))+ ((objective(index(j+1),i)-objective(index(j-1),i))/(M2(i)-M1(i)))  ;

        CDF[2:-1-1] = CDF[2:-1-1]/ objective.shape[2];
        CDF[I] = opt.Inf;
    return [CDF]
