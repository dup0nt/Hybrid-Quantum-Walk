from quantum_walk import quantum_walk
from execute_circuits import execute_circuits, batch_execute
from data_w import *
from common import sys

precisions = ['double', 'single']  
precision = precisions[0]

hardware = 'CPU'
num_threads = 0
parallel_exp = 1

batching=1


# Retrieve number of qubits and steps from command line arguments
num_qubits = 5
num_steps = 20

# Retrieve coin parameters from command line arguments
coin_type = 1
theta = 2

# Retrieve boundary conditions from command line arguments
boundary = 0
dist_boundary = 1

# Retrieve QASM inputs from command line arguments
shots = 10000

simulator = 'aer_simulator_statevector'

job_id = 0000000

all_results = []

pathe = './Output/Data/'
file = file_name(num_qubits,num_steps,coin_type,theta,boundary,dist_boundary,shots,job_id,simulator)

for i in range(num_steps):
    all_results.append(quantum_walk(i,num_qubits,boundary,dist_boundary,coin_type,theta))

if(batching==0):

    exec_answers = execute_circuits(all_results,
                                    shots,
                                    simulator,
                                    num_threads,
                                    parallel_exp,
                                    hardware,
                                    precision)
else:
    exec_answers = batch_execute(all_results,
                                shots,
                                simulator,
                                num_threads,
                                hardware,
                                precision)

#proc_answer = convert_dicts_to_array(exec_answers,shots)
#save_results_to_file(proc_answer, pathe, file + ".txt")
