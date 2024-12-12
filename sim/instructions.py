class MIPSInstructions:
    @staticmethod
    def add(rd, rs, rt):
        """R-type add instruction."""
        return rs + rt
    
    @staticmethod
    def sub(rd, rs, rt):
        """R-type subtract instruction."""
        return rs - rt
    
    @staticmethod
    def and_op(rd, rs, rt):
        """R-type bitwise AND instruction."""
        return rs & rt
    
    @staticmethod
    def or_op(rd, rs, rt):
        """R-type bitwise OR instruction."""
        return rs | rt
    
    @staticmethod
    def slt(rd, rs, rt):
        """R-type set less than instruction."""
        return 1 if rs < rt else 0
    
    @staticmethod
    def sll(rd, rt, shamt):
        """R-type shift left logical instruction."""
        return rt << shamt
    
    @staticmethod
    def srl(rd, rt, shamt):
        """R-type shift right logical instruction."""
        return rt >> shamt
    
    @staticmethod
    def addi(rt, rs, imm):
        """I-type add immediate instruction."""
        # Sign extend immediate value
        if imm & 0x8000:
            imm = -((~imm + 1) & 0xFFFF)
        return rs + imm