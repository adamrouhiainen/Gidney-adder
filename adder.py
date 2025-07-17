from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister


def logical_and():
    qc = QuantumCircuit(3, name='AND')

    qc.h(2)
    qc.t(2)
    
    qc.cx(0, 2)
    qc.cx(1, 2)
    qc.cx(2, 1)
    qc.cx(2, 0)
    
    qc.tdg(0)
    qc.tdg(1)
    qc.t(2)
    
    qc.cx(2, 0)
    qc.cx(2, 1)
    
    qc.h(2)
    qc.s(2)

    return qc.to_gate()


def logical_and_dg():
    qc = QuantumCircuit(3, name='AND†')
    
    qc.sdg(2)
    qc.h(2)
    
    qc.cx(2, 1)
    qc.cx(2, 0)
    
    qc.tdg(2)
    qc.t(1)
    qc.t(0)
    
    qc.cx(2, 0)
    qc.cx(2, 1)
    qc.cx(1, 2)
    qc.cx(0, 2)

    qc.tdg(2)
    qc.h(2)
    
    return qc.to_gate()


def gidney_adder(n_bits):
    n_blocks = n_bits - 2
    n_qbits = 3*(n_blocks) + 5
    qc = QuantumCircuit(n_qbits, name='Gidney adder')
    
    # Forward
    # Start
    qc.append(logical_and(), [0, 1, 2])
    
    # Gidney blocks
    for b in range(n_blocks):
        n = 3*b + 2
        qc.cx(n, n+1)
        qc.cx(n, n+2)
        qc.append(logical_and(), [n+1, n+2, n+3])
        qc.cx(n, n+3)
    
    # End
    qc.cx(n_qbits-3, n_qbits-1)
    
    # Reverse
    # Gidney blocks reversed
    for b in reversed(range(1, n_blocks+1)):
        n = 3*b - 1
        qc.cx(n, n+3)
        qc.append(logical_and_dg(), [n+1, n+2, n+3])
        qc.cx(n, n+1)
    qc.append(logical_and_dg(), [0, 1, 2])
    
    # End
    for b in range(n_bits):
        n = 3*b
        qc.cx(n, n+1)

    return qc.to_gate()
