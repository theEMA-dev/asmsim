import sys
import argparse

# Define constants
REGISTER_COUNT = 32
MEMORY_SIZE = 512

# Global state
registers = [0] * REGISTER_COUNT
memory = [0] * MEMORY_SIZE
program_counter = 0
instructions = []
labels = {}

# Utility functions
def load_program(filename):
    """Load instructions from a file into memory."""
    global instructions, labels
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line_number, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ':' in line:  # Label detection
                label, instr = line.split(':')
                labels[label.strip()] = line_number
                if instr.strip():
                    instructions.append(instr.strip())
            else:
                instructions.append(line)

def display_registers():
    """Display the current state of the registers."""
    print("\nRegisters:")
    for i in range(REGISTER_COUNT):
        print(f"R{i}: {registers[i]}", end='\t')
        if (i + 1) % 4 == 0:
            print()

def display_memory():
    """Display the current state of the memory."""
    print("\nMemory:")
    for i in range(0, MEMORY_SIZE, 16):
        print(f"{i:03x}: ", end='')
        print(' '.join(f"{memory[j]:02x}" for j in range(i, i + 16)))

def execute_instruction(instruction):
    """Decode and execute a single instruction."""
    global program_counter
    print(f"Executing: {instruction}")
    # Tokenize the instruction
    tokens = instruction.split()
    opcode = tokens[0]

    # Implement a subset of MIPS instructions
    if opcode == 'add':
        rd, rs, rt = parse_r_format(tokens)
        registers[rd] = registers[rs] + registers[rt]
    elif opcode == 'sub':
        rd, rs, rt = parse_r_format(tokens)
        registers[rd] = registers[rs] - registers[rt]
    elif opcode == 'lw':
        rt, offset_rs = parse_i_format(tokens)
        offset, rs = offset_rs
        registers[rt] = memory[registers[rs] + offset]
    elif opcode == 'sw':
        rt, offset_rs = parse_i_format(tokens)
        offset, rs = offset_rs
        memory[registers[rs] + offset] = registers[rt]
    elif opcode == 'j':
        target = parse_j_format(tokens)
        program_counter = labels[target] - 1
    else:
        print(f"Unknown instruction: {opcode}")

    program_counter += 1

def parse_r_format(tokens):
    """Parse R-format instruction."""
    rd = int(tokens[1][1:])
    rs = int(tokens[2][1:])
    rt = int(tokens[3][1:])
    return rd, rs, rt

def parse_i_format(tokens):
    """Parse I-format instruction."""
    rt = int(tokens[1][1:])
    offset, rs = tokens[2].split('(')
    offset = int(offset)
    rs = int(rs[1:-1])
    return rt, (offset, rs)

def parse_j_format(tokens):
    """Parse J-format instruction."""
    return tokens[1]

def run():
    """Run the program step-by-step."""
    global program_counter
    while program_counter < len(instructions):
        display_registers()
        display_memory()
        execute_instruction(instructions[program_counter])
        input("Press Enter to continue...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MIPS 32-bit Simulator")
    parser.add_argument('program', help="Path to the MIPS assembly program")
    args = parser.parse_args()

    load_program(args.program)
    try:
        run()
    except KeyboardInterrupt:
        print("\nSimulation terminated.")
