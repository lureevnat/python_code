import sbx


def crossover(opt):
    if opt.crossoverOption == 1:
            [opt["popChild"], opt["nrealcross"]] = sbx(opt["popChild"], opt["pcross"], opt["nrealcross"], opt["eta_c"], opt["bound"][1][:], opt["bound"][2][:], opt["Epsilon"]);
    else:

            [opt["popChild"], opt["nrealcross"]] = sbx(opt["popChild"], opt.pcross, opt.nrealcross, opt.eta_c, opt["bound"][1][:], opt["bound"][2][:], opt["Epsilon"]);
    return [opt]
