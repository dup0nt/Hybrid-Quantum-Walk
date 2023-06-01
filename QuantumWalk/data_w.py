from common import os, datetime, np

now = datetime.now()
formatted_now = now.strftime('%Y-%m-%d @ %H_%M_%S')

# Define a function to save all_results to a file
def save_results_to_file(all_results, file_path, file_name):
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)

    with open(file_path+file_name, "w") as f:
        #for result in all_results:
            # Write each result as a separate line in the file
        
            # Write each numpy array as a separate line in the file
        np.savetxt(f, all_results)
           
def file_name(num_qubits,num_steps,coin_type,theta,boundry,dist_boundry,shots,job_id,simulator):
    
    if (coin_type==0):
        coin_name = 'H_'
    else:
        coin_name = 'Ry('+ str(theta)+')_'

    if (boundry==0):
        boundry_value = ""
    else:
        boundry_value = "B" + str(dist_boundry) + "_" 

    

    return str(job_id) + "_"  + str(formatted_now) + "__Q" + str(num_qubits) + "_"+ coin_name + "S" + str(num_steps) + "_" + boundry_value + str(shots) + "_" + str(simulator)