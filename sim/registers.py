class Registers:
    def __init__(self):
        # Initialize 32 general-purpose registers
        self.registers = [0] * 32
        self.pc = 0  # Program Counter

    def read(self, reg_num):
        """Read a value from a register."""
        return self.registers[reg_num]

    def write(self, reg_num, value):
        """Write a value to a register."""
        self.registers[reg_num] = value

    def update_pc(self, value):
        """Update the program counter."""
        self.pc = value
