'Modified MSA parallel example prepared based on https://github.com/luca-s/mpi-master-slave'
from mpi4py import MPI
from mpi_master_slave import Master, Slave
from mpi_master_slave import WorkQueue
import time
import numpy as np
import os

'timehistory_parllel.py is the file to run time history analysis with a function RHA defined inside'
'RHA(k,z) where k is the ground motion number and z is the intensity level'
'make sure the file name is timehistory_parllel.py and the function file inside is named as RHA'
from timehistory_parallel import RHA

'Run the line below in the command prompt'
# mpiexec -np 6 C:/Users/ssi178/AppData/Local/anaconda3/python.exe  P:/0_parallel_computing_MSA/RHA_master_slave.py
# 2 in the code above is the total number of processors available. Do not use a number greater than the total available processors.
# C:/Users/ssi178/AppData/Local/anaconda3/python.exe is the location where the python interpreter is located in my computer. Use a location specific to your computer here.
# P:/0_parallel_computing_MSA/RHA_master_slave.py is the location where the RHA_master_slave.py is located in my computer.  Use a location specific to your computer here.
 

'Inputs'
starting_IL    = 1    # starting intensity level nuber to run in parallel
ending_IL      = 2    # ending intensity level nuber to run in parallel
gms            = 5    # total number of ground motions for each intensity level
curdir         = 'P:/0_parallel_computing_MSA/' # location of the current directory in which the python files are placed
def MSA_saveloc(curdir,z): # location to save MSA results. Change this based on your preference
    return curdir+'MSA_results/level_'+str(z)
def GM_loc(curdir,z): # location of the ground motions. Change this based on your preference
    return curdir+'GMS/level_'+str(z)
# create folders to save results from MSA. Change this based on your preference. 
for z in range(starting_IL,ending_IL+1):
    saveloc = str(MSA_saveloc(curdir,z))
    isFile  = os.path.exists(saveloc)
    if str(isFile) == 'False':           # Directory to store time history analysis results in the y direction
        os.makedirs(saveloc)         

def main():   
    name = MPI.Get_processor_name()
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()
    if rank == 0: # Master
        begin = time.time()
        app = MyApp(slaves = range(1, size))
        app.run(starting_IL, ending_IL, gms,curdir)
        app.terminate_slaves()
        end = time.time()
        print(f"Total runtime of the program is {end - begin}")
    else: # Any slave
        MySlave().run()
    
class MyApp(object):
    """
    This is my application that has a lot of work to do so it gives work to do
    to its slaves until all the work is done
    """
    def __init__(self, slaves):
        # when creating the Master we tell it what slaves it can handle
        self.master = Master(slaves)
        # WorkQueue is a convenient class that run slaves on a tasks queue
        self.work_queue = WorkQueue(self.master)
    def terminate_slaves(self):
        """
        Call this to make all slaves exit their run loop
        """
        self.master.terminate_slaves()
    def run(self, starting_IL, ending_IL, gms,curdir):
        """
        This is the core of my application, keep starting slaves
        as long as there is work to do
        """
        # let's prepare our work queue. This can be built at initialization time
        # but it can also be added later as more work become available       
        for z in range(starting_IL,ending_IL+1):
            for k in range (1,gms+1):
                # 'data' will be passed to the slave and can be anything
                self.work_queue.add_work(data = (k,z, str(MSA_saveloc(curdir,z)), str(GM_loc(curdir,z))))     
        # Keeep starting slaves as long as there is work to do
        while not self.work_queue.done():
            # give more work to do to each idle slave (if any)
            self.work_queue.do_work()
            # reclaim returned data from completed slaves
            for slave_return_data in self.work_queue.get_completed_work():
                done, message, rankno = slave_return_data
                if done:                    
                    print('Processor "%d" - "%s"' % ( rankno, message) )
            # sleep some time
            time.sleep(0)
class MySlave(Slave):
    """
    A slave process extends Slave class, overrides the 'do_work' method
    and calls 'Slave.run'. The Master will do the rest
    """
    def __init__(self):
        super(MySlave, self).__init__()
    def do_work(self, data):
        rank = MPI.COMM_WORLD.Get_rank()
        name = MPI.Get_processor_name()
        gmno, intensity, saveloc, GMloc = data
        RHA(intensity,gmno,saveloc,GMloc)
        return (True, 'Completed ground motion '+str(gmno)+' at level '+str(intensity),rank)

if __name__ == "__main__":
    main()
