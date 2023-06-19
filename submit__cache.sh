#!/bin/bash
# set the partition where the job will run (default = normal)
#SBATCH --partition=cpu2
#SBATCH -A cquant

# set the number of nodes and processes per node
#SBATCH --nodes=1

#SBATCH --ntasks=1

# set name of job
#SBATCH --job-name=TQ06S128s

# set the mem for the whole job
#SBATCH --mem=1190M

# set the number of tasks (processes) per node.
#SBATCH --cpus-per-task=80


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
srun -c $SLURM_CPUS_PER_TASK python /veracruz/projects/c/cquant/Dirac-Quantum-Walk/QuantumWalk/main.py 6 128 1 2 1 2 10000 aer_simulator_statevector ${SLURM_JOB_ID} 80 CPU single

