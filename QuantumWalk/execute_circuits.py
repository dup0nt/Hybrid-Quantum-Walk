from simulator import choose_backend
from common import np, transpile,execute,QuantumCircuit, plot_histogram,plt

def execute_circuits(circuits_list,shots,simulator,num_threads,parallel_exp,hardware,precision):
    backend = choose_backend(simulator,num_threads,parallel_exp,hardware,precision)
    
    if (simulator=='aer_simulator_statevector'):
        sim_statevector = backend
        circuits_list = transpile(circuits_list, sim_statevector)
        job_statevector = sim_statevector.run(circuits_list, shots=shots)
        answer = job_statevector.result().get_counts()
    
    else:
        job = execute(circuits_list, backend=backend, shots=shots)
        answer = job.result().get_counts()
    
    return answer