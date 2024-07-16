############################### General Notes: Multiple stripe analysis using OpenSeespy and leader-follower architecture #########################
This document is intended to help users interested in conducting multiple stripe analysis (MSA) using parallel computing. The example code (RHA_master_slave.py) can be used to conduct MSA of a building model using the leader-follower architecture to efficiently run analysis in parallel. 
The following packages are to be installed before running the main file (RHA_master_slave.py) in the command line:
1. Install mpiexec using the following link
	* https://learn.microsoft.com/en-us/message-passing-interface/microsoft-mpi?redirectedfrom=MSDN#ms-mpi-source-code
2. Install Openseespy and python packages for parallel computing (py-3.8 – m implies python version 3.8. Replace with whatever version is installed on your PC).
	• py -3.8 -m pip install openseespy
	• py -3.8 -m pip install mpi4py
	• py -3.8 -m pip install mpi_master_slave
Note1: Message Passing Interface (MPI) is a standardized and portable way for computers to communicate with each other when working together on a task. pip install mpi4py installs this package for python. 
Note2: Leader-follower architecture is a dynamic load balancing scheme to efficiently improve the efficiency of parallel computing. mpi_master_slave installs this package for python. This package was previously developed by Luca Scarabello, Landon T. Clipp (https://github.com/luca-s/mpi-master-slave). It has been modified to run MSA using OpenSeespy. Details of this package and some example applications are in the original GitHub page:
 More basic information about the leader-follower architecture can be found at: 
•	https://www.geeksforgeeks.org/master-slave-architecture/ 
•	https://medium.com/@cpsupriya31/understanding-master-slave-architecture-uses-and-challenges-2acc907de7c4  


#######################################################################################################################################################################################
Instrcutions to use the code:
1. Step 1: Prepare the required files to conduct MSA using your model. The required files are:
	* Canti2DEQ.py 
		# This is an example linear elastic cantilever example from the OpenSeespy website (https://openseespydoc.readthedocs.io/en/latest/src/Canti2DEQ.html). 
		# Replace this with your building model, with the gravity load  and damping applied. 
		# return a list of nodes (cntrl_nodes) at which the displacement and acceleration time histories are supposed to be recorded. 
	* timehistory_parallel.py
		# This file has the commands to conduct response history analysis of your building subjected to a ground motion time history.
		# inputs to this file are the intensity level (intensity), ground motion number (hmno), and the folder to save the MSA results (GMloc). The results include displacement and acceleration 		                          	   response histories at the cantilever tip. The files to be saved can be modified based on your preference.
	* RHA_master_slave.py
		# This file employs the leader-follower architecture to coduct MSA of your model in parallel.

Details about timehistory_parallel.py:
	* The building model defined in Canti2DEQ.py file is imported in line 9 and 10.
	* Example ground motions at different intensity levels are placed in the folder GMS. Inside the GMS folder, level_1 and level_2 contain ground motions at two intensity levels and also the respective 	   	   recording time steps of the ground motions are in the file named DT. The acceleration data is in incg/sec^2 (as the example cantilevel model uses inches as the units for length). Replace these files based on 	   	   your intensity levels and the ground motions selected at these levels. Make sure the acceleration and DT file formats are similar to the ones in this example.
	* Based on the intensity, gmno, and GMloc inputs, the time step and ground acceleration data are loaded in lines 14, 15, 16.
	* Based on the specified cntrl_nodes (from cantilever_model), acceleration and displacement time histories are recorded in lines 20 and 21. Here is a good place to add any additional recorders based                         	   on your requirements.
	* Change the analysis parameters based on your requirements. DO NOT USE LINEAR ALGORITHM FOR NONLINEAR ANALYSIS USING IMPLICIT SCHEMES.

Details about RHA_master_slave.py:
	* timehistory_parallel.py file is loaded and the function RHA is imported in line 12.
	* Line 22 to 25 are the required inputs. 
	* MSA_saveloc (line 26) returns the directory where the GMS are placed. Replace based on your requirements (or just use this format)
	*  GM_loc (line 28) returns the directory where the MSA results will be saved.
	* The directory to save MSA results is created in lines 31 to 35.
### Note: Read through https://github.com/luca-s/mpi-master-slave to understand the functioning of the leader-follower algorithm.
	* Inputs to the leader processor (rank == 0) are provided in line 45.
	* Same inputs to the leader processor are again provided in line 66.
	* The list of jobs are created in line 76. Modify this based on your requirements (i.e. if you want to run multiple models)
	* The inputs to each follower processor are provided by the leader in line 98.
	* Call in the RHA function file to provide the inputs and start a response history analysis (line 99).
	* Message to be printed after the analysis is returned in line 100.

RUN PARALLEL MSA USING OPENSEESPY
Run the RHA_master_slave.py in the command line using the command below:
	*  mpiexec -np 2 C:/Users/ssi178/AppData/Local/anaconda3/python.exe  P:/0_parallel_computing_MSA/RHA_master_slave.py
		# 2 in the code above is the total number of processors available. Do not use a number greater than the total available processors.
		# C:/Users/ssi178/AppData/Local/anaconda3/python.exe is the location where the python interpreter is located in my computer. Use a location specific to your computer here.
		# P:/0_parallel_computing_MSA/RHA_master_slave.py is the location where the RHA_master_slave.py is located in my computer.  Use a location specific to your computer here.
