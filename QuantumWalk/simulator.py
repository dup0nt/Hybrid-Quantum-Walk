from common import Aer

def choose_backend (simulator_variable):
    
    simulator = Aer.get_backend(simulator_variable)
    simulator.set_options(max_parallel_threads=40,max_parallel_experiments=0)
    
    return simulator

