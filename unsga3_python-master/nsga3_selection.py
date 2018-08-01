import numpy as np
import bos
import crowdingDistance
import math
def nsga3_selection(opt):

    [n, _] = opt["totalpopObj"].shape;
    opt.R = np.zeros(  opt["totalpopObj"].shape[1]        ,1);

    selectedPopIndex = [];
    index = opt.totalpopCV<=0;
    FeasiblePopIndex = np.where(index == 1);
    InfeasiblePopIndex = np.where(index == 0);

    #----------------------------------------------------------------------
    #---------Find Non-dominated Sorting of Feasible Solutions If exists---
    #----------------------------------------------------------------------


    #F = cell(n,1);
    F = [[]]*n
    opt.R = np.zeros((n,1));
    if FeasiblePopIndex.size:

        [R,_] = bos(opt["totalpopObj"][FeasiblePopIndex][:]);

        for i in range(1,FeasiblePopIndex.shape[1]):
            F[R(i)] = np.concatenate(F[R(i)], np.transpose(FeasiblePopIndex[i]),axis=1);


    #----------------------------------------------------------------------
    #--If Less #Feasible <N, then we need sort infeasibles to select-------
    #----------------------Don't do niching here---------------------------
    #----------------------------------------------------------------------

    #%% Haitham - Start
    opt["pop2Dir"] = np.zeros((opt["N"], 1));
    opt["pop2DirDistances"] = np.zeros((opt["N"], 1));
    opt["associationsReady"] = False;
    idx = 1;
    #% Haitham

    if FeasiblePopIndex.shape[1]<opt["N"]:

        #-------------Pick all feasible solutions--------------------------
        selectedPopIndex = np.transpose(FeasiblePopIndex);

        #--------------Rank the Infeasible Solutions-----------------------

        if InfeasiblePopIndex.size:

            CV = opt.totalpopCV(InfeasiblePopIndex);
            [_,index] = np.sort(CV);#ascending order

            for i in range(1, index.shape[1]):
                selectedPopIndex = np.concatenate(selectedPopIndex, np.transpose(InfeasiblePopIndex[index[i]]),axis=1);
                if selectedPopIndex.shape[2] >= opt.N:
                    break;

    #----------------------------------------------------------------------
    #--If there are more #Feasibles than we need to select, Do Niching-----
    #----------------------------------------------------------------------

    else:

        #%% Haitham - Start
        opt["associationsReady"] = True;
        # Haitham - End

        #------------------Find Last Front---------------------------------

        count = np.zeros((n,1));
        for i in range(1,n):
            count[i] = F[i].shape[2];

        cd = cumsum(count);
        p1 = np.where(opt.N<cd);
        lastfront = p1(1);

        #-----------Select upto the front before last front----------------

        for i in range(1,lastfront-1):
            selectedPopIndex = np.concatenate(selectedPopIndex, np.transpose(F[i]),axis=1);

        #do a check in to see if N reached

        lastPopIndex = F[lastfront];

        combinedObj = np.concatenate(opt["totalpopObj"][selectedPopIndex][:], opt["totalpopObj"][lastPopIndex][:],axis=0);
        combinePopIndex = np.concatenate(selectedPopIndex, np.transpose(lastPopIndex),axis=1);

        #------------------------------------------------------------------
        #---------------------------FIND INTERCEPT-------------------------
        #------------------------------------------------------------------

        z = min(combinedObj);#find the population minimum
        TranslatedObj = combinedObj - np.tile(z, (combinedObj.shape[1], 1));#recalculate objective according to z

        ASFLines = np.identity(opt["M"]);#ASF direction inclined along each objective
        S = np.zeros((opt["M"], opt["M"]));#To collect the intercept

        for i in range(1,opt["M"]):
            w = ASFLines[i][:];
            w[1:opt["M"]!=i] = 1e-16;
            w = np.divide(w,np.linalg.norm(w));
            [_, index] = min(max(np.divide(TranslatedObj,np.tile(w,TranslatedObj.shape[1],1)),[],2));#finding ASF values with a direction inclined in an objective
            S[i][:] = TranslatedObj[index][:]; #choise the element with smallest asf w.r.t. ASFLines(i,:)

        #----Check if M points doesn't make M-simplex----------------------
        #----It can also happen when size(lastPopIndex,2)<opt.M------------

        if np.linalg.det(S)<1e-16:
            A = max(TranslatedObj,[], 1);
        else:
            b = np.ones((opt.M,1));
            A = np.linsolve((S,b));
            A = np.divide(1,A);
            A = np.transpose(A);

#             if opt["M"]==3: # check intercept
#                 hold all;
#                 xlabel('x')
#                 ylabel('y')
#                 zlabel('z')
#                 box on
#                 grid on
#                 hold on
#                 Intercept = [A(1) 0 0;
#                             0 A(2) 0;
#                             0 0 A(3)];
#                 fill3(Intercept(:,1),Intercept(:,2),Intercept(:,3),'c');
#                 scatter3(S(:,1), S(:,2), S(:,3),'*');
#             end

        #---------------Plot to see if intercept is correct----------------



        #------------------NORMALIZE WITH INTERCEPT------------------------

        NormalizedObj = np.divide(TranslatedObj,np.tile(A,TranslatedObj.shape[1],1));

        #------------------------------------------------------------------
        #-------------------ASSOCIATION------------------------------------
        #------------------------------------------------------------------

        #------------------------------------------------------------------
        #-----For Each Direction select nearest solution for last front----
        #-----For Two cases: Selected fronts, and Last front---------------
        #------------------------------------------------------------------
        #should have been same for all cases

        Count = np.zeros((opt.numdir, 1));

        #----------------for selected indices------------------------------

        tempPopDir = np.zeros(opt.totalpopObj.shape[1], 1);#for each solution save direction
        distance = np.zeros(opt.totalpopObj.shape[1], 1);#for each solution save distance of that direction
        distance[1:] = math.inf;

        for i in range( 1,selectedPopIndex.shape[2]):
            s = selectedPopIndex(i);
            obj = NormalizedObj[np.where(combinePopIndex==s),:];

            for j in range(1,opt.numdir):
                w = opt.dirs[j,:];
                d = np.linalg.norm(obj-((w*np.transpose(obj))*w)/(np.linalg.norm(w)*np.linalg.norm(w)));#remove one '

                if d < distance[s]:
                    tempPopDir[s] = j;
                    distance[s] = d;

            Count[tempPopDir[s]] = Count[tempPopDir[s]]+1;

            #%% Haitham - Start
            opt["pop2Dir"][idx] = tempPopDir[s];
            opt["pop2DirDistances"][idx] = distance[s];
            idx = idx + 1;
            # Haitham - End

        #----------------for last front indices----------------------------
        DirLast = [[]]*opt.numdir;#collect the solutions those prefer this direction
        DirLastDist = [[]]*opt.numdir;#collect the distances
        tempPopDir = np.zeros(opt["totalpopObj"].shape[1], 1);#for each solution save direction
        distance = np.zeros(opt["totalpopObj"].shape[1], 1);#for each solution save distance of that direction
        distance[1:] = math.inf;

        for i in range(1,lastPopIndex.shape[2]):
            s = lastPopIndex(i);
            obj = NormalizedObj[np.where(combinePopIndex==s)][:];#take normalized obj

            for j in range(1,opt["numdir"]):
                w = opt["dirs"][j,:];
                d = np.linalg.norm(obj-((w*np.transpose(obj))*w)/(np.linalg.norm(w)*np.linalg.norm(w)));#remove one '
                if d < distance[s]:
                    tempPopDir[s] = j;
                    distance[s] = d;


            DirLast[tempPopDir(s)] = np.concatenate(DirLast[tempPopDir(s)], np.transpose(s),axis=1);
            DirLastDist[tempPopDir(s)] = np.concatenate(DirLastDist[tempPopDir[s]], np.transpose(distance[s]),axis=1);

        #-------------------NICHING PRESERVATION---------------------------

        for i in range(1,opt["numdir"]):
            [_, I] = np.sort(DirLastDist[i]);
            DirLast[i] = DirLast[i](I);

        while selectedPopIndex.shape[2]<opt.N:

            [p_j, j]=min(Count);

            if DirLast[j].size==0:
                Count[j]=math.inf; #excluded for further consideration

            elif p_j==0:
                selectedPopIndex = np.concatenate(selectedPopIndex, np.transpose(DirLast[j][1]),axis=1);#choose the first

                #%% Haitham - Start
                opt["pop2Dir"][idx] = DirLast[j](1);
                opt["pop2DirDistances"][idx] = DirLastDist[j](1);
                idx = idx + 1;
                #% Haitham - End

                Count[j] = Count[j]+1;
                DirLast[j][1] = [];

            else: #% when p_j>=1
                index = np.random.randint(DirLast[j].shape[2]+1); #chose randomly
                selectedPopIndex = np.concatenate(selectedPopIndex, np.transpose(DirLast[j][index]),axis=1);

                #%% Haitham - Start
                opt["pop2Dir"][idx] = DirLast[j][index];
                opt["pop2DirDistances"][idx] = DirLastDist[j][index];
                idx = idx + 1;
                #% Haitham - End

                DirLast[j][index] = [];
                Count[j] = Count[j]+1;

    #end#if size(FeasiblePopIndex,1)<opt.N

    #---------------Select for Next Generation-----------------------------

    opt["pop"] =  opt["totalpop"][selectedPopIndex][:];
    opt["popObj"] = opt["totalpopObj"][selectedPopIndex][:];
    opt["popCV"] = opt["totalpopCV"][selectedPopIndex][:];
    opt["popCons"] = opt["totalpopCons"][selectedPopIndex][:];
    return opt;
