import subprocess
import time
import math

threads = [48]
qubits = [6]
steps = [2**7]
partitions = ['cpu1','cpu2', 'hmem1','hmem2','gpu']
precisions = ['double', 'single']  
simulators = ['aer_simulator_statevector','aer_simulator']


partition = partitions[0]
precision = precisions[0]
simulator = simulators[0]
parallel_exp = 48/4

Teste = ""

#tipo de coin:
# 0 -> Hadamard
# 1 -> Ry (for Dirac Evolution)
#       -> theta - define the amount of rotation
coin_type=1
theta=2

#barreiras? ou quantum walk ciclico:
# 0 -> nao
# 1 -> sim
boundary=1

#distância da barreira e do espaço possível:
#-> Nota: ter em atenção a dimensão do espaço, N = 2**num_qubits
dist_boundary=2

#Qasm inputs:
shots=10000

partitions_details = {
    'int': {
        'memory': '1984M',
        '#CPUS': 48
    },
    'vis': {
        'memory': '15976M',
        '#CPUS': 64
    },
    'cpu1': {
        'memory': '1984M',
        '#CPUS': 48
    },
    'cpu2': {
        'memory': '1190M',
        '#CPUS': 80
    },
    'hmem1': {
        'memory': '4800M',
        '#CPUS': 80
    },
    'hmem2': {
        'memory': '21300M',
        '#CPUS': 144
    },
    'gpu': {
        'memory': '1190M',
        '#CPUS': 80
    }
}


#Begin job:
def digit_string(variable, codification):
    if (variable<10):
        my_string = codification+  "0" + str(variable)
    else:
        my_string = codification+ str(variable)

    return my_string

for step in steps:
    for qubit in qubits:
        for thread in threads:
            job_name = Teste +  digit_string(qubit,"Q") + digit_string(step,"S") + digit_string(parallel_exp,"P") + str(precision[0]).upper()
            if simulator == 'aer_simulator_statevector':
                job_name += simulator[4]

            else:
                job_name += simulator[0]

            if partition=='gpu':
                hardware = 'GPU'
                job_name += "G"
            else:
                hardware = 'CPU'
            
            bash_execute = """#!/bin/bash
# set the partition where the job will run (default = normal)
#SBATCH --partition={}
#SBATCH -A cquant

# set the number of nodes and processes per node
#SBATCH --nodes=1

#SBATCH --ntasks=1

# set name of job
#SBATCH --job-name={}

# set the mem for the whole job
#SBATCH --mem-per-cpu={}

# set the number of tasks (processes) per node.
#SBATCH --cpus-per-task={}


# set max wallclock time (in this case 2800 minutes)
#SBATCH --time=2800:00

# err and out job files

# Get the Slurm Job ID
JOB_ID=$SLURM_JOB_ID

# Use OpenMP and set environment variables
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export SLURM_JOB_ID=$SLURM_JOB_ID
export OMPI_MCA_btl="^openib"
export OMPI_MCA_mtl="ofi"

module load Anaconda
source activate cquant_env

# Print the number of tasks per node
echo "number of tasks = $SLURM_NTASKS"
echo "number of cpus_per_task = $SLURM_CPUS_PER_TASK"

# Run the command
srun -c $SLURM_CPUS_PER_TASK python3 /veracruz/projects/c/cquant/Dirac-Quantum-Walk/QuantumWalk/main.py {} {} {} {} {} {} {} {} ${{SLURM_JOB_ID}} {} {} {} {}

""".format(partition,job_name, partitions_details[partition]['memory'],thread,qubit,step,coin_type,theta,boundary,dist_boundary,shots,simulator,thread,hardware,precision,parallel_exp)


            script_filename = "/veracruz/projects/c/cquant/Dirac-Quantum-Walk/submit__cache.sh"
            with open(script_filename, "w") as file:
                file.write(bash_execute)


            # Execute the echo command
            result = subprocess.run(["sbatch", script_filename], capture_output=True, text=True)

            if result.returncode == 0:
                print("Success job input: " + str(result.stdout))
            else:
                print("Job upload failed " + str(result.stderr))

            
            time.sleep(0.1)
            
