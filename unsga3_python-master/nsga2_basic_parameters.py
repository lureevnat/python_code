import initweight
import numpy as np
import math
import pdb



def nsga2_basic_parameters(opt):
    
    #-----OPTIMIZATION ALGORITHM PARAMETERS-------------------------------
    opt['eta_c'] = 15;#crossover index
    opt['eta_m'] = 20;#mutation index
    opt['G']  = 200;# Generations
    opt['N'] = 200;#population size in optimization algorithm
    opt['pcross'] = 0.9; # Crossover probability
    opt['nrealcross'] = 0;#number of crossover performed
    opt['nrealmut'] = 0;#number of mutation performed
    opt['gen'] = 1;#starting generation
    opt['pop'] = np.array([]);#initial population
    opt['popObj'] = np.array([]);
    opt['Epsilon'] = 1e-14;#numerical difference
    opt['Inf'] = 1e14;#maximum value
    opt['initpopsize'] = opt['N'];#initial sample size for high fidelity computation
           
    opt['crossoverOption'] = 1;# 1 = simulated binary crossover
    opt['mutationOption'] = 1;# 1 = polynomial mutation
    opt['matingselectionOption'] = 1;#1 = binary constraint tournament selection
    opt['survivalselectionOption'] = 2;#1 = NSGA-II, 2 = NSGA-III
    opt['associationsReady'] = False;
    
    if opt['survivalselectionOption']==1:
        opt['algorithm_name'] = 'nsga2';
    else:
        opt['algorithm_name'] = 'nsga3';
    
    
    opt['testfilename'] = opt['algorithm_name']+'_'+opt['objfunction'].lower();
        
    #filename where data will be saved
    opt['varfilename'] = opt['objfunction']+'_var_'+str(opt['r'])+'.txt';#save variables
    opt['objfilename'] = opt['objfunction']+'_obj_'+str(opt['r'])+'.txt';#save objective
    opt['cvfilename']  = opt['objfunction']+'_cv_'+str(opt['r'])+'.txt';#constraint violation
    
    
    #-----OBJECTIVE FUNCTION PARAMETERS------------------------------------
    problem = opt['objfunction'].lower();
    if problem in ['zdt1','zdt2','zdt3','zdt4','zdt6']:
            opt['M']= 2;#number of objectives
            opt['V']= 30;#;10;#number of variables
            opt['C']= 0;#number of constraints
            opt['utopian']= np.array([-0.05, -0.05]);#ideal point, may not be used
            opt['min_val']= np.array([0,0]);#minimum value for normalization, may not be used
            opt['max_val']= np.array([1,1]);#maximum objective, may not be used
            
            if opt['objfunction'] in ['zdt6']:
                opt['min_val']= np.array([0.25,0]);
            elif opt['objfunction'] in ['zdt3']:
                opt['utopian']= np.array([-0.05, -1.1]);
                opt['min_val']= np.array([0,-1]);
                opt['max_val']= np.array([1,1]);
            
            
    elif problem in ['dtlz1', 'dtlz2', 'dtlz3','dtlz4', 'dtlz5', 'dtlz7']:
            opt['M']= 2;
            opt['V']= 11;
            opt['C']= 0;
            opt['utopian']= np.array([ -0.05 * i for i in opt['M']*[1]]);
            opt['min_val']= np.array(opt['M']*[0]);
            opt['max_val']= np.array(opt['M']*[1]);
 
    elif problem in ['wfg1', 'wfg2', 'wfg3','wfg4', 'wfg5', 'wfg6','wfg7','wfg8','wfg9']:
            opt['M']= 3;
            opt['V']= 8; 
            opt['C']= 0;
            opt['utopian']= np.array([ -0.05 * i for i in opt['M']*[1]]);
            opt['min_val']= np.array(opt['M']*[0]);
            opt['max_val']= np.array(opt['M']*[1]);
            
    elif problem in ['uf1', 'uf2', 'uf3','uf4', 'uf5', 'uf6','uf7','uf8','uf9']:
            opt['M']= 2;
            opt['V']= 30; 
            opt['C']= 0;
            opt['utopian']= np.array([ -0.05 * i for i in opt['M']*[1]]);
            opt['min_val']= np.array(opt['M']*[0]);
            opt['max_val']= np.array(opt['M']*[1]);
            
    elif problem in ['do2dk','do2dk1','deb2dk','deb2dk1']:
            opt['M']= 2;
            opt['V']= 30;
            opt['C']= 0;
            opt['utopian']= np.array([ -0.05 * i for i in opt['M']*[1]])
            opt['min_val']= np.array(opt['M']*[0]);
            opt['max_val']= np.array(opt['M']*[1]);
            
    elif problem in ['deb3dk','deb3dk1']:
            opt['M']= 3;
            opt['V']= 30;
            opt['C']= 0;
            opt['utopian']= np.array([-0.05, -0.05, -0.05]);
            opt['min_val']= np.array([0, 0, 0]);

    elif problem in ['c2dtlz2','c3dtlz2']:
            opt['M']= 3;
            opt['V']= 7; 
            
            opt['utopian']= np.array([-0.05, -0.05, -0.05]);
            opt['min_val']= np.array([0, 0, 0]);
            
            if opt['objfunction'] in ['c2dtlz2']:
                opt['C']= 1;
                opt['max_val']= np.array([1,1,1]);
            else:
                opt['C']= 3;
                opt['max_val']= np.array([2.01,2.01, 2.01]);
            
        
    elif problem in ['bnh']:
            opt['M']= 2;
            opt['V']= 2; 
            opt['C']= 2;
            opt['utopian']= np.array([-0.05, -0.05]);
            opt['min_val']= np.array([0, 0]);
            opt['max_val']= np.array([140, 55]);
            
    elif problem in ['osy']:
            opt['M']= 2;
            opt['V']= 6;
            opt['C']= 6;
            opt['utopian']= np.array([-300, 0]);
            opt['min_val']= np.array([-274, 4]);
            opt['max_val']= np.array([-42, 76]);
            
    elif problem in ['srn']:
            opt['M']= 2;
            opt['V']= 2; 
            opt['C']= 2;
            opt['utopian']= np.array([0,-300]);
            opt['min_val']= np.array([0,-250]);
            opt['max_val']= np.array([240,0]);
    elif problem in ['tnk']:
            opt['M']= 2;
            opt['V']= 2; 
            opt['C']= 2;
            opt['utopian']= np.array([-0.001, -0.001]);
            opt['min_val']= np.array([0, 0]);
            opt['max_val']= np.array([1.2, 1.2]);
    elif problem in ['water']:
            opt['M']= 5;
            opt['V']= 3; 
            opt['C']= 7;
            opt['utopian']=np.array([ (-0.05)*i for i in opt['M']*[1] ]);
            opt['min_val']= np.array([0.75, 0, 0, 0, 0]);
            opt['max_val']= np.array([0.95, 0.9, 1.0, 1.6, 3.2]);
    elif problem in ['carside']:
            opt['M']= 3;
            opt['V']= 7; 
            opt['C']= 10;
            opt['utopian']= np.array([24.3180,    3.5352,   10.5610]);
            opt['min_val']= np.array([24.3680,    3.5852,   10.6110]);
            opt['max_val']= np.array([42.7620,    4.0000,   12.5210]);
            
    elif problem in ['welded']:
            opt['M']= 2;
            opt['V']= 4; 
            opt['C']= 4;
            opt['utopian']= np.array([2.3316,   -0.0496]);
            opt['min_val']= np.array([2.3816,    0.0004]);
            opt['max_val']= np.array([36.4403,   0.0157]);           
    else:
            print('Function definition is not found');
    
    
    #--------LOWER AND UPPER BOUND OF DECISION VARIABLE--------------------
    opt['bound'] = np.zeros([2,opt['V']]);
    opt['bound'][1][:] = np.ones([1,opt['V']]);
    
    if(opt['objfunction'] in ['zdt4'.lower()]) :
        opt['bound'][0][1:] = opt['bound'][0,1:]+(-5);
        opt['bound'][1][1:] = opt['bound'][1][1:]*5;
    elif opt['objfunction'] in ['uf1','uf2','uf5','uf6','uf7']:
        opt['bound'][0][1:] = opt['bound'][0][1:]+(-1);
        opt['bound'][1][1:] = opt['bound'][1][1:]*1;
    elif opt['objfunction'] in ['uf4']:
        opt['bound'][0][1:] = opt['bound'][0][1:]+(-2);
        opt['bound'][1][1:] = opt['bound'][1][1:]*2;
    elif opt['objfunction'] in ['uf8','uf9','uf10']:    
        opt['bound'][0][2:] = opt['bound'][0][2:]+(-2);
        opt['bound'][1][2:] = opt['bound'][1][2:]*2;
    elif opt['objfunction'] in ['bnh']:
        opt['bound'][1][0]=5;
        opt['bound'][1][1]=3;
    elif opt['objfunction'] in ['OSY']:
        opt['bound'][1][0]=10;#x1
        opt['bound'][1][1]=10;
        opt['bound'][1][5]=10;
        opt['bound'][0][2]=1;
        opt['bound'][0][4]=1;
        opt['bound'][1][2]=5;
        opt['bound'][1][4]=5;
        opt['bound'][1][3]=6;
    elif opt['objfunction'] in ['srn']:
        opt['bound'][0][0:] = opt['bound'][0][0:]+(-20);
        opt['bound'][1][0:] = opt['bound'][1][0:]*20;
    elif opt['objfunction'] in ['tnk']:
        opt['bound'][1][0:] = opt['bound'][1][0:]*math.pi;
    elif opt['objfunction'] in ['water']:
        opt['bound'][0][0:] = opt['bound'][0][0:]+0.01;
        opt['bound'][1][0] = 0.45;   
        opt['bound'][1][1:] = 0.10; 
    elif opt['objfunction'] in ['carside']:
        opt['bound'][0][0:] = [0.5, 0.45, 0.5, 0.5, 0.875, 0.4, 0.4];
        opt['bound'][1][0:] = [1.5, 1.35, 1.5, 1.5, 2.625, 1.2, 1.2];
    elif opt['objfunction'] in ['welded']:
        opt['bound'][0][0:] = [0.125, 0.1, 0.1, 0.125];
        opt['bound'][1][0:] = [5, 10, 10, 5];
    elif opt['objfunction'] in ['wfg1','wfg2','wfg3','wfg4','wfg5','wfg6','wfg7','wfg8','wfg9']:
        opt['bound'][0][:] = np.zeros((1,opt['V']));
        opt['bound'][1][:] = np.ones((1,opt['V']));
    
    #---------REFERENCE DIRECTION------------------------------------------

    #%% Haitham - Start
    dirCount = math.inf;
    tempN = opt['N'];
    #pdb.set_trace()

    while dirCount > opt['N']:
        opt['dirs']= np.transpose(initweight.initweight(opt['M'], tempN));
        dirCount = opt['dirs'].shape[0];
        tempN = tempN - 1;

    #pdb.set_trace()
    #Haitham - End

#     %Three obj
#     if opt['M']==5
#         opt['dirs']= initweight(5, 210)';
#     elseif opt['M']==3 %Three obj
#         opt['dirs']= initweight(3, 91)';
#     else
#         opt['dirs']= initweight(2, 21)';
#     end

    #initialization
    opt['numdir']= opt['dirs'].shape[0];#number of reference directions
    opt['curdir'] = opt['dirs'][0][:];#current direction
    opt['pmut'] = 1.0/opt['V']; #Mutation probability    
    opt['CD'] = np.zeros((opt['N'],1));#initial crowding distance
    opt['PR'] = np.zeros((opt['N'],1));#initial pagerank for PR
    opt['Color'] = ['k','b','r','g','y',[.5, .6, .7],[.8, .2, .6]]; #Colors
    opt['totalFuncEval'] = opt['N'] * opt['G'];#total number of function evaluation

#------------------------------END OF -FILE--------------------------------

    return(opt)
