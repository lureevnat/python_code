import lhsamp_model
import evaluate_pop
import evaluateCV
import plot_population
import mating_selection
import crossover
import mutation
import survival_selection
import os
import numpy as np

def nsga2_main(opt):
    #------------INITIALIZE------------------------------------------------
    opt["pop"] = lhsamp_model.lhsamp_model(opt["N"], opt);#LHS Sampling

    #------------EVALUATE--------------------------------------------------
    [opt["popObj"], opt["popCons"]] = evaluate_pop.evaluate_pop(opt, opt["pop"]);
    opt["popCV"] = evaluateCV.evaluateCV(opt["popCons"]);
    opt["archiveObj"] = opt["popObj"];#to save all objectives
    opt["archive"] = opt["pop"];
    opt["archiveCV"] = opt["popCV"];

    #-------------------PLOT INITIAL SOLUTIONS-----------------------------
    plot_population(opt, opt["popObj"]);

    if os.path.isfile(opt["histfilename"]):
        os.remove(opt["histfilename"])

    # if exist(opt["histfilename"], 'file')==2:
    #     delete(opt["histfilename"]);

    #--------------- OPTIMIZATION -----------------------------------------
    funcEval = opt["N"];

    while funcEval < opt["totalFuncEval"] : # Generation # 1 to

        M1 = np.tile(funcEval, opt["N"], 1);
        M2 = opt["pop"];
        M3 = opt["popObj"];
        M4 = (-1)*opt["popCV"];
        M = np.concatenate(M1, M2, M3, M4,axis=1);

        #dlmwrite(opt.histfilename, M, '-append', 'delimiter',' ','precision','%.10f');%history of run
        opt = mating_selection(opt);#--------Mating Parent Selection-------
        opt = crossover(opt);#-------------------Crossover-----------------
        opt = mutation(opt);#--------------------Mutation------------------


        #---------------EVALUATION-----------------------------------------
        [opt["popChildObj"], opt["popChildCons"]] = evaluate_pop(opt, opt["popChild"]);
        opt["popCV"] = evaluateCV(opt["popCons"]);
        opt["popChildCV"] = evaluateCV(opt["popChildCons"]);



        #---------------MERGE PARENT AND CHILDREN--------------------------
        opt["totalpopObj"] = np.concatenate(opt["popChildObj"], opt["popObj"]);
        opt.totalpop = np.concatenate(opt["popChild"], opt["pop"]);
        opt.totalpopCV = np.concatenate(opt["popChildCV"], opt["popCV"]);
        opt.totalpopCons = np.concatenate(opt["popChildCons"], opt["popCons"]);

        #-----------------SURVIVAL SELECTION-------------------------------
        opt = survival_selection(opt);
        funcEval = funcEval + opt.N;

        opt.popCV = evaluateCV(opt["popCons"]);
        opt.archive = np.concatenate(opt["archive"],opt["pop"]);
        opt.archiveObj = np.concatenate(opt["archiveObj"],opt["popObj"]);
        opt.archiveCV = np.concatenate(opt["archiveCV"],opt["popCV"]);


        #-------------------PLOT NEW SOLUTIONS-----------------------------

        if funcEval%1000==0:
            print(funcEval);
            plot_population(opt, opt["popObj"]);
        #[opt.FeasibleIndex, opt.ParetoIndex] = calculate_feasible_paretofront(opt, opt.archive, opt.archiveObj, opt.archiveCV);

    M1 = np.concatenate(funcEval, opt["N"], 1,axis=1);
    M2 = opt.pop;
    M3 = opt.popObj;
    M4 = (-1)*opt.popCV;
    M = np.concatenate(M1, M2, M3, M4,axis=1);

    with open('opt["histfilename"]', 'w') as f:
                f.write(M)
    # dlmwrite(opt.histfilename, M, '-append', 'delimiter',' ','precision','%.10f');#history of run

    return opt;
#------------------------------END OF -FILE--------------------------------

