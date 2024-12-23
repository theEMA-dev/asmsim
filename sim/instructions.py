class Instructions:
    @staticmethod
    def add(rs, rt):
        return rs + rt
    
    @staticmethod
    def sub(rs, rt):
        return rs - rt
    
    @staticmethod
    def and_op(rs, rt):
        return rs & rt
    
    @staticmethod
    def or_op(rs, rt):
        return rs | rt
    
    @staticmethod
    def slt(rs, rt):
        return 1 if rs < rt else 0
    
    @staticmethod
    def sll(rt, shamt):
        return rt << shamt
    
    @staticmethod
    def srl(rt, shamt):
        return rt >> shamt
    
    @staticmethod
    def addi(rs, imm):
        # Sign extend immediate value
        if imm & 0x8000:
            imm = -((~imm + 1) & 0xFFFF)
        return rs + imm
    
    @staticmethod
    def beq(rs_val, rt_val, label):
        return rs_val == rt_val, label

    @staticmethod
    def bne(rs_val, rt_val, label):
        return rs_val != rt_val, label

    @staticmethod
    def lw(base_addr, offset):
        return base_addr + offset

    @staticmethod
    def sw(base_addr, offset):
        return base_addr + offset

    @staticmethod
    def j(target):
        return target

    @staticmethod
    def jal(target, return_addr):
        return target, return_addr
    
    @staticmethod
    def jr(rs_val):
        return rs_val