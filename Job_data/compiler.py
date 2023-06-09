import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np


file_name = "./Job_data/sacctoutput.csv"
#file_results = "./Dirac Quantum Walk/Output/Data"

df = pd.read_csv(file_name)
df = df[(~df['State'].str.contains('CANCELLED|FAILED|OUT_OF_MEMORY|TIMEOUT|RUNNING')) & (~df['JobID'].str.contains('.extern'))]

df['ShiftedMaxRSS'] = df['MaxRSS'].shift(-1)

df.loc[~df['JobName'].str.contains('.batch'), 'MaxRSS'] = df.loc[~df['JobName'].str.contains('.batch'), 'ShiftedMaxRSS']

df.loc[df['JobName'].str.contains('.batch'), 'MaxRSS'] = None
df = df.drop(columns=['ShiftedMaxRSS'])
df = df[(~df['JobID'].str.contains('.batch'))]

df['qubits'] = df['JobName'].str.extract(r'Q(\d+)S')
df['steps'] = df['JobName'].str.extract(r'S(\d+)[a-zA-Z]')
df['MaxRSS'] = df['MaxRSS'].str.extract(r'(\d+\.\d{2})M').astype(float)
df['qubits'] = df['qubits'].astype(int)
df['steps'] = df['steps'].astype(int)


def time_to_seconds(time_str):
    days = 0
    hours = 0
    minutes = 0
    seconds = 0

    if '-' in time_str:
        days, time_str = time_str.split('-')
        days = int(days)


    time_str = time_str.split('.')[0][:-3] 
    time_parts = time_str.split(':')

    if len(time_parts) == 1:
        seconds = int(time_parts[0])

    elif len(time_parts)== 2:
        minutes = int(time_parts[0])
        seconds = int(time_parts[1])

    else:
        hours = int(time_parts[0])
        minutes = int(time_parts[1])
        seconds = int(time_parts[2])

    total_seconds = (days * 86400) + (hours * 3600) + (minutes * 60) + seconds
    return int(total_seconds)

df['TotalCPU_seconds'] = df['TotalCPU'].apply(time_to_seconds)


def ploter(xaxis, yaxis,hue, dataframe=df, ifqubits=[5,6], ifsteps=[2**7,2**8]):
    if (xaxis not in ('qubits', 'steps', 'AllocCPUS')):
        raise ValueError("Cannot meet conditions for X axis")

    if(yaxis not in ('steps', 'TotalCPU', 'MaxRSS','TotalCPU_seconds')):
        raise ValueError("Cannot meet conditions for Y axis")

    if(hue not in ('steps', 'qubits')):
        raise ValueError("Cannot meet conditions for hue")
    
    if(yaxis == 'TotalCPU'):
        yaxis = 'TotalCPU_seconds'

    if(hue=='qubits'):
        step_value = (ifsteps[0])
        dataframe = dataframe[dataframe['steps'] == (step_value)]

    else:
        qubit_value = (ifqubits[0])
        dataframe = dataframe[dataframe['qubits'] == (qubit_value)]
    
    dataframe = dataframe[dataframe['qubits'].isin(ifqubits)]
    dataframe = dataframe[dataframe['steps'].isin(ifsteps)]
    #dataframe['TotalCPU_seconds'] = dataframe['TotalCPU_seconds'].apply()

    sns.set_style("whitegrid", {"grid.color": "0.9", "grid.linewidth": 0.5, "grid.alpha": 0.5})
    ax = sns.barplot(x=xaxis, y=yaxis, hue=hue, width=0.3, data=dataframe, errorbar=None)

    ax.minorticks_on()
    ax.grid(which='both', axis='y', linestyle=':', linewidth='0.5', color='gray', alpha=0.2)
    print(dataframe)
    plt.show()

ploter('AllocCPUS', 'MaxRSS','qubits')