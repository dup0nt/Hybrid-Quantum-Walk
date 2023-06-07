import pandas as pd
from matplotlib import pyplot as plt


file_name = "/Users/diogogoncalves/Documents/GitProjects/Thesis/Dirac Quantum Walk/Job_data/sacctoutput.csv"
df = pd.read_csv(file_name)
df = df[(~df['State'].str.contains('CANCELLED|FAILED')) & (~df['JobID'].str.contains('.extern'))]

df['ShiftedMaxRSS'] = df['MaxRSS'].shift(-1)

df.loc[~df['JobName'].str.contains('.batch'), 'MaxRSS'] = df.loc[~df['JobName'].str.contains('.batch'), 'ShiftedMaxRSS']

df.loc[df['JobName'].str.contains('.batch'), 'MaxRSS'] = None
df = df.drop(columns=['ShiftedMaxRSS'])
df = df[(~df['JobID'].str.contains('.batch'))]

df['qubits'] = df['JobName'].str.extract(r'Q(\d+)S')
df['steps'] = df['JobName'].str.extract(r'S(\d+)[a-zA-Z]')
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


    print(time_parts)

    if len(time_parts) == 1:
        seconds = int(time_parts)

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

def ploter(xaxis, yaxis, dataframe=df, ifqubits=6, ifsteps=2**5):
    if (xaxis not in ('qubits', 'steps', 'AllocCPUS')):
        raise ValueError("Cannot meet conditions for X axis")

    if(yaxis not in ('steps', 'TotalCPU', ' MaxRSS')):
        raise ValueError("Cannot meet conditions for Y axis")

    if yaxis=='TotalCPU':
        yaxis = time_to_seconds(yaxis)

    df.plot(x=xaxis,y=yaxis)
    plt.show()

ploter('qubits', 'TotalCPU')
