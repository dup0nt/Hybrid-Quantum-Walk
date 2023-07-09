from common import Aer
from qiskit_aer import *

def choose_backend (simulator_variable,num_threads,parallel_exp,hardware,precision,job_size):
    
    simulator = Aer.get_backend(simulator_variable)
    simulator = simulator.set_options(#max_job_size=job_size,
                                    max_parallel_threads=num_threads,
                                    max_parallel_experiments=parallel_exp,
                                    #max_parallel_shots=1,
                                    device=hardware,
                                    precision=precision
                                    )
    
    print(f"Simulator: {simulator}")

    return simulator

