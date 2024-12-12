from sim.instructions import add, sub

class CPU:
    def __init__(self, registers, memory):
        self.registers = registers
        self.memory = memory

    def execute(self, instruction):
        """Decode and execute an instruction."""
        opcode = instruction[:6]
        if opcode == '000000':  # R-type instruction
            func = instruction[26:]  # Function code
            if func == '100000':  # ADD
                add(self.registers, rs, rt, rd)
            elif func == '100010':  # SUB
                sub(self.registers, rs, rt, rd)
        # Handle I-type and J-type instructions similarly.
