from simulator import choose_backend
from common import np, transpile,execute,QuantumCircuit, plot_histogram,plt

def execute_circuits(circuits_list,shots,simulator):
    backend = choose_backend(simulator)
    
    if (simulator=='aer_simulator_statevector'):
        sim_statevector = backend
        circuits_list = transpile(circuits_list, sim_statevector)
        job_statevector = sim_statevector.run(circuits_list, shots=shots)
        answer = job_statevector.result().get_counts()
        
    else:  
        job = execute(circuits_list, backend=backend, shots=shots)
        answer = job.result().get_counts()
    
    """
    data_dict = answer

    # Convert binary keys to decimal and store in a new list
    decimal_keys = list(map(lambda x: int(x, 2), data_dict.keys()))
    #decimal_keys = np.array(decimal_keys)-(num_steps)

    # Extract integer values from the dictionary and store in a new list
    integer_values = np.array(list(data_dict.values()))/shots

    results = np.zeros(2**num_qubits,)

    for i,key in enumerate(decimal_keys):
            results[key] = integer_values[i]

    #results[decimal_keys] = integer_values #mais rapido
    """
    return answer