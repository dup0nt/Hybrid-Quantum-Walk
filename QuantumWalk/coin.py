# Import libraries from common.py
from common import np, QuantumCircuit
from common import np

#from main import boundry, coin_type, theta, dist_boundry

# Your code here


#Coin "principal"
num_qubits_coin = 1

def build_coin(num_qubits,coin_type,theta,boundry):
    sig_circ = QuantumCircuit(1, name="coin")
    if (coin_type == 0):
        sig_circ.h(0)
    else:
        sig_circ.ry(theta, 0)

    if (boundry == 0):
        sig = sig_circ.to_gate()
    else:   
        sig = sig_circ.to_gate().control(num_qubits)

    #Coin para o limite do lado Esquerdo
    sig_left = QuantumCircuit(1, name="coin_L")
    #quando chega ao limite da esquerda |000>, tem de andar para a direita!!!
    sig_left.x(0)
    sig_left = sig_left.to_gate().control(num_qubits)

    #Coin para o limite do lado Direito
    sig_right = QuantumCircuit(1, name="coin_R")
    #quando chega ao limite da direita |111>, tem de andar para a esquerda!!!
    sig_right.x(0)
    sig_right = sig_right.to_gate().control(num_qubits)

    return [sig_left, sig,sig_right]

def coin(qw, num_qubits, boundry, dist_boundry, sig_left, sig, sig_right):
    append_vector = list(range(num_qubits+1))
    
    
    if (boundry == 0):
        qw.append(sig,[num_qubits])

    else:
        #condição para aplicar x gates
        for i in range(2**num_qubits):
            #condição para avançar nas diferentes posições
            for ancilla in range(num_qubits):
                if (np.mod(i,2**ancilla))==0:
                    qw.x(ancilla)

            #condicao para avancar nas diferentes coin para cada posicao

            #lmite do lado esquerdo
            if (i==dist_boundry):
                qw.append(sig_left,append_vector)

            #lmite do lado direito
            elif (i==(2**num_qubits-dist_boundry+1)):
                qw.append(sig_right,append_vector)

            else:
                qw.append(sig,append_vector)
