import subprocess
import time

threads = [10,20,40,80]
qubits = [5,6,7,8]
steps = [2**7,2**8,2**9]
partitions = ['cpu2', 'hmem1']


partition = partitions[0]

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
            job_name = digit_string(qubit,"Q") + digit_string(step,"S") + simulator[0]

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

# set max wallclock time (in this case 200 minutes)
#SBATCH --time=2800:00

# err and out job files

#SBATCH --error=HQW.err
#SBATCH --output=HQW.out

# Get the Slurm Job ID
JOB_ID=$SLURM_JOB_ID


export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export SLURM_JOB_ID=$SLURM_JOB_ID

module load Anaconda
source activate cquant_env

echo
echo "number of tasks = " $SLURM_NTASKS
echo


# Use variables in a command
command="python /veracruz/projects/c/cquant/Dirac-Quantum-Walk/QuantumWalk/main.py {} {} {} {} {} {} {} {} ${{SLURM_JOB_ID}}" 

# Run the command
eval "${{command}}"

""".format(partition,job_name,thread,qubit,step,coin_type,theta,boundary,dist_boundary,shots,simulator)



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


