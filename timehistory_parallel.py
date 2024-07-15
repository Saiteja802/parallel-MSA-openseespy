
"-------------------------------- Response history analysis --------------------------------------"
from openseespy.opensees import *
import numpy as np


def RHA(intensity,gmno,saveloc,GMloc):            
    wipe() # wipe previously existing models
    from Canti2DEQ import cantilever_model # read the building model. Using the first earthquake example from OpenSeespy website. Replace with your building model
    cntrl_nodes = cantilever_model()  #  Run the building model with gravity load and damping applied. Set the analysis time to 0.                     
    print ("################################################")
    print("Starting RHA of cantilever column - intensity level - "+str(intensity)+" Ground motion no. - "+str(gmno))
    print ("################################################")
    ts     = np.genfromtxt(GMloc+'/dt.txt')                         # time step of the GM
    gacc   = np.genfromtxt(GMloc+'/gacc_'+str(gmno)+'.txt')            # gacc data 
    dt     = ts[gmno-1]                                            # time step of the GM
    timeSeries('Path',3,'-dt',dt,'-values',*gacc)   # time series
    pattern('UniformExcitation', 3, 1,'-accel', 3)  # acc loading pattern 
    'Acceleration response recorder'
    recorder('Node', '-file', saveloc+"/displacement."+str(gmno)+".out", '-time', '-node'  ,*cntrl_nodes, '-dof',1,'disp')  # dispalcement recorder. Replace with the node numbers and dof of interest based on your model
    recorder('Node', '-file', saveloc+"/acceleration."+str(gmno)+".out",'-timeSeries',3,'-time','-node',*cntrl_nodes,'-dof',1,'accel') # acceleration recorder. Replace with the node numbers and dof of interest based on your model
    wipeAnalysis()		  # clear previously-define analysis parameters    
    # analysis parameters
    system('BandGeneral') # how to store and solve the system of equations in the analysis
    constraints('Plain')  # how it handles boundary conditions
    numberer('Plain')     # Use RCM if the model is complex. This scheme will renumber dof's to minimize stiffness matrix band-width
    algorithm('Linear')	  # use Linear algorithm for linear analysis. DO NOT USE LINEAR ALGORITHM FOR NONLINEAR PROBLEMS
    test('NormUnbalance', 1.0e-3, 500, 0, 0)
    integrator('Newmark',0.5,0.25) # using the newmark's average acceleration scheme (implicit scheme)
    analysis('Transient') # define type of analysis: time-dependent

    for i in range(len(gacc)):
        analyze(1, dt)	  # Run the analysis at a constant time step dt
    wipe()
  
# RHA(1,2,'P:/0_parallel_computing_MSA/'+ 'MSA_results/level_'+str(1),'P:/0_parallel_computing_MSA/'+ 'GMS/level_'+str(1))