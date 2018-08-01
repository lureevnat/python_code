import nsga2_selection
import nsga3_selection
def survival_selection(opt):
    if opt.survivalselectionOption==1:
        #NSGA-II
        opt = nsga2_selection(opt);
    elif opt.survivalselectionOption==2:
        #NSGA-III
        opt = nsga3_selection(opt);
    else:
        print('Survival Selection is not defined');
    return [opt]
