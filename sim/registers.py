class Registers:
    '''
    Registers Component
    Provides a 32-bit MIPS register file implementation with:\n
    - 32 general-purpose registers ($0-$31)\n
    - Program Counter (PC) special register\n
    - Register naming conventions following MIPS architecture\n
    '''
    def __init__(self):
        # 32 general-purpose registers (including $zero)
        self.registers = [0] * 32
        # Special registers
        self.pc = 0  # Program Counter
        
    def reset(self):
        '''Reset Register File State\n
        Initializes all general-purpose registers to 0\n
        Resets program counter (PC) to 0\n
        Returns:\n
            None
        '''
        self.registers = [0] * 32
        self.pc = 0
        
    def read_register(self, register_number):
        '''Read Value from Register\n
        Parameters:\n
            register_number (int): Register number (0-31)\n
        Returns:\n
            int: 32-bit value stored in specified register\n
        Raises:\n
            ValueError: If register_number is outside valid range (0-31)
        '''
        if 0 <= register_number < 32:
            return self.registers[register_number]
        else:
            raise ValueError(f"Invalid register number: {register_number}")
    
    def write_register(self, register_number, value):
        '''Write Value to Register\n
        Parameters:\n
            register_number (int): Register number (0-31)\n
            value (int): 32-bit value to write\n
        Notes:\n
            - Writing to $zero (register 0) is silently ignored\n
            - Values are masked to 32 bits (& 0xFFFFFFFF)\n
        Raises:\n
            ValueError: If register_number is outside valid range (0-31)
        '''
        if 0 <= register_number < 32:
            if register_number != 0:  # Prevent writing to $zero
                self.registers[register_number] = value & 0xFFFFFFFF
        else:
            raise ValueError(f"Invalid register number: {register_number}")
    
    def get_register_name(self, register_number):
        '''Get MIPS Register Name\n
        Converts register number to standard MIPS register name\n
        Parameters:\n
            register_number (int): Register number (0-31)\n
        Returns:\n
            str: Register name (e.g., "$zero", "$t0", "$sp")\n
            "Invalid": If register_number is outside valid range\n
        Register naming follows MIPS conventions:\n
            $0: $zero (constant 0)\n
            $1: $at (assembler temporary)\n
            $2-$3: $v0-$v1 (values)\n
            $4-$7: $a0-$a3 (arguments)\n
            $8-$15: $t0-$t7 (temporaries)\n
            $16-$23: $s0-$s7 (saved)\n
            $24-$25: $t8-$t9 (temporaries)\n
            $26-$27: $k0-$k1 (kernel)\n
            $28: $gp (global pointer)\n
            $29: $sp (stack pointer)\n
            $30: $fp (frame pointer)\n
            $31: $ra (return address)
        '''
        register_names = [
            "$zero", "$at", "$v0", "$v1", "$a0", "$a1", "$a2", "$a3",
            "$t0", "$t1", "$t2", "$t3", "$t4", "$t5", "$t6", "$t7",
            "$s0", "$s1", "$s2", "$s3", "$s4", "$s5", "$s6", "$s7",
            "$t8", "$t9", "$k0", "$k1", "$gp", "$sp", "$fp", "$ra"
        ]
        return register_names[register_number] if 0 <= register_number < 32 else "Invalid"