import pandas as pd

cache = {}

def read_file(file_name):
    if file_name not in cache:
        with open(file_name, "r") as file:
            cache[file_name] = file.readlines()
    return cache[file_name]

file_name = "/Users/diogogoncalves/Documents/GitProjects/Thesis/Dirac Quantum Walk/Job_data/beta_jobs_results.txt"

data = read_file(file_name)

column_names = data[0].strip().split()  # Apply .strip() and .split() to the column names
data_rows = data[2:]

# Apply .strip() and .split() to each row in data_rows
processed_rows = [row.split() for row in data_rows]

df = pd.DataFrame(processed_rows, columns=column_names)

print(df)