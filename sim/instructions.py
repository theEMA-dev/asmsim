# R-format Instructions
def add(registers, rd, rs, rt):
    result = registers.read(rs) + registers.read(rt)
    registers.write(rd, result)

def sub(registers, rd, rs, rt):
    result = registers.read(rs) - registers.read(rt)
    registers.write(rd, result)
    
def andOp(registers, rd, rs, rt):
    result = registers.read(rs) & registers.read(rt)
    registers.write(rd, result)

def orOp(registers, rd, rs, rt):
    result = registers.read(rs) | registers.read(rt)
    registers.write(rd, result)
    
def slt(registers, rd, rs, rt):
    result = 1 if registers.read(rs) < registers.read(rt) else 0
    registers.write(rd, result)
    
def sll(registers, rd, rt, shamt):
    result = registers.read(rt) << shamt
    registers.write(rd, result)
    
def srl(registers, rd, rt, shamt):
    result = registers.read(rt) >> shamt
    registers.write(rd, result)

# I-format Instructions
def addi(registers, rt, rs, imm):
    result = registers.read(rs) + imm
    registers.write(rt, result)
    
def lw(registers, rt, rs):
    address = registers.read(rs)
    registers.write(rt, registers.memory.read(address))
    
def sw(registers, rt, rs):
    address = registers.read(rs)
    registers.memory.write(address, registers.read(rt))
    
def beq(registers, rs, rt, label):
    if registers.read(rs) == registers.read(rt):
        registers.branch(label)
        
def bne(registers, rs, rt, label):
    if registers.read(rs) != registers.read(rt):
        registers.branch(label)

# J-format Instructions
def j(registers, label):
    registers.jump(label)
    
def jal(registers, label):
    registers.write(31, registers.pc)
    registers.jump(label)
    
def jr(registers, rs):
    registers.jump(registers.read(rs))