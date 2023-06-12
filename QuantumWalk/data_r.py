import seaborn as sns
#from main import all_results
from common import os, datetime, np, plt


pathe = './Output/Data/'
#file_name = "2023-05-09 @ 11_46_43__Q6_Ry(1)_S128_B15_5000.txt"
#file_path = pathe

quantas = 2

files = sorted(os.listdir(pathe))#, key=os.path.getmtime)
# Choose the bottom 5 files
#bottom_files = files[-quantas:]
bottom_files = files[:quantas]


def build_graph(data,file_name):
    plt.figure()
    ax = sns.heatmap((data))
    ax.set_xlabel('Position')
    ax.set_ylabel('Steps')

    now = datetime.now()
    formatted_now = now.strftime('%Y-%m-%d %H:%M:%S')

    pathe = './Output/Graphs/'
    file_name = pathe + str(file_name)[:-4]+'_heatmap.png'  # You can change this to your desired file name and format (e.g., heatmap.jpg, heatmap.svg)
    plt.savefig(file_name)

# Iterate over the bottom 5 files
for file_name in bottom_files:
    # Construct the full file path
    file_path = os.path.join(pathe, file_name)
    # Check if the file exists and is a file (not a directory)
    if os.path.isfile(file_path):
        # Read in the file using np.loadtxt
        with open(file_path, 'r') as f:
            data = np.loadtxt(f)

    else:
        print(f"Error: {file_path} does not exist.")

    build_graph(data,file_name)
# Reshape the data to the correct shape