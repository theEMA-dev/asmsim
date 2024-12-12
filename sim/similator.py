from cpu import CPU

class MIPSSimulator:
    def __init__(self):
        self.cpu = CPU()
    
    def load_assembly_file(self, filename):
        """Load assembly instructions from a file."""
        with open(filename, 'r') as f:
            instructions = f.readlines()
        
        # Clean instructions (remove comments, whitespace)
        cleaned_instructions = []
        for line in instructions:
            # Remove comments and whitespace
            line = line.split('#')[0].strip()
            if line:
                cleaned_instructions.append(line)
        
        return cleaned_instructions
    
    def simulate(self, filename):
        """Simulate a MIPS assembly program."""
        instructions = self.load_assembly_file(filename)
        
        # Run the program
        self.cpu.run_program(instructions)
    
    def print_registers(self):
        """Print the current state of registers."""
        registers = self.cpu.registers
        for i in range(32):
            print(f"{registers.get_register_name(i)}: {registers.read_register(i)}")
    
    def print_memory(self, start=0, end=32):
        """Print a range of memory contents."""
        memory = self.cpu.memory
        
        print("Instruction Memory:")
        for i in range(start, min(end, len(memory.instruction_memory))):
            print(f"Address {i}: {memory.instruction_memory[i]}")
        
        print("\nData Memory:")
        for i in range(start, min(end, len(memory.data_memory))):
            print(f"Address {i}: {memory.data_memory[i]}")

def main():
    simulator = MIPSSimulator()
    
    # Example usage
    try:
        simulator.simulate('./sim/test.asm')
        
        print("Simulation Complete. Register States:")
        simulator.print_registers()
        
        print("\nMemory Contents:")
        simulator.print_memory()
    
    except Exception as e:
        print(f"Error during simulation: {e}")

if __name__ == "__main__":
    main()