#imports
from quantum_walk import quantum_walk
from data_w import *
from common import sys



# Retrieve number of qubits and steps from command line arguments
num_qubits = 7
num_steps = 1

# Retrieve coin parameters from command line arguments
coin_type = 1
theta = 2

# Retrieve boundary conditions from command line arguments
boundary = 0
dist_boundary = 1

# Retrieve QASM inputs from command line arguments
shots = 10000

simulator = 'aer_simulator'

job_id = 0000000

all_results = []

pathe = './Dirac-Quantum-Walk/Output/Data/'
file = file_name(num_qubits,num_steps,coin_type,theta,boundary,dist_boundary,shots,job_id,simulator)

for i in range(num_steps):
    all_results.append(quantum_walk(i,num_qubits,shots,boundary,dist_boundary,coin_type,theta,simulator))
    save_results_to_file(all_results, pathe, file + ".txt")
    

