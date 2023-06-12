from common import np,  execute, QuantumCircuit, QuantumRegister, ClassicalRegister, QFT, plot_histogram, transpile
from coin import build_coin,coin
from shift import shift
from simulator import choose_backend



def quantum_walk(num_steps,num_qubits,boundry,dist_boundry,coin_type,theta):

    position = QuantumRegister(num_qubits, "pos")
    coin_reg = QuantumRegister(1, "coin")
    cr = ClassicalRegister(num_qubits, "register")
    qw = QuantumCircuit(position,coin_reg,cr)

    # create a QFT circuit on 3 qubits
    qft = QFT(num_qubits, inverse=False)

    # apply phase inversions to the QFT circuit to obtain the IQFT
    iqft = QFT(num_qubits, inverse=True)

    initial_pos = np.zeros((2**num_qubits,))
    initial_pos[int(2**num_qubits/2)] = 1

    if (boundry ==0):
        initial_pos = np.fft.fft(initial_pos)
        initial_pos /= np.sqrt(len(initial_pos))

    qw.initialize(initial_pos,position)

    #Start the coin in a even state
    qw.h(num_qubits)
    qw.s(num_qubits)

    my_coins = build_coin(num_qubits,coin_type, theta, boundry)


    for step in range(num_steps):
            coin(qw, num_qubits,boundry,dist_boundry,my_coins[0], my_coins[1], my_coins[2])
            if (boundry==1):
                qw.append(qft, range(num_qubits))
            shift(qw,num_qubits)
            if (boundry==1):
                qw.append(iqft, range(num_qubits))
                
    if (boundry==0):  
        qw.append(iqft, range(num_qubits))
    
    for n in range(num_qubits):
            qw.measure(n,n)

    return qw