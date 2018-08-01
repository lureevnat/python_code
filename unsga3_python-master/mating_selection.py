import constrained_tournament_selection
import niching_based_tournament_selection

def mating_selection(opt):

    if opt.survivalselectionOption == 1:
            opt.popChild = constrained_tournament_selection(opt, opt["pop"], opt["popObj"], opt["popCV"]);
    elif opt.survivalselectionOption == 2:
            opt.popChild = niching_based_tournament_selection(opt, opt["pop"], opt["popObj"], opt["popCV"]);
    else:
            opt.popChild = constrained_tournament_selection(opt, opt["pop"], opt["popObj"], opt["popCV"]);
    return [opt]
