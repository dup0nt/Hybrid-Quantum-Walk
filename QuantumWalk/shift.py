from common import QuantumCircuit, np

def R(j,sinal):
   gate = QuantumCircuit(1, name="R, j="+str(j))
   gate.p(sinal*2*np.pi/pow(2,j), 0)
   return gate.to_gate().control(1)
    

def shift(circ,num_qubits):
    for i in range(num_qubits):
        circ.append(R(num_qubits-i,-1), [num_qubits, i])
        circ.x(num_qubits)
        circ.append(R(num_qubits-i,1), [num_qubits, i])
        circ.x(num_qubits)