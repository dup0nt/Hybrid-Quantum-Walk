from common import os, datetime, np

now = datetime.now()
formatted_now = now.strftime('%Y-%m-%d @ %H_%M_%S')

def steps_list(num_steps,indicative):
    list_steps = []
    if indicative==0:
        list_steps.append(num_steps)
    else:
        list_steps = range(num_steps)

    return list_steps


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

    

    return str(job_id) + "  "  + str(formatted_now) + "__Q" + str(num_qubits) + "_"+ coin_name + "S" + str(num_steps) + "_" + boundry_value + str(shots) + "_" + str(simulator)


def convert_dicts_to_array(answer, shots):
    # Determine the length of the largest binary key
    max_key_len = max(map(len, answer[0].keys()))

    # Generate an array with the proper size
    num_circuits = len(answer)
    results = np.zeros((num_circuits, 2**max_key_len))

    # Populate the array with the results
    for i in range(num_circuits):
        for key, value in answer[i].items():
            decimal_key = int(key, 2)
            results[i, decimal_key] = value / shots

    return results