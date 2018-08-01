import plot_population
import numpy as np
opt = {}
opt["M"] = 3
opt["pareto"] = np.loadtxt('Pareto Front/C2DTLZ2.3D.pf')
opt["pareto"] = np.loadtxt('Pareto Front/C2DTLZ2.3D.pf')


plot_population.plot_population(opt,opt["pareto"])
