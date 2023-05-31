#!/bin/bash
# set the partition where the job will run (default = normal)
#SBATCH --partition=cpu2
#SBATCH -A cquant

# set the number of nodes and processes per node
#SBATCH --nodes=1

# set name of job
#SBATCH --job-name=Q08S512

# set the number of tasks (processes) per node.
#SBATCH --cpus-per-task=80

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
command="python ./QuantumWalk/main.py 8 512 1 2 1 2 10000 ${SLURM_JOB_ID}" 

# Run the command
eval "${command}"

