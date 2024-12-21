class Memory:
    def __init__(self, instruction_memory_size=512, data_memory_size=512):
        self.instruction_memory = [0] * instruction_memory_size
        self.data_memory = [0] * data_memory_size
    
    def load_instruction(self, address, instruction):
        if 0 <= address < len(self.instruction_memory):
            self.instruction_memory[address] = instruction
        else:
            raise ValueError(f"Invalid instruction memory address: {address}")
    
    def get_instruction(self, pc):
        """Get instruction at word-aligned PC address"""
        index = pc // 4  # Convert PC to array index
        if 0 <= index < len(self.instruction_memory):
            return self.instruction_memory[index]
        return 0
    
    def write_word(self, address, value):
        if 0 <= address < len(self.data_memory):
            self.data_memory[address] = value & 0xFFFFFFFF
        else:
            raise ValueError(f"Invalid data memory address: {address}")
    
    def read_word(self, address):
        if 0 <= address < len(self.data_memory):
            return self.data_memory[address]
        else:
            raise ValueError(f"Invalid data memory address: {address}")