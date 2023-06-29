from common import Aer

def choose_backend (simulator_variable,num_threads,parallel_exp,hardware,precision,job_size):
    
    simulator = Aer.get_backend(simulator_variable)
    simulator.set_options(max_job_size=job_size,
                          max_parallel_threads=num_threads,
                          max_parallel_experiments=parallel_exp,
                          device=hardware,
                          precision=precision
                          )
    
    return simulator

