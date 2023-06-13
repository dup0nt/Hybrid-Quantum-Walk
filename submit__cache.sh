#!/bin/bash
# set the partition where the job will run (default = normal)
#SBATCH --partition=hmem1
#SBATCH -A cquant

# set the number of nodes and processes per node
#SBATCH --nodes=1

# set name of job
#SBATCH --job-name=Q07S500s

# set the number of tasks (processes) per node.
#SBATCH --cpus-per-task=80
#SBATCH --mem=370G
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
command="python /veracruz/projects/c/cquant/Dirac-Quantum-Walk/QuantumWalk/main.py 7 500 1 2 1 2 10000 aer_simulator_statevector ${SLURM_JOB_ID} 80" 

# Run the command
eval "${command}"

