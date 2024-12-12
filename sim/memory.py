class Memory:
    def __init__(self, instruction_memory_size=512, data_memory_size=512):
        # Instruction Memory
        self.instruction_memory = [0] * instruction_memory_size
        
        # Data Memory
        self.data_memory = [0] * data_memory_size
    
    def load_instruction(self, address, instruction):
        """Load an instruction into instruction memory."""
        if 0 <= address < len(self.instruction_memory):
            self.instruction_memory[address] = instruction
        else:
            raise ValueError(f"Invalid instruction memory address: {address}")
    
    def get_instruction(self, address):
        """Retrieve an instruction from instruction memory."""
        if 0 <= address < len(self.instruction_memory):
            return self.instruction_memory[address]
        else:
            raise ValueError(f"Invalid instruction memory address: {address}")
    
    def write_word(self, address, value):
        """Write a 32-bit word to data memory."""
        if 0 <= address < len(self.data_memory):
            self.data_memory[address] = value & 0xFFFFFFFF  # 32-bit mask
        else:
            raise ValueError(f"Invalid data memory address: {address}")
    
    def read_word(self, address):
        """Read a 32-bit word from data memory."""
        if 0 <= address < len(self.data_memory):
            return self.data_memory[address]
        else:
            raise ValueError(f"Invalid data memory address: {address}")