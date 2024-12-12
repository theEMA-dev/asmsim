class Assembler:
    def __init__(self):
        # Opcode and function code mappings
        self.opcode_map = {
            'add': 0b000000,  # R-type
            'sub': 0b000000,
            'and': 0b000000,
            'or': 0b000000,
            'slt': 0b000000,
            'sll': 0b000000,
            'srl': 0b000000,
            'addi': 0b001000,
            'lw': 0b100011,
            'sw': 0b101011,
            'beq': 0b000100,
            'bne': 0b000101,
            'j': 0b000010,
            'jal': 0b000011
        }
        
        self.funct_map = {
            'add': 0b100000,
            'sub': 0b100010,
            'and': 0b100100,
            'or': 0b100101,
            'slt': 0b101010,
            'sll': 0b000000,
            'srl': 0b000010
        }
        
        # Mapping of register names to their numbers
        self.register_map = {
            '$zero': 0, '$at': 1, '$v0': 2, '$v1': 3,
            '$a0': 4, '$a1': 5, '$a2': 6, '$a3': 7,
            '$t0': 8, '$t1': 9, '$t2': 10, '$t3': 11, 
            '$t4': 12, '$t5': 13, '$t6': 14, '$t7': 15,
            '$s0': 16, '$s1': 17, '$s2': 18, '$s3': 19, 
            '$s4': 20, '$s5': 21, '$s6': 22, '$s7': 23,
            '$t8': 24, '$t9': 25, '$k0': 26, '$k1': 27,
            '$gp': 28, '$sp': 29, '$fp': 30, '$ra': 31
        }
    
    def _parse_register(self, reg_str):
        """Parse register string to its numeric value."""
        # Remove '$' if present and convert to lowercase
        reg_name = reg_str.lower()
        if reg_name.startswith('$'):
            reg_name = reg_name[1:]
        
        # Try direct numeric lookup first
        try:
            # Check if it's a direct numeric register number
            reg_num = int(reg_name)
            if 0 <= reg_num < 32:
                return reg_num
        except ValueError:
            # If not a number, look up in register map
            full_reg_name = f'${reg_name}'
            if full_reg_name in self.register_map:
                return self.register_map[full_reg_name]
        
        raise ValueError(f"Invalid register: {reg_str}")
    
    def assemble(self, instruction):
        """Convert assembly instruction to machine code."""
        # Remove commas and split instruction
        parts = instruction.replace(',', '').split()
        opcode = parts[0].lower()
        
        if opcode in ['add', 'sub', 'and', 'or', 'slt', 'sll', 'srl']:
            return self._assemble_r_type(instruction)
        elif opcode in ['addi', 'lw', 'sw', 'beq', 'bne']:
            return self._assemble_i_type(instruction)
        elif opcode in ['j', 'jal']:
            return self._assemble_j_type(instruction)
        else:
            raise ValueError(f"Unsupported instruction: {instruction}")
    
    def _assemble_r_type(self, instruction):
        """Assemble R-type instructions."""
        parts = instruction.replace(',', '').split()
        opcode = parts[0].lower()
        
        # Handle special case for shift instructions
        if opcode in ['sll', 'srl']:
            rd = self._parse_register(parts[1])
            rt = self._parse_register(parts[2])
            shamt = int(parts[3])
        else:
            rd = self._parse_register(parts[1])
            rs = self._parse_register(parts[2])
            rt = self._parse_register(parts[3])
            shamt = 0
        
        instruction_bits = (
            (self.opcode_map[opcode] << 26) |  # Opcode (6 bits)
            ((rs if opcode not in ['sll', 'srl'] else 0) << 21) |  # Rs (5 bits)
            (rt << 16) |                       # Rt (5 bits)
            (rd << 11) |                       # Rd (5 bits)
            (shamt << 6) |                     # Shamt (5 bits)
            self.funct_map[opcode]             # Function code (6 bits)
        )
        
        return instruction_bits
    
    def _assemble_i_type(self, instruction):
        """Assemble I-type instructions."""
        parts = instruction.replace(',', '').split()
        opcode = parts[0].lower()
        
        if opcode in ['lw', 'sw']:
            rt = self._parse_register(parts[1])
            offset_and_base = parts[2].split('(')
            offset = int(offset_and_base[0])
            rs = self._parse_register(offset_and_base[1][:-1])
        else:
            rt = self._parse_register(parts[1])
            rs = self._parse_register(parts[2])
            offset = int(parts[3])
        
        instruction_bits = (
            (self.opcode_map[opcode] << 26) |  # Opcode (6 bits)
            (rs << 21) |                       # Rs (5 bits)
            (rt << 16) |                       # Rt (5 bits)
            (offset & 0xFFFF)                  # Immediate/Offset (16 bits)
        )
        
        return instruction_bits
    
    def _assemble_j_type(self, instruction):
        """Assemble J-type instructions."""
        parts = instruction.split()
        opcode = parts[0].lower()
        target = int(parts[1])
        
        instruction_bits = (
            (self.opcode_map[opcode] << 26) |  # Opcode (6 bits)
            (target & 0x3FFFFFF)               # Target address (26 bits)
        )
        
        return instruction_bits