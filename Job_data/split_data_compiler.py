import numpy as np
import os
from datetime import datetime

now = datetime.now()
formatted_now = now.strftime('%Y-%m-%d @ %H_%M_%S')

data_path = "./Dirac-Quantum-Walk/Output/Data"
job_name = "Q09S1023P01DsCU00SJS01"
parallel_cache_path = "./Dirac-Quantum-Walk/Output/Parallel_cache/"+job_name+".txt"
data_compiled_path = "/veracruz/projects/c/cquant/Dirac-Quantum-Walk/Output/Data/Data_compiled/"+job_name+" "+ str(formatted_now) + ".txt"




with open(parallel_cache_path,"r") as file:
    job_id_list = file.readlines()
job_id_list = [int(line.rstrip('\n')) for line in job_id_list]


files = sorted(os.listdir(data_path))
#files.sort(key=lambda x: os.path.getmtime(os.path.join(data_path, x)), reverse=True)

with open(data_compiled_path, 'w') as out_file:    
    for file in files:
        try:
            # If the first seven characters can be converted to int and they're in 'lines', open the file
            #print(int(file[:6]))
            if int(file[:6]) in job_id_list:
                #print(int(file[:6]))
                with open(os.path.join(data_path, file), 'r') as f:
                    out_file.write(f.read())
        except ValueError:
            # Continue to the next file if the conversion to int fails
            continue