
from .registers import Registers
from .memory import Memory
from .assembler import Assembler

'''
    Simulator Component
    Interface for UI to access the SIM component.
'''

class Simulator:
    def __init__(self):
        self.registers = Registers()
        self.memory = Memory()
        self.assembler = Assembler()
        self.current_pc = 0
        self.program_loaded = False
        self.program_length = 0
        self.debug_mode = False
        self.execution_history = []
        
    def load(self, program):
        """Load and assemble program from string"""
        # Returns: Translated binary code as default
        self.registers.reset()
        self.memory.reset()
        self.current_pc = 0
        self.registers.pc = 0
        self.execution_history.clear()
        
        machine_code = self.assembler.assemble(program)
        
        for i, instruction in enumerate(machine_code):
            self.memory.load_instruction(i, instruction)
            
        self.program_length = len(machine_code)
        self.program_loaded = True
        
        translations = self.assembler.get_translations('binary')
        result = '\n'.join(translations)
        return result

    def load_from_file(self, filename):
        """Load and assemble program from file"""
        with open(filename, 'r') as f:
            program = f.read()
            
        return self.load(program)

    def step(self):
        """Execute single instruction and return detailed state"""
        # Returns: Status KV pair from the step executed
        if not self.program_loaded:
            return {
                'status': 'error',
                'message': 'No program loaded',
                'state': self.get_state()
            }

        if self.registers.pc >= self.program_length * 4:
            return {
                'status': 'completed',
                'message': 'Program completed - reached end of instructions',
                'state': self.get_state()
            }

        instruction = self.memory.get_instruction(self.registers.pc)
        if instruction == 0:
            return {
                'status': 'halted',
                'message': 'Program halted - reached null instruction',
                'state': self.get_state()
            }

        # Record pre-execution state
        old_pc = self.registers.pc
        pre_state = self.get_register_state()

        # Execute instruction
        continue_execution = self.execute_instruction(instruction)
        
        # Record execution in history
        instruction_info = self._get_instruction_info(instruction)
        execution_record = {
            'pc': old_pc,
            'instruction': f"0x{instruction:08x}",
            'instruction_info': instruction_info,
            'pre_state': pre_state,
            'post_state': self.get_register_state()
        }
        self.execution_history.append(execution_record)

        # Update PC if needed
        if continue_execution:
            self.registers.pc += 4
            self.current_pc = self.registers.pc

        result = {
            'status': 'running',
            'pc': self.registers.pc,
            'previous_pc': old_pc,
            'instruction': f"0x{instruction:08x}",
            'instruction_info': instruction_info,
            'state': self.get_state(),
            'message': 'Instruction executed successfully'
        }

        if self.debug_mode:
            self._print_step_debug(result)

        return result

    def run(self):
        """Run the program with detailed execution tracking"""
        # Returns: Status KV pair from the whole program
        if not self.program_loaded:
            return {
                'status': 'error',
                'message': 'No program loaded',
                'execution_history': self.execution_history
            }

        print("\nStarting program execution...")
        instruction_count = 0
        max_iterations = 1000000  # Prevent infinite loops
        execution_results = []

        while instruction_count < max_iterations:
            step_result = self.step()
            execution_results.append(step_result)
            
            if step_result['status'] in ['completed', 'halted', 'error']:
                break
                
            instruction_count += 1

        final_result = {
            'status': 'completed',
            'instructions_executed': instruction_count,
            'execution_results': execution_results,
            'final_state': self.get_state(),
            'message': f"Program execution completed with {instruction_count} instructions"
        }

        if instruction_count >= max_iterations:
            final_result.update({
                'status': 'error',
                'message': 'Program terminated - reached maximum instruction limit'
            })

        if self.debug_mode:
            self._print_run_debug(final_result)

        return final_result

    def get_state(self):
        """Get current simulator state"""
        return {
            'pc': self.registers.pc,
            'registers': self.get_register_state(),
            'memory': self.get_memory_state(),
            'history': self.execution_history
        }

    def get_register_state(self):
        """Get register contents with sign extension"""
        register_state = {}
        for i in range(32):
            value = self.registers.read_register(i)
            # Convert 2's complement to signed
            if value & 0x80000000:  # If negative (MSB is 1)
                value = -((~value + 1) & 0xFFFFFFFF)
            register_state[i] = value
        return register_state

    def get_memory_state(self):
        """Get memory contents"""
        return {
            'instructions': self.memory.read_instruction_memory(),
            'data': self.memory.read_data_memory()
        }

    def execute_r_type(self, instruction, rs, rt, rd, shamt, funct):
        """Handle R-type instructions"""
        rs_val = self.registers.read_register(rs)
        rt_val = self.registers.read_register(rt)
        
        if funct == 0x20:  # add
            result = (rs_val + rt_val) & 0xFFFFFFFF  # Add truncation
            self.registers.write_register(rd, result)
        elif funct == 0x22:  # sub
            result = (rs_val - rt_val) & 0xFFFFFFFF  # Add truncation
            self.registers.write_register(rd, result)
        elif funct == 0x24:  # and
            result = rs_val & rt_val
            self.registers.write_register(rd, result)
        elif funct == 0x25:  # or
            result = rs_val | rt_val
            self.registers.write_register(rd, result)
        elif funct == 0x2A:  # slt
            # Sign comparison for SLT
            rs_signed = rs_val if rs_val < 0x80000000 else rs_val - 0x100000000
            rt_signed = rt_val if rt_val < 0x80000000 else rt_val - 0x100000000
            result = 1 if rs_signed < rt_signed else 0
            self.registers.write_register(rd, result)
        elif funct == 0x00:  # sll
            result = (rt_val << shamt) & 0xFFFFFFFF
            self.registers.write_register(rd, result)
        elif funct == 0x02:  # srl
            result = (rt_val >> shamt) & 0xFFFFFFFF
            self.registers.write_register(rd, result)
        elif funct == 0x08:  # jr
            self.current_pc = rs_val
            self.registers.pc = self.current_pc
            return False
        return True

    def execute_i_type(self, op, rs, rt, imm):
        """Handle I-type instructions"""
        rs_val = self.registers.read_register(rs)
        
        # Sign extend immediate value
        if imm & 0x8000:
            imm |= 0xFFFF0000
            
        if op == 0x08:  # addi
            result = (rs_val + imm) & 0xFFFFFFFF
            self.registers.write_register(rt, result)
            
        elif op == 0x23:  # lw
            addr = (rs_val + imm) & 0xFFFFFFFF
            value = self.memory.read_word(addr)
            self.registers.write_register(rt, value)
            
        elif op == 0x2B:  # sw
            addr = (rs_val + imm) & 0xFFFFFFFF
            rt_val = self.registers.read_register(rt)
            self.memory.write_word(addr, rt_val)
            
        elif op == 0x04:  # beq
            rt_val = self.registers.read_register(rt)
            if rs_val == rt_val:
                target = self.registers.pc + 4 + (imm << 2)
                self.current_pc = target
                self.registers.pc = target
                return False
                
        elif op == 0x05:  # bne
            rt_val = self.registers.read_register(rt)
            if rs_val != rt_val:
                target = self.registers.pc + 4 + (imm << 2)
                self.current_pc = target
                self.registers.pc = target
                return False
        
        return True

    def execute_j_type(self, op, address):
        """Handle J-type instructions"""      
        if op == 0x02:  # j
            target = (self.registers.pc & 0xF0000000) | (address << 2)
            self.current_pc = target
            self.registers.pc = target
            return False
            
        elif op == 0x03:  # jal
            target = (self.registers.pc & 0xF0000000) | (address << 2)
            self.registers.write_register(31, self.registers.pc + 4)  # Store return address
            self.current_pc = target
            self.registers.pc = target
            return False
            
        return True

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

        # Handle instruction based on type
        if op == 0:  # R-type
            return self.execute_r_type(instruction, rs, rt, rd, shamt, funct)
        elif op in [0x02, 0x03]:  # J-type
            return self.execute_j_type(op, address)
        else:  # I-type
            return self.execute_i_type(op, rs, rt, imm)

    def _get_instruction_info(self, instruction):
        """Decode and return instruction information"""
        op = (instruction >> 26) & 0x3F
        rs = (instruction >> 21) & 0x1F
        rt = (instruction >> 16) & 0x1F
        rd = (instruction >> 11) & 0x1F
        shamt = (instruction >> 6) & 0x1F
        funct = instruction & 0x3F
        imm = instruction & 0xFFFF
        address = instruction & 0x3FFFFFF

        return {
            'opcode': f"0x{op:02x}",
            'type': 'R-type' if op == 0 else 'J-type' if op in [0x02, 0x03] else 'I-type',
            'fields': {
                'rs': f"${rs} ({self.registers.get_register_name(rs)})",
                'rt': f"${rt} ({self.registers.get_register_name(rt)})",
                'rd': f"${rd} ({self.registers.get_register_name(rd)})",
                'shamt': shamt,
                'funct': f"0x{funct:02x}",
                'immediate': f"0x{imm:04x}",
                'address': f"0x{address:07x}"
            }
        }

    def _print_step_debug(self, result):
        """Print debug information for step execution"""
        print("\nInstruction Execution Details:")
        print(f"PC: 0x{result['pc']:08x} (Previous: 0x{result['previous_pc']:08x})")
        print(f"Instruction: {result['instruction']}")
        print("\nInstruction Info:")
        info = result['instruction_info']
        print(f"Type: {info['type']}")
        print(f"Opcode: {info['opcode']}")
        print("\nFields:")
        for field, value in info['fields'].items():
            print(f"  {field}: {value}")
        
        if self.debug_mode == 2:  # More detailed debug level
            print("\nRegister Changes:")
            pre_state = result['state']['history'][-1]['pre_state']
            post_state = result['state']['history'][-1]['post_state']
            for reg in range(32):
                if pre_state[reg] != post_state[reg]:
                    reg_name = self.registers.get_register_name(reg)
                    print(f"  ${reg} ({reg_name}): 0x{pre_state[reg]:08x} -> 0x{post_state[reg]:08x}")

    def _print_run_debug(self, result):
        """Print debug information for complete program execution"""
        print("\nProgram Execution Summary:")
        print(f"Status: {result['status']}")
        print(f"Instructions Executed: {result['instructions_executed']}")
        print(f"Message: {result['message']}")
        
        if self.debug_mode == 2:  # More detailed debug level
            print("\nFinal Register State:")
            for reg in range(32):
                reg_name = self.registers.get_register_name(reg)
                value = result['final_state']['registers'][reg]
                print(f"  ${reg} ({reg_name}): 0x{value:08x}")
            
            print("\nNon-Zero Memory Contents:")
            for addr, value in result['final_state']['memory']['data'].items():
                if value != 0:
                    print(f"  [0x{int(addr):08x}]: 0x{value:08x}")
    
    def _print_info(self):
        """Print the current state of registers and memory"""
        reg_state = self.get_register_state()
        print("\nRegister Contents:")
        for reg_num, value in reg_state.items():
            print(f"{self.registers.get_register_name(reg_num)}: {value}")

        print("\nInstruction Memory Contents:")
        for i, instruction in enumerate(self.memory.instruction_memory):
            if instruction != 0:  # Only print non-zero instructions
                print(f"[0x{i*4:04x}] 0x{instruction:08x}")
    
        print("\nData Memory Contents:")
        for i, data in enumerate(self.memory.data_memory):
            if data != 0:  # Only print non-zero data
                print(f"{i}[0x{i*4:04x}] 0x{data:08x}")
    