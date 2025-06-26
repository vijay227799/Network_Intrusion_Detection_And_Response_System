import socket
import os
from qiskit import QuantumCircuit, transpile, assemble
from qiskit_aer import Aer
from qiskit.primitives import Sampler
from qiskit_aer.backends import QasmSimulator
import matplotlib.pyplot as plt

# Server configuration
HOST = 'localhost'
PORT = 12345

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server is listening on {HOST}:{PORT}")

def parse_algorithm_text(text):
    # For simplicity, assume the text contains instructions to add gates.
    # For example: "H 0; CX 0 1; Measure all"
    qc = QuantumCircuit(2)
    instructions = text.split(';')
    for instruction in instructions:
        parts = instruction.strip().split()
        if parts[0] == 'H':
            qc.h(int(parts[1]))
        elif parts[0] == 'CX':
            qc.cx(int(parts[1]), int(parts[2]))
        elif parts[0].lower() == 'measure' and parts[1].lower() == 'all':
            qc.measure_all()
    return qc

def run_quantum_simulation(circuit):
    # Simulate the circuit using Qiskit's Aer simulator
    simulator = QasmSimulator()
    compiled_circuit = transpile(circuit, simulator)
    job = execute(compiled_circuit, simulator, shots=1000)
    result = job.result()
    counts = result.get_counts(circuit)
    
    # Generate a plot of the results
    fig, ax = plt.subplots()
    ax.bar(counts.keys(), counts.values())
    ax.set_xlabel('States')
    ax.set_ylabel('Counts')
    ax.set_title('Quantum Circuit Simulation Results')
    
    # Save the plot as an image
    image_path = 'simulation_results.png'
    plt.savefig(image_path)
    plt.close()
    
    return image_path

while True:
    # Accept a client connection
    client_connection, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    # Receive the HTTP request
    request = client_connection.recv(1024).decode()
    print(f"Request: {request}")

    # Parse the HTTP request
    try:
        file_name = request.split(' ')[1]
        if file_name == '/':
            file_name = '/index.html'
        file_path = '.' + file_name

        # Check if the requested file is /simulate
        if file_name.startswith('/simulate'):
            # Extract the algorithm text from the query parameter
            query = file_name.split('?')[1] if '?' in file_name else ''
            params = dict(param.split('=') for param in query.split('&') if '=' in param)
            algorithm_text = params.get('algorithm', '')

            # Parse and run the quantum algorithm simulation
            circuit = parse_algorithm_text(algorithm_text)
            image_path = run_quantum_simulation(circuit)
            
            # Read the generated image file
            with open(image_path, 'rb') as img_file:
                response_data = img_file.read()
            response_header = 'HTTP/1.1 200 OK\r\n'
            response_header += f'Content-Length: {len(response_data)}\r\n'
            response_header += 'Content-Type: image/png\r\n\r\n'
        elif os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                response_data = file.read()
            response_header = 'HTTP/1.1 200 OK\r\n'
            response_header += f'Content-Length: {len(response_data)}\r\n'
            response_header += 'Content-Type: text/html\r\n\r\n'
        else:
            response_header = 'HTTP/1.1 404 Not Found\r\n'
            response_header += 'Content-Type: text/html\r\n\r\n'
            response_data = b"<html><body><h1>404 Not Found</h1></body></html>"

        # Send the HTTP response
        client_connection.sendall(response_header.encode() + response_data)

    except Exception as e:
        print(f"Error processing request: {e}")

    # Close the client connection
    client_connection.close()
