from registers import Registers
from memory import Memory
from assembler import Assembler

class Simulator:
    def __init__(self):
        self.registers = Registers()
        self.memory = Memory()
        self.assembler = Assembler()
        
    def load_program(self, filename):
        """Load and assemble program from file"""
        with open(filename, 'r') as f:
            program = f.read()
            
        # Assemble the program
        machine_code = self.assembler.assemble(program)
        
        # Load into memory
        for i, instruction in enumerate(machine_code):
            self.memory.load_instruction(i, instruction)
            
        return len(machine_code)

    def execute_instruction(self, instruction):
        """Execute a single instruction"""
        # Extract operation fields
        op = (instruction >> 26) & 0x3F
        rs = (instruction >> 21) & 0x1F
        rt = (instruction >> 16) & 0x1F
        rd = (instruction >> 11) & 0x1F
        shamt = (instruction >> 6) & 0x1F
        funct = instruction & 0x3F
        imm = instruction & 0xFFFF
        address = instruction & 0x3FFFFFF

        # R-format instructions
        if op == 0:
            rs_val = self.registers.read_register(rs)
            rt_val = self.registers.read_register(rt)
            
            if funct == 0x20:  # add
                result = rs_val + rt_val
                self.registers.write_register(rd, result)
            elif funct == 0x22:  # sub
                result = rs_val - rt_val
                self.registers.write_register(rd, result)
            elif funct == 0x24:  # and
                result = rs_val & rt_val
                self.registers.write_register(rd, result)
            elif funct == 0x25:  # or
                result = rs_val | rt_val
                self.registers.write_register(rd, result)
            elif funct == 0x2A:  # slt
                result = 1 if rs_val < rt_val else 0
                self.registers.write_register(rd, result)
            elif funct == 0x00:  # sll
                result = rt_val << shamt
                self.registers.write_register(rd, result)
            elif funct == 0x02:  # srl
                result = rt_val >> shamt
                self.registers.write_register(rd, result)
            elif funct == 0x08:  # jr
                self.registers.pc = rs_val
                return False
        
        # I-format instructions
        elif op == 0x08:  # addi
            rs_val = self.registers.read_register(rs)
            # Sign extend immediate value
            if imm & 0x8000:
                imm = -((~imm + 1) & 0xFFFF)
            result = rs_val + imm
            self.registers.write_register(rt, result)
            
        elif op == 0x23:  # lw
            rs_val = self.registers.read_register(rs)
            addr = rs_val + ((imm ^ 0x8000) - 0x8000)  # Sign extend
            value = self.memory.read_word(addr)
            self.registers.write_register(rt, value)
            
        elif op == 0x2B:  # sw
            rs_val = self.registers.read_register(rs)
            rt_val = self.registers.read_register(rt)
            addr = rs_val + ((imm ^ 0x8000) - 0x8000)  # Sign extend
            self.memory.write_word(addr, rt_val)
            
        elif op == 0x04:  # beq
            rs_val = self.registers.read_register(rs)
            rt_val = self.registers.read_register(rt)
            if rs_val == rt_val:
                offset = imm
                if offset & 0x8000:  # Check if negative
                    offset = -((~offset + 1) & 0xFFFF)
                self.registers.pc += (offset * 4)  # Word-aligned addresses
                print(f"DEBUG: BEQ taken to PC={self.registers.pc:08x}")
                return False
                
        elif op == 0x05:  # bne
            rs_val = self.registers.read_register(rs)
            rt_val = self.registers.read_register(rt)
            if rs_val != rt_val:
                offset = imm
                if offset & 0x8000:  # Check if negative
                    offset = -((~offset + 1) & 0xFFFF)
                self.registers.pc += (offset * 4)  # Word-aligned addresses
                print(f"DEBUG: BNE taken to PC={self.registers.pc:08x}")
                return False
                
        # J-format instructions
        elif op == 0x02:  # j
            target = address
            print(f"DEBUG: Jump instruction - target={target:08x}")
            self.registers.pc = target  # Set PC directly to target address
            return False
            
        elif op == 0x03:  # jal
            target = ((self.registers.pc & 0xF0000000) | (address << 2))
            self.registers.write_register(31, self.registers.pc + 1)
            self.registers.pc = target >> 2
            print(f"Jump and link to address: 0x{target:08x}")
            return False
            
        return True

    def run(self):
        print("\nStarting program execution...")
        max_instructions = len(self.memory.instruction_memory)
        instruction_count = 0
        max_iterations = 1000000
    
        while self.registers.pc < max_instructions and instruction_count < max_iterations:
            print(f"\nFetching instruction at PC index={self.registers.pc}")
            instruction = self.memory.get_instruction(self.registers.pc)
            if instruction == 0:
                print("Halting - null instruction")
                break
            
            print(f"PC: {self.registers.pc:04x} | Instruction: 0x{instruction:08x}")
            continue_execution = self.execute_instruction(instruction)
            instruction_count += 1
        
            if continue_execution:
                self.registers.pc += 4
                
    def print_registers(self):
        """Print the current state of registers"""
        print("\nProgram completed. Register contents:")
        for i in range(32):
            name = self.registers.get_register_name(i)
            value = self.registers.read_register(i)
            if value != 0:  # Only print non-zero registers
                print(f"{name}: {value}")

    def print_memory(self):
        """Print the contents of instruction and data memory"""
        print("\nInstruction Memory Contents:")
        for i, instruction in enumerate(self.memory.instruction_memory):
            if instruction != 0:  # Only print non-zero instructions
                print(f"[0x{i*4:04x}] 0x{instruction:08x}")
    
        print("\nData Memory Contents:")
        for i, data in enumerate(self.memory.data_memory):
            if data != 0:  # Only print non-zero data
                print(f"[0x{i*4:04x}] 0x{data:08x}")
                
    def simulateFromFile(self, filename):
        program_length = self.load_program(filename)
        print(f"Loaded program of {program_length} instructions")
        self.run()
        self.print_registers()
        self.print_memory()
            
def main():
    simulator = Simulator()
    try:
        simulator.simulateFromFile('./test.asm')
        
    except FileNotFoundError:
        print("Running in debug mode")
        simulator.simulateFromFile('./sim/test.asm')
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
    