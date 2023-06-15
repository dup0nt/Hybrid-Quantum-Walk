import subprocess
import time

threads = [2,4,10]
qubits = [7]
steps = [200]
partitions = ['cpu2', 'hmem1','hmem2','gpu']


partition = partitions[1]

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

#Backend
# 'qasm_simulator'
# 'aer_simulator'
# 'aer_simulator_statevector'
simulator = 'aer_simulator_statevector'

partitions_mem = {
    'int': '96GB',
    'barca': '96GB',
    'vis': '1TB',
    'cpu1': '96GB',
    'cpu2': '96GB',
    'hmem1': '384GB',
    'hmem2': '3TB',
    'gpu': '96GB'
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
            if simulator == 'aer_simulator_statevector':
                job_name = digit_string(qubit,"Q") + digit_string(step,"S") + simulator[4]

            else:
                job_name = digit_string(qubit,"Q") + digit_string(step,"S") + simulator[0]

            if partition=='gpu':
                hardware = 'GPU'
                job_name = job_name + "G"
            else:
                hardware = 'cpu'
            
            bash_execute = """#!/bin/bash
# set the partition where the job will run (default = normal)
#SBATCH --partition={}
#SBATCH -A cquant

# set the number of nodes and processes per node
#SBATCH --nodes=1

# set name of job
#SBATCH --job-name={}

# set the number of tasks (processes) per node.
#SBATCH --cpus-per-task={}
#SBATCH --mem={}
# set max wallclock time (in this case 2800 minutes)
#SBATCH --time=2800:00

# err and out job files

#SBATCH --error=HQW.err
#SBATCH --output=HQW.out

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

command="python /veracruz/projects/c/cquant/Dirac-Quantum-Walk/QuantumWalk/main.py {} {} {} {} {} {} {} {} ${{SLURM_JOB_ID}} {}" 

# Run the command
srun -c $SLURM_CPUS_PER_TASK "${{command}}"

""".format(partition,job_name,thread,partitions_mem[partition],qubit,step,coin_type,theta,boundary,dist_boundary,shots,simulator,thread)


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
