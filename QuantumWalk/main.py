#imports
from quantum_walk import quantum_walk
from execute_circuits import execute_circuits, batch_execute
from data_w import *
from common import sys

print("output", sys.argv)
#print(f"Qubits: {sys.argv[1]}, Steps: {sys.argv[2]}, coin_type: {sys.argv[3]}, theta: {sys.argv[1]}, boundary: {sys.argv[1]}, simulator: {sys.argv[1]}, shots: {sys.argv[1]}, theta: {sys.argv[1]}")
# Retrieve number of qubits and steps from command line arguments
num_qubits = int(sys.argv[1])
num_steps = int(sys.argv[2])

# Retrieve coin parameters from command line arguments
coin_type = int(sys.argv[3])
theta = int(sys.argv[4])

# Retrieve boundary conditions from command line arguments
boundary = int(sys.argv[5])
dist_boundary = int(sys.argv[6])

# Retrieve QASM inputs from command line arguments
shots = int(sys.argv[7])
simulator = str(sys.argv[8])
job_id = int(sys.argv[9])
num_threads =int(sys.argv[10])
hardware = str(sys.argv[11])
precision = str(sys.argv[12])
parallel_exp = int(sys.argv[13])
batching = int(sys.argv[14])
multiple_circuit = int(sys.argv[15])
job_size = (sys.argv[16])

# Check if the input value is an integer or None
if job_size is not None and job_size.isdigit():
    # Convert the input value to an integer
    job_size = int(job_size)
else:
    # Handle the case when the input value is None or not a valid integer
    job_size = None

all_results = []

pathe = '/veracruz/projects/c/cquant/Dirac-Quantum-Walk/Output/Data/'
file = file_name(num_qubits,num_steps,coin_type,theta,boundary,dist_boundary,shots,job_id,simulator)

steps = steps_list(num_steps,multiple_circuit)

for i in steps:
    all_results.append(quantum_walk(i,num_qubits,boundary,dist_boundary,coin_type,theta))

if(batching==0):

    exec_answers = execute_circuits(all_results,
                                    shots,
                                    simulator,
                                    num_threads,
                                    parallel_exp,
                                    hardware,
                                    precision,
                                    job_size)
else:
    exec_answers = batch_execute(all_results,
                                shots,
                                simulator,
                                num_threads,
                                parallel_exp,
                                hardware,
                                precision,
                                job_size)

#proc_answer = convert_dicts_to_array(exec_answers,shots,multiple_circuit)
#save_results_to_file(proc_answer, pathe, file + ".txt")