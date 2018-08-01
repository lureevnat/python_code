import nsga2_basic_parameters
import nsga2_main
import calculate_feasible_paretofront
import numpy as np
import plot_population
import math

def main():
    global opt
    test_function = ['zdt1','zdt2','zdt3','zdt4','zdt6', \
                     'dtlz1','dtlz2','dtlz3','dtlz4', 'dtlz5', \
                     'dtlz7','srn','bnh','osy','tnk', \
                     'c2dtlz2', 'DO2DK','DO2DK1',  'DEB2DK','DEB2DK1', \
                     'DEB3DK','DEB3DK1','UF1'];
    #print(type(test_function))
    run = 1
    for func_no in range(15,16,1):
        for r in range(1,run+1,1):
            opt['r'] = r
            print(r)
            opt['objfunction'] = test_function[func_no]
            opt = nsga2_basic_parameters.nsga2_basic_parameters(opt)
            opt["pareto"] = np.loadtxt('Pareto Front/C2DTLZ2.3D.pf')

            #-----------PLOT PARETO FRONT----------------------------------

            plot_population.plot_population(opt,opt["pareto"])



            if r<10:
                opt["objfilename"] = opt["testfilename"]+ '_00' + str(r) + '.obj'
                opt["histfilename"] = opt["testfilename"]+'_00'+str(r)+'.hist'
            elif r<100:
                opt["objfilename"] = opt["testfilename"]+'_0'+str(r)+'.obj'
                opt["histfilename"] = opt["testfilename"]+'_0'+str(r)+'.hist'
            else:
                opt["objfilename"] = opt["testfilename"]+'_'+str(r)+'.obj'
                opt["histfilename"] = opt["testfilename"]+'_'+str(r)+'.hist'
            #---------------- OPTIMIZE ------------------------------------
            opt = nsga2_main.nsga2_main(opt);


            #----------------WRITE TO FILE---------------------------------

            [_, ParetoIndex] = calculate_feasible_paretofront.calculate_feasible_paretofront(opt, opt.pop, opt.popObj, opt.popCV);
            #dlmwrite(opt.objfilename, opt.popObj(ParetoIndex,:), 'delimiter',' ','precision','%.10f');#feasible non-dominated front
            with open('opt["objfilename"]', 'w') as f:
                f.write(opt.popObj[ParetoIndex,:])


            #----------PLOT PARETO FRONT AND FINAL SOLUTION----------------
            plot_population(opt, opt.pareto);
            plot_population(opt, opt.popObj);

            pass
opt = {}
main()  
print("End of Main")   
