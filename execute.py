import subprocess
import time
import math

threads = [80]
qubits = [9]
steps = [2**10]#list(range(1,80,2))
partitions = ['cpu1','cpu2', 'hmem1','hmem2','gpu']
precisions = ['double', 'single']  
simulators = ['statevector']#['aer_simulator_statevector','aer_simulator']


partition = partitions[1]
precision = precisions[0]
simulator = simulators[0]
parallel_exps = [1]
batchings = [0]
multiple_circuits = 0 #0 if no (i.e. for individual circuits), 1 if yes
split_circuits_per_cluster_node = 1 #0 -> no (default), 1-> yes,        -SCCN-



"""
For job_size:
if batching = 0, then job_size updates directly on the execute() 

if batching = 1
    job_size = None : batch size is "dynamic"
    job_size = int  : batch size is given by the var job_size
"""

job_sizes= [None] #divisão em batches iguais ou subexeucuts

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
        'memory': '1970M',
        '#CPUS': 48
    },
    'cpu2': {
        'memory': '1100M',
        '#CPUS': 80
    },
    'hmem1': {
        'memory': '4700M',
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
    if variable <0:
        my_string = codification+str(variable)
    elif (variable<10):
        my_string = codification+  "0" + str(variable)
    else:
        my_string = codification+ str(variable)

    return my_string

if split_circuits_per_cluster_node==1:
    multiple_circuits = 0 #force execution of single circuits
    parallel_exps = [1]
    steps = list(range(steps[0]))



for parallel_exp in parallel_exps:
    for batching in batchings:
        for job_size in job_sizes:
            for step in steps:
                for qubit in qubits:
                    for thread in threads:
                        job_name = Teste +  digit_string(qubit,"Q")
                        
                        if split_circuits_per_cluster_node==1:
                            job_name+=digit_string(steps[-1],"S")
                        else:
                            job_name+=digit_string(step,"S")
                        
                        job_name+=digit_string(parallel_exp,"P") + str(precision[0]).upper()

                        if simulator == 'aer_simulator_statevector':
                            job_name += simulator[4]

                        else:
                            job_name += simulator[0]

                        if partition=='gpu':
                            hardware = 'GPU'
                            job_name += "G"
                        else:
                            job_name += "C"
                            hardware = 'CPU'

                        if (batching== 1 and (isinstance(job_size,int))):
                            job_name+=digit_string(job_size,"B") #Batched
                        elif(batching== 1 and (not isinstance(job_size,int))):
                            job_name+=digit_string(0,"B")
                        else:
                            job_name+=digit_string(0,"U") #Unbatched

                        if multiple_circuits==0:
                            job_name+='S'
                        else:
                            job_name+='M'

                        if (job_size==None and multiple_circuits==0):
                            job_name+=digit_string(1,'JS')  
                        elif (job_size==None and multiple_circuits==1):
                            job_name+=digit_string(int(steps[0]),'JS') 
                        else:
                            job_name+=digit_string(job_size,'JS')   
                        
                        job_name_non_divised = job_name   

                        if split_circuits_per_cluster_node==0:
                            job_name+=digit_string(-1,"SCCN_")
                        else:
                            job_name+=digit_string(step,"SCCN_")

                                                

#SBATCH --exclusive
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
srun mprof run --output /veracruz/projects/c/cquant/Dirac-Quantum-Walk/Output/Profiler/Data/${{SLURM_JOB_ID}}.prof python3 /veracruz/projects/c/cquant/Dirac-Quantum-Walk/QuantumWalk/main.py {} {} {} {} {} {} {} {} ${{SLURM_JOB_ID}} {} {} {} {} {} {} {} {}

""".format(partition,job_name, partitions_details[partition]['memory'],thread,qubit,step,coin_type,theta,boundary,dist_boundary,shots,simulator,thread,hardware,precision,parallel_exp,batching,multiple_circuits, job_size,split_circuits_per_cluster_node)


                        # "/veracruz/projects/c/cquant/Dirac-Quantum-Walk/submit__cache.sh"
                        script_filename = "/veracruz/projects/c/cquant/Dirac-Quantum-Walk/submit__cache.sh"
                        with open(script_filename, "w") as file:
                            file.write(bash_execute)

                        # Execute the echo command
                        result = subprocess.run(["sbatch", script_filename], capture_output=True, text=True)



                        if(split_circuits_per_cluster_node==1):
                            job_id = str(result.stdout)[-7:]
                            parallel_cache = "/veracruz/projects/c/cquant/Dirac-Quantum-Walk/Output/Parallel_cache/{}.txt".format(job_name_non_divised)
                            with open(parallel_cache, "a") as file:
                                #file.write("Forced parallization of circuits per cluster nodes")
                                file.write(job_id)

                       

                        if result.returncode == 0:

                            print("\n=*=*=*=*=*=*=*=*=*=*=*=")
                            print("Success job input: " + str(result.stdout))
                            print("== Simulation Data ==")
                            print("Partition: {}".format(partition))
                            print("Job Name: {}".format(job_name))
                            print("Thread: {}".format(thread))
                            print("Qubit: {}".format(qubit))
                            print("Step: {}".format(step))
                            #print("Coin Type: {}".format(coin_type))
                            #print("Theta: {}".format(theta))
                            #print("Boundary: {}".format(boundary))
                            #print("Dist Boundary: {}".format(dist_boundary))
                            #print("Shots: {}".format(shots))
                            print("Simulator: {}".format(simulator))
                            #print("Hardware: {}".format(hardware))
                            print("Precision: {}".format(precision))
                            print("Multiple Circuits: {}".format(multiple_circuits))
                            print("Batching: {}".format(batching))
                            print("max_parallel_experiments: {}".format(parallel_exp))
                            print("max_job_size: {}".format(job_size))
                            print("=*=*=*=*=*=*=*=*=*=*=*=\n\n")
                        else:
                            print("Job upload failed " + str(result.stderr))

                        
                        time.sleep(0.001)
             
