import pol_mut


def mutation(opt):

    if opt.mutationOption==1:
            [opt["popChild"], opt["nrealmut"]] = pol_mut(opt["popChild"], opt["pmut"], opt["nrealmut"],  opt["eta_m"],  opt["bound"][1][:], opt["bound"][2][:] );

    else:
            [opt["popChild"], opt["nrealmut"]] = pol_mut(opt["popChild"], opt["pmut"], opt["nrealmut"],  opt["eta_m"],  opt["bound"][1][:], opt["bound"][2][:] );
    return [opt]
