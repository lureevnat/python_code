import numpy as np
import bos
import crowdingDistance

def nsga2_selection(opt):


    [n, _] = opt["totalpopObj"].shape;
    opt.R = np.zeros(opt["totalpopObj"].shape[1],1);

    selectedPopIndex = [];
    index = opt.totalpopCV<=0;
    FeasiblePopIndex = np.where(index == 1);
    InfeasiblePopIndex = np.where(index == 0);

    #---------------Find Non-dominated Sorting of Feasible Solutions-------
    R = np.zeros((n,1));
    #F = cell(n,1);
    F = [[[]]*n]
    opt["R"] = np.zeros((n,1));
    if FeasiblePopIndex.size:

        [R,_] = bos(opt["totalpopObj"][FeasiblePopIndex][:]);

        for i in range(1,FeasiblePopIndex.shape[1]):
            F[R[i]] = np.concatenate(F[R[i]], np.transpose(FeasiblePopIndex[i]),axis=1);

        #---------------Store Ranking of Feasible Solutions--------------------
        opt["R"][FeasiblePopIndex] = R;





    #--------------Rank the Infeasible Solutions---------------------------

    if InfeasiblePopIndex.size:

        CV = opt["totalpopCV"][InfeasiblePopIndex];

        [_,index] = np.sort(CV,axis=0);
        c = max(R) + 1;

        for i in range(1, index.shape[1]):
            if i>1 and (CV(index(i))==CV(index(i-1))): #If both CV are same, they are in same front
                opt["R"][InfeasiblePopIndex[index(i)]] = opt["R"][InfeasiblePopIndex[index(i-1)]];
                b = opt["R"][InfeasiblePopIndex[index[i]]];
                F[b] = np.concatenate(F[b], InfeasiblePopIndex[index[i]],axis=1);
            else:
                opt["R"][InfeasiblePopIndex(index(i))] = c ;
                F[c] = np.concatenate(F[c], np.transpose(InfeasiblePopIndex[index[i]]), axis=1);
                c = c + 1;


    #----------------Select High Rank Solutions----------------------------
    count = np.zeros((n,1));
    for i in range(1,n):
        count[i] = np.array(F[i]).shape[2];

    cd = count.cumsum(axis=0);
    p1 = np.where(opt.N<cd);
    lastfront = p1[1];

    opt.pop = np.zeros(opt["pop"].shape);



    for i in range(1,lastfront-1):
        selectedPopIndex = np.concatenate(selectedPopIndex, np.transpose(F[i]),axis=1);



    #------------CROWDING DISTANCE PART------------------------------------

    opt["CD"] = np.zeros(opt["totalpopObj"].shape[1],1);
    for i in range(1,max(R)):
        front = F[i];
        front_cd = crowdingDistance(opt, front, opt["totalpopObj"][front][:]);
        opt["CD"][front] = front_cd;


    if selectedPopIndex.shape[2]<opt.N:
        index = F[lastfront];
        CDlastfront = opt.CD(index);

        [_,I] = np.sort(CDlastfront);

        j = 1;
        for i in range(selectedPopIndex.shape[2]+1, opt.N):
            selectedPopIndex = np.concatenate(selectedPopIndex, np.transpose(index[I[j]]),axis=1);
            j = j + 1;

    #---------------Select for Next Generation-----------------------------

    opt["pop"] =  opt["totalpop"][selectedPopIndex][:];
    opt["popObj"] = opt["totalpopObj"][selectedPopIndex][:];
    opt["popCV"] = opt["totalpopCV"][selectedPopIndex][:];
    opt["popCons"] = opt["totalpopCons"][selectedPopIndex][:];
    opt["CD"] = opt["CD"][selectedPopIndex][:];
    return opt;
