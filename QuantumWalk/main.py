#imports
from quantum_walk import quantum_walk
from execute_circuits import execute_circuits
from data_w import *
from common import sys

print("output", sys.argv)

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

all_results = []

pathe = '/veracruz/projects/c/cquant/Dirac-Quantum-Walk/Output/Data/'
file = file_name(num_qubits,num_steps,coin_type,theta,boundary,dist_boundary,shots,job_id,simulator)

for i in range(num_steps):
    all_results.append(quantum_walk(i,num_qubits,boundary,dist_boundary,coin_type,theta))

exec_answers = execute_circuits(all_results,
                                shots,
                                simulator,
                                num_threads,
                                hardware,
                                precision)

proc_answer = convert_dicts_to_array(exec_answers,shots)
save_results_to_file(proc_answer, pathe, file + ".txt")
    

