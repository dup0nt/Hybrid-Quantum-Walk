#!/bin/bash
# set the partition where the job will run (default = normal)
#SBATCH --partition=gpu
#SBATCH -A cquant

# set the number of nodes and processes per node
#SBATCH --gres=gpu:1

#SBATCH --ntasks=1

# set name of job
#SBATCH --job-name=Q09S1024P01DsGU00SJS01SCCN_-1

# set the mem for the whole job
#SBATCH --mem-per-cpu=1190M

# set the number of tasks (processes) per node.
#SBATCH --cpus-per-task=80



# set max wallclock time (in this case 2800 minutes)
#SBATCH --time=2800:00

# out
#SBATCH --output=/veracruz/projects/c/cquant/Dirac-Quantum-Walk/Output/FilesOut/%j.out

# err and out job files
#SBATCH --error=/veracruz/projects/c/cquant/Dirac-Quantum-Walk/Output/FilesErr/%j.err

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
srun mprof run --output /veracruz/projects/c/cquant/Dirac-Quantum-Walk/Output/Profiler/Data/${SLURM_JOB_ID}.prof python3 /veracruz/projects/c/cquant/Dirac-Quantum-Walk/QuantumWalk/main.py 9 1024 1 2 1 2 10000 statevector ${SLURM_JOB_ID} 80 GPU double 1 0 0 None 0

