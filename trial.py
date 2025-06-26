import re

instruction = "RX(1.57) 0;H 0;Z 1;RY(0.8) 2;CX 0 1;"
instructions = instruction.split(';')

for instruction in instructions:
    instruction = instruction.strip()  # Remove any leading/trailing spaces
    if not instruction:  # Skip empty instructions (e.g., from splitting)
        continue

    if '(' in instruction:  # Check if the instruction contains parentheses
        match = re.match(r"([A-Z]+)\(([^)]+)\)\s+(\d+)", instruction)
        if match:
            gate = match.group(1)  # Extract the gate (e.g., "RX")
            angle = float(match.group(2))  # Extract the angle (e.g., 1.57)
            target_qubit = int(match.group(3))  # Extract the target qubit
            print(f"Gate: {gate}, Angle: {angle}, Target Qubit: {target_qubit}")
        else:
            raise ValueError(f"Invalid instruction format: {instruction}")
    else:  # Handle gates without angles
        parts = instruction.split()
        gate = parts[0]  # Extract the gate (e.g., "H", "Z", etc.)
        if len(parts) == 2:  # Single-qubit gate (e.g., "H 0")
            target_qubit = int(parts[1])
            print(f"Gate: {gate}, Target Qubit: {target_qubit}")
        elif len(parts) == 3:  # Two-qubit gate (e.g., "CX 0 1")
            control_qubit = int(parts[1])
            target_qubit = int(parts[2])
            print(f"Gate: {gate}, Control Qubit: {control_qubit}, Target Qubit: {target_qubit}")
        else:
            raise ValueError(f"Invalid instruction format: {instruction}")
