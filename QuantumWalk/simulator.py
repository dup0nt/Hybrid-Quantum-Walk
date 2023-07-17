from common import Aer
from qiskit_aer import *

def choose_backend (simulator_variable,num_threads,max_parallel_experiments,hardware,precision,job_size):
    
    #simulator = Aer.get_backend(simulator_variable)
    
    simulator = AerSimulator(method=simulator_variable)#, precision='double',mps_omp_threads=6)#max_parallel_threads=3,max_parallel_shots=3)#,max_parallel_experiments=0)

    simulator.set_options(precision=precision,
                        max_job_size=job_size,
                        max_parallel_threads=num_threads,
                        max_parallel_experiments=max_parallel_experiments,
                        max_parallel_shots=num_threads,
                        device=hardware,
                        shots=10000
    )
                                   
    
    return simulator

