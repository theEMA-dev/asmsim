from registers import Registers
from memory import Memory
from instructions import Instructions
from assembler import Assembler

class CPU:
    def __init__(self):
        self.registers = Registers()
        self.memory = Memory()
        self.instructions = Instructions()
        self.assembler = Assembler()
        
    def fetch(self):
        """Fetch instruction from memory."""
        instruction = self.memory.get_instruction(self.registers.pc)
        self.registers.pc += 1
        return instruction
    
    def decode(self, instruction):
        """Decode instruction and return its components."""
        # Extract opcode (6 bits)
        opcode = (instruction >> 26) & 0b111111
        
        # Extract basic register components
        rs = (instruction >> 21) & 0b11111
        rt = (instruction >> 16) & 0b11111
        rd = (instruction >> 11) & 0b11111
        
        # Extract function code for R-type
        funct = instruction & 0b111111
        
        # Extract immediate/offset for I-type
        imm = instruction & 0xFFFF
        
        # Extract target for J-type
        target = instruction & 0x3FFFFFF
        
        return {
            'opcode': opcode,
            'rs': rs,
            'rt': rt,
            'rd': rd,
            'funct': funct,
            'imm': imm,
            'target': target
        }
    
    def execute(self, decoded_instruction):
        """Execute the decoded instruction."""
        opcode = decoded_instruction['opcode']
        rs = decoded_instruction['rs']
        rt = decoded_instruction['rt']
        rd = decoded_instruction['rd']
        funct = decoded_instruction['funct']
        imm = decoded_instruction['imm']
        
        # R-type instructions
        if opcode == 0:
            rs_val = self.registers.read_register(rs)
            rt_val = self.registers.read_register(rt)
            
            if funct == 0b100000:  # add
                result = self.instructions.add(rd, rs_val, rt_val)
                self.registers.write_register(rd, result)
            elif funct == 0b100010:  # sub
                result = self.instructions.sub(rd, rs_val, rt_val)
                self.registers.write_register(rd, result)
            elif funct == 0b100100:  # and
                result = self.instructions.and_op(rd, rs_val, rt_val)
                self.registers.write_register(rd, result)
            elif funct == 0b100101:  # or
                result = self.instructions.or_op(rd, rs_val, rt_val)
                self.registers.write_register(rd, result)
            elif funct == 0b101010:  # slt
                result = self.instructions.slt(rd, rs_val, rt_val)
                self.registers.write_register(rd, result)
            elif funct == 0b000000:  # sll
                shamt = (decoded_instruction['rd'] << 0) | (funct >> 6)
                result = self.instructions.sll(rd, rt_val, shamt)
                self.registers.write_register(rt, result)
            elif funct == 0b000010:  # srl
                shamt = (decoded_instruction['rd'] << 0) | (funct >> 6)
                result = self.instructions.srl(rd, rt_val, shamt)
                self.registers.write_register(rt, result)
        
        # I-type instructions
        elif opcode == 0b001000:  # addi
            rs_val = self.registers.read_register(rs)
            result = self.instructions.addi(rt, rs_val, imm)
            self.registers.write_register(rt, result)
        
        elif opcode == 0b000100:  # beq
            rs_val = self.registers.read_register(rs)
            rt_val = self.registers.read_register(rt)
            if rs_val == rt_val:
                return False, imm
            return True, None
        
        elif opcode == 0b000101:  # bne
            rs_val = self.registers.read_register(rs)
            rt_val = self.registers.read_register(rt)
            if rs_val != rt_val:
                return False, imm
            return True, None
        
        elif opcode == 0b100011:  # lw
            rs_val = self.registers.read_register(rs)
            addr = rs_val + imm
            value = self.memory.load_word(addr)
            self.registers.write_register(rt, value)
        
        elif opcode == 0b101011:  # sw
            rs_val = self.registers.read_register(rs)
            rt_val = self.registers.read_register(rt)
            addr = rs_val + imm
            self.memory.store_word(addr, rt_val)
            
        #J-type instructions
        elif opcode == 0b000010:  # j
            return False, addr
        
        elif opcode == 0b000011:  # jal
            self.registers.write_register(31, self.pc + 4)  # Store return address
            return False, addr

        return True, None
        
    def run_program(self, instructions):
        """Load and execute a list of assembly instructions."""
        # First pass: assemble instructions and load into memory
        for i, instr in enumerate(instructions):
            machine_code = self.assembler.assemble(instr)
            self.memory.load_instruction(i, machine_code)
        
        # Reset program counter
        self.registers.pc = 0
        
        # Execute instructions
        while self.registers.pc < len(instructions):
            instruction = self.fetch()
            decoded = self.decode(instruction)
            self.execute(decoded)