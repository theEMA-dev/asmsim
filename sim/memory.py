'''
    Memory Component
    Provides Immediate and Data Memory to SIM component
'''

class Memory:
    def __init__(self):
        self.INSTRUCTION_MEMORY_SIZE = 512
        self.DATA_MEMORY_SIZE = 512
        self.reset()
    
    def reset(self):
        self.instruction_memory = [0] * (self.INSTRUCTION_MEMORY_SIZE // 4)
        self.data_memory = [0] * (self.DATA_MEMORY_SIZE // 4)
        
    def read_instruction_memory(self):
        return self.instruction_memory
    
    def read_data_memory(self):
        return self.data_memory
    
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
        """Write a word to data memory at word-aligned address"""
        if (address % 4) != 0:
            raise ValueError(f"Memory Access Error: Unaligned adress {address}")
        if 0 <= address < len(self.data_memory) * 4:  # Check byte address
            word_index = address // 4  # Convert byte address to word index
            self.data_memory[word_index] = value & 0xFFFFFFFF
        else:
            raise ValueError(f"Memory Access Error: Invalid adress {address}")
    
    def read_word(self, address):
        """Read a word from data memory at word-aligned address"""
        if (address % 4) != 0:
            raise ValueError(f"Memory Access Error: Unaligned adress {address}")
        if 0 <= address < len(self.data_memory) * 4:  # Check byte address
            word_index = address // 4  # Convert byte address to word index
            return self.data_memory[word_index]
        else:
            raise ValueError(f"Memory Access Error: Invalid adress {address}")