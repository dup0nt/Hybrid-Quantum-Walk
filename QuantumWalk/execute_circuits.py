from simulator import choose_backend
from common import np, transpile,execute,QuantumCircuit, plot_histogram,plt

def subdivide_list(original_list, N):
    return [original_list[i:i+N] for i in range(0, len(original_list), N)]

def batching(circuits_list,job_size=None):
    batch = []
    batch_list = []
    counter = 0


    max_depth = circuits_list[-1].depth()

    if isinstance(job_size,int):
        batch_list = subdivide_list(circuits_list,job_size)
    else:
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

    print(batch_list)
    return batch_list

def batch_execute(circuits_list,shots,simulator,num_threads,parallel_exp,hardware,precision,job_size):
    batch_list = batching(circuits_list,job_size)
    #print(f"My batch list: {batch_list}")
    

    answers_list = []
   
    for batch in batch_list:
        #print(f"My batch: {batch}")
        #print(f"My number of parallel operations: {len(batch)}")
                                                                    #len(batch)
        answer = execute_circuits(batch,shots,simulator,num_threads,parallel_exp,hardware,precision)
        if not isinstance(answer, list):
            answer = [answer]
        print(f"Type(answer): {type(answer)}")
        #answers_list.append(answer)
        answers_list += answer

    return answers_list


def execute_circuits(circuits_list,shots,simulator,num_threads,parallel_exp,hardware,precision,job_size=None):
    backend = choose_backend(simulator,num_threads,parallel_exp,hardware,precision,job_size)
    
    print("== Simulation Data ==")
    print("Len Circuit_list: {}".format(len(circuits_list)))
    print("Simulator: {}".format(simulator))
    print("Shots: {}".format(shots))
    print("Num Threads: {}".format(num_threads))
    print("Parallel Exp: {}".format(parallel_exp))
    print("Hardware: {}".format(hardware))
    print("Precision: {}".format(precision))
    print("Job Size: {}".format(job_size))

    if (simulator=='aer_simulator_statevector'):
        sim_statevector = backend
        circuits_list = transpile(circuits_list, sim_statevector)
        job_statevector = sim_statevector.run(circuits_list, shots=shots)
        answer = job_statevector.result().get_counts()
    
    else:
        job = execute(circuits_list, backend=backend, shots=shots)
        answer = job.result().get_counts()
    
    return answer


