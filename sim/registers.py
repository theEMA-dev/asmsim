class Registers:
    def __init__(self):
        # 32 general-purpose registers (including $zero)
        self.registers = [0] * 32
        # Special registers
        self.pc = 0  # Program Counter
        
    def read_register(self, register_number):
        if 0 <= register_number < 32:
            return self.registers[register_number]
        else:
            raise ValueError(f"Invalid register number: {register_number}")
    
    def write_register(self, register_number, value):
        if 0 <= register_number < 32:
            if register_number != 0:  # Prevent writing to $zero
                self.registers[register_number] = value & 0xFFFFFFFF
        else:
            raise ValueError(f"Invalid register number: {register_number}")
    
    def get_register_name(self, register_number):
        register_names = [
            "$zero", "$at", "$v0", "$v1", "$a0", "$a1", "$a2", "$a3",
            "$t0", "$t1", "$t2", "$t3", "$t4", "$t5", "$t6", "$t7",
            "$s0", "$s1", "$s2", "$s3", "$s4", "$s5", "$s6", "$s7",
            "$t8", "$t9", "$k0", "$k1", "$gp", "$sp", "$fp", "$ra"
        ]
        return register_names[register_number] if 0 <= register_number < 32 else "Invalid"