#!/bin/bash

# set the partition where the job will run (default = normal)
#SBATCH --partition=cpu2
#SBATCH -A cquant

# set the number of nodes and processes per node
#SBATCH --nodes=1

# set the number of tasks (processes) per node.
#SBATCH --cpus-per-task=80

# set max wallclock time (in this case 200 minutes)
#SBATCH --time=2440:00

# Define variables
# number of qubits highly influences the performance of the simulator
num_qubits=10
num_steps=$((2**12))

#tipo de coin:
# 0 -> Hadamard
# 1 -> Ry (for Dirac Evolution)
#       -> theta - define the amount of rotation
coin_type=1
theta=1

#barreiras? ou quantum walk ciclico:
# 0 -> nao
# 1 -> sim
boundary=1

#distância da barreira e do espaço possível:
#-> Nota: ter em atenção a dimensão do espaço, N = 2**num_qubits
dist_boundary=3

#Qasm inputs:
shots=10000

# set name of job
#SBATCH --job-name=HQW

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL

# send mail to this address
#SBATCH --mail-user=diogo.mfg00@gmail.com

# err and out job files

#SBATCH --error=HQW.err
#SBATCH --output=HQW.out

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

module load Anaconda
source activate cquant_env

echo
echo "number of tasks = " $SLURM_NTASKS
echo


# Use variables in a command
command="python ./QuantumWalk/main.py ${num_qubits} ${num_steps} ${coin_type} ${theta} ${boundary} ${dist_boundary} ${shots}"

# Run the command
eval "${command}"

#python ./QuantumWalk/main.py

#SBATCH sacct -u dgoncalves --format="jobid, jobname, start, end, elapsed, state, averageRSS, exitcode" > ./Output/JobReports.txt

