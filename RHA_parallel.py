
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
    'Displacement and acceleration response recorder'
    recorder('Node', '-file', saveloc+"/displacement."+str(gmno)+".out", '-time', '-node'  ,*cntrl_nodes, '-dof',1,'disp')  # dispalcement recorder at the control nodes
    recorder('Node', '-file', saveloc+"/acceleration."+str(gmno)+".out",'-timeSeries',3,'-time','-node',*cntrl_nodes,'-dof',1,'accel') # total acceleration recorder at the control nodes
    wipeAnalysis()		  # clear previously-define analysis parameters    
    # analysis parameters
    system('BandGeneral') # how to store and solve the system of equations in the analysis
    constraints('Plain')  # how it handles boundary conditions
    numberer('Plain')     # Use RCM if the model is complex. RCM scheme will renumber dof to minimize stiffness matrix band-width
    algorithm('Linear')	  # Use Linear algorithm as this is a linear elastic analysis.
    test('NormUnbalance', 1.0e-3, 500, 0, 0)
    integrator('Newmark',0.5,0.25) # using the Newmark's constant average acceleration scheme (implicit scheme)
    analysis('Transient') # define type of analysis: time-dependent

    for i in range(len(gacc)):
        analyze(1, dt)	  # Run the analysis at a constant time step dt
    wipe()
