 
- Run load_qiskit_account when necessary to load provider
- To export from .ipynb notebook to .py
    jupyter nbconvert --to script your_notebook.ipynb

- Run slurm script:
    sbatch submit_job.sh

- To find position in queue:
    squeue -t PD -S "-p" -o "%.7i %.9P %.30j %.8u %.2t %.19S %.8r" | awk -v jobid=366681 '$1 == jobid { print "Your job is at position " NR " in the queue." }'

- To see jobs list:
    sacct -u dgoncalves --format="jobid, jobname, start, end, elapsed, state, exitcode"

- Launch exclusive job (o not share memory on jobs in the same machine):
    --exclusive

- Obtain info from job:
    seff
    sreport


- Create CSV File (não esquecer de definir o path!):

    sacct --starttime="2023-06-20" --endtime="2024-06-27" --user=dgoncalves --format=JobID,JobName,User,Partition,State,AllocCPUs,Elapsed,MaxRSS,TotalCPU,ReqMem --units=M -P --delimiter=',' > sacctoutput_analysis.csv