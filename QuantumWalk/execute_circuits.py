from simulator import choose_backend
from common import np, transpile,execute,QuantumCircuit, plot_histogram,plt

def batching(circuits_list):
    max_depth = circuits_list[-1].depth()

    batch = []
    batch_list = []
    counter = 0

    for circ in circuits_list:
        counter+=circ.depth()
        if counter<=max_depth+50: #adiciono o +50 para ter alguma margem
            batch.append(circ)

        else:
            batch_list.append(batch)
            counter = circ.depth()
            batch = []
            batch.append(circ)

           # if circ==circuits_list[-1]:
            #    batch_list.append(batch)

    if batch:
            batch_list.append(list(batch))
    return batch_list

def batch_execute(circuits_list,shots,simulator,num_threads,hardware,precision):
    batch_list = batching(circuits_list)
    #print(f"My batch list: {batch_list}")
    
    print(batch_list)

    answers_list = []
    for batch in batch_list:
        #print(f"My batch: {batch}")
        #print(f"My number of parallel operations: {len(batch)}")
        
        answer = execute_circuits(batch,shots,simulator,num_threads,len(batch),hardware,precision)
        answers_list.append(answer)

    return answers_list


def execute_circuits(circuits_list,shots,simulator,num_threads,parallel_exp,hardware,precision,job_size):
    backend = choose_backend(simulator,num_threads,parallel_exp,hardware,precision,job_size)
    
    if (simulator=='aer_simulator_statevector'):
        sim_statevector = backend
        circuits_list = transpile(circuits_list, sim_statevector)
        job_statevector = sim_statevector.run(circuits_list, shots=shots)
        answer = job_statevector.result().get_counts()
    
    else:
        job = execute(circuits_list, backend=backend, shots=shots)
        answer = job.result().get_counts()
    
    return answer


