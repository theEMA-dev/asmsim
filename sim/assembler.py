'''
    Assembler Component
    Assembles the MIPS32 Assembly code to Machine code
'''

class Assembler:
    def __init__(self):
        self.current_address = 0
        self.labels = {}
        self.instructions = []
        self.translations = []
        
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
        
        self.opcode_map = {
            'add': 0, 'sub': 0, 'and': 0, 'or': 0, 'slt': 0,
            'sll': 0, 'srl': 0, 'jr': 0,
            'addi': 8, 'lw': 35, 'sw': 43,
            'beq': 4, 'bne': 5,
            'j': 2, 'jal': 3
        }
        
        self.funct_map = {
            'add': 0x20, 'sub': 0x22, 'and': 0x24,
            'or': 0x25, 'slt': 0x2a, 'sll': 0x00,
            'srl': 0x02, 'jr': 0x08
        }

    def is_valid_label(self, label):
        """Check if label contains only valid characters"""
        return all(c.isalnum() or c == '_' for c in label)
    
    def is_valid_instruction(self, instruction):
        """Check if instruction contains only valid characters"""
        valid_chars = set('abcdefghijklmnopqrstuvwxyz$,()0123456789 _-')
        return all(c.lower() in valid_chars for c in instruction)
    
    def first_pass(self, code):
        """First pass: collect all labels and their addresses with validation"""
        self.current_address = 0
        self.labels = {}
        self.instructions = []
        
        for line_num, line in enumerate(code, 1):
            # Split comments
            line = line.split('#')[0].strip()
            if not line:
                continue
            
            # Process labels
            if ':' in line:
                label = line[:line.find(':')].strip()
                if not self.is_valid_label(label):
                    raise SyntaxError(f"Invalid label '{label}' at line {line_num}")
                self.labels[label] = self.current_address * 4
                
                # Process instruction after label
                instruction = line[line.find(':')+1:].strip()
                if instruction:
                    if not self.is_valid_instruction(instruction):
                        raise SyntaxError(f"Invalid instruction '{instruction}' at line {line_num}")
                    self.instructions.append(instruction)
                    self.current_address += 1
            else:
                if not self.is_valid_instruction(line):
                    raise SyntaxError(f"Invalid instruction '{line}' at line {line_num}")
                self.instructions.append(line)
                self.current_address += 1
        
        return self.instructions

    def parse_register(self, reg):
        """Convert register name to number"""
        if reg in self.register_map:
            return self.register_map[reg]
        # Handle numeric register values
        if reg.startswith('$'):
            try:
                num = int(reg[1:])
                if 0 <= num < 32:
                    return num
            except ValueError:
                pass
        raise ValueError(f"Invalid register: {reg}")

    def parse_immediate(self, imm):
        """Parse immediate value"""
        try:
            # Handle hex values
            if imm.startswith('0x'):
                return int(imm, 16)
            # Handle decimal values
            return int(imm)
        except ValueError:
            # Check if it's a label
            if imm in self.labels:
                return self.labels[imm]
            raise ValueError(f"Invalid immediate value: {imm}")

    def assemble_instruction(self, instruction):
        """Assemble a single instruction"""
        parts = instruction.replace(',', ' ').split()
        if not parts:
            return None
            
        opcode = parts[0].lower()
        
        try:
            # R-format instructions
            if opcode in ['add', 'sub', 'and', 'or', 'slt']:
                rd = self.parse_register(parts[1])
                rs = self.parse_register(parts[2])
                rt = self.parse_register(parts[3])
                return (self.opcode_map[opcode] << 26) | (rs << 21) | (rt << 16) | \
                       (rd << 11) | self.funct_map[opcode]
                       
            # Shift instructions
            elif opcode in ['sll', 'srl']:
                rd = self.parse_register(parts[1])
                rt = self.parse_register(parts[2])
                shamt = self.parse_immediate(parts[3])
                return (self.opcode_map[opcode] << 26) | (rt << 16) | \
                       (rd << 11) | (shamt << 6) | self.funct_map[opcode]
                       
            # I-format instructions
            elif opcode in ['addi']:
                rt = self.parse_register(parts[1])
                rs = self.parse_register(parts[2])
                imm = self.parse_immediate(parts[3])
                return (self.opcode_map[opcode] << 26) | (rs << 21) | \
                       (rt << 16) | (imm & 0xFFFF)
                       
            # Memory instructions
            elif opcode in ['lw', 'sw']:
                rt = self.parse_register(parts[1])
                offset_base = parts[2].replace(')', '').split('(')
                offset = int(offset_base[0])
                rs = self.parse_register(offset_base[1])
                return (self.opcode_map[opcode] << 26) | (rs << 21) | \
                       (rt << 16) | (offset & 0xFFFF)
                       
            # Branch instructions
            elif opcode in ['beq', 'bne']:
                rs = self.parse_register(parts[1])
                rt = self.parse_register(parts[2])
                label = parts[3]
                if label in self.labels:
                    # Calculate word offset (divide by 4)
                    offset = (self.labels[label] - (self.current_address * 4 + 4)) // 4
                    return (self.opcode_map[opcode] << 26) | (rs << 21) | \
                           (rt << 16) | (offset & 0xFFFF)
                else:
                    raise ValueError(f"Undefined label: {label}")
                    
            # Jump instructions
            elif opcode in ['j', 'jal']:
                if parts[1] in self.labels:
                    target = self.labels[parts[1]]
                    return (self.opcode_map[opcode] << 26) | target
                else:
                    raise ValueError(f"Undefined label: {parts[1]}")
                    
            # Jump register
            elif opcode == 'jr':
                rs = self.parse_register(parts[1])
                return (self.opcode_map[opcode] << 26) | (rs << 21) | \
                       self.funct_map[opcode]
                       
            else:
                raise ValueError(f"Unknown instruction: {opcode}")
                
        except Exception as e:
            raise ValueError(f"Error assembling instruction '{instruction}': {str(e)}")

    def assemble(self, code):
        """Assemble the complete program"""
        if isinstance(code, str):
            code = code.split('\n')

        self.translations.clear()
        self.first_pass(code)
        
        machine_code = []
        self.current_address = 0
        
        for instruction in self.instructions:
            if instruction.strip():
                mc = self.assemble_instruction(instruction)
                if mc is not None:
                    machine_code.append(mc)
                    self.translations.append(self.translate(mc, instruction))
                    self.current_address += 1
                    
        return machine_code
    
    def translate(self, instruction, original_text):
        """Translate single instruction to machine code formats"""
        # Extract fields
        op = (instruction >> 26) & 0x3F
        rs = (instruction >> 21) & 0x1F
        rt = (instruction >> 16) & 0x1F
        rd = (instruction >> 11) & 0x1F
        shamt = (instruction >> 6) & 0x1F
        funct = instruction & 0x3F
        imm = instruction & 0xFFFF
        addr = instruction & 0x3FFFFFF
    
        # Format binary
        binary = format(instruction, '032b')
        formatted = f"{binary[:6]} {binary[6:11]} {binary[11:16]} {binary[16:21]} {binary[21:26]} {binary[26:]}"
    
        # Determine instruction type
        instr_type = 'R' if op == 0 else 'J' if op in [2, 3] else 'I'
    
        translation = {
            'original': original_text.strip(),
            'type': instr_type,
            'hex': f"0x{instruction:08x}",
            'binary': formatted,
            'fields': {
                'opcode': f"0x{op:02x}",
                'rs': f"${rs}" if instr_type != 'J' else None,
                'rt': f"${rt}" if instr_type != 'J' else None,
                'rd': f"${rd}" if instr_type == 'R' else None,
                'shamt': f"0x{shamt:02x}" if instr_type == 'R' else None,
                'funct': f"0x{funct:02x}" if instr_type == 'R' else None,
                'immediate': f"0x{imm:04x}" if instr_type == 'I' else None,
                'address': f"0x{addr:07x}" if instr_type == 'J' else None
            }
        }
        return translation
    
    def get_translations(self, format_type='all'):
        """Return stored translations in specified format"""
        for line in self.translations:
            all = []
            all.append(line)
        
        if format_type == 'hex':
            return [(t['hex']) for t in self.translations]
        elif format_type == 'binary':
            return [(t['binary']) for t in self.translations]
        else:
            return all