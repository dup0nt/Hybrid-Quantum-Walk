#!/bin/bash

#SBATCH --partition=hmem1
#SBATCH -A cquant
#SBATCH --nodes=1
#SBATCH --job-name=_Q07S500s
#SBATCH --cpus-per-task=80
#SBATCH --mem=370G
#SBATCH --time=2800:00
#SBATCH --error=HQW.err
#SBATCH --output=HQW.out

# Get the Slurm Job ID
JOB_ID=$SLURM_JOB_ID

# Use OpenMP and set environment variables
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export SLURM_JOB_ID=$SLURM_JOB_ID
export OMPI_MCA_btl="^openib"
export OMPI_MCA_mtl="ofi"

# Load the Anaconda module and source the cquant_env virtual environment
module load Anaconda
source activate cquant_env

# Print the number of tasks per node
echo "number of tasks = $SLURM_NTASKS"

# Run the Python command with the specified variables in parallel with srun
srun -c $SLURM_CPUS_PER_TASK python /veracruz/projects/c/cquant/Dirac-Quantum-Walk/QuantumWalk/main.py 8 500 1 2 1 2 10000 aer_simulator_statevector $SLURM_JOB_ID 80