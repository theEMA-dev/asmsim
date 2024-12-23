import os
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from sim.simulator import Simulator
import unittest as ut

class IFormatInstructionsTest(ut.TestCase):
    def setUp(self):
        self.simulator = Simulator()
        self.test_addi = """
        addi $s0, $zero, 5    # s0 = 5
        addi $s1, $zero, 3    # s1 = 3
        addi $t0, $s0, 3      # t0 = 8
        """
        self.test_addi_negative = """
        addi $s0, $zero, 5    # s0 = 5
        addi $s1, $zero, -3   # s1 = -3
        addi $t0, $s0, -3     # t0 = 2
        """
        self.test_lw = """
        addi $s0, $zero, 12   # s0 = 12
        lw $t0, 0($s0)        # t0 = 42
        """
        self.test_sw = """
        addi $t0, $zero, 40   # t0 = 40
        addi $t1, $zero, 11   # t1 = 11
        sw $t0, 0($t0)        # memory[40] = 11
        """
        self.test_beq = """
        addi $s0, $zero, 5    # s0 = 5
        addi $s1, $zero, 5    # s1 = 5
        beq $s0, $s1, skip    # should branch
        addi $s2, $zero, 1    # s2 = 1
        skip:
        addi $s3, $zero, 2    # s3 = 2
        """
        self.test_beq_neq = """
        addi $s0, $zero, 5    # s0 = 5
        addi $s1, $zero, 6    # s1 = 6
        beq $s0, $s1, skip    # should not branch
        addi $s2, $zero, 1    # s2 = 1
        skip:
        addi $s3, $zero, 2    # s3 = 2
        """
        self.test_bne = """
        addi $s0, $zero, 5    # s0 = 5
        addi $s1, $zero, 6    # s1 = 6
        bne $s0, $s1, skip    # should branch
        addi $s2, $zero, 1    # s2 = 1
        skip:
        addi $s3, $zero, 2    # s3 = 2
        """
        self.test_bne_neq = """
        addi $s0, $zero, 5    # s0 = 5
        addi $s1, $zero, 5    # s1 = 5
        bne $s0, $s1, skip    # should not branch
        addi $s2, $zero, 1    # s2 = 1
        skip:
        addi $s3, $zero, 2    # s3 = 2
        """
        
        
    def test_addi(self):
        self.simulator.load(self.test_addi)
        
        state = self.simulator.step()
        self.assertEqual(state['status'], 'running')
        self.assertEqual(state['state']['registers'][16], 5)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][17], 3)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][8], 8)
        
        print('Successful test: ADDI (Positive)')
        
    def test_addi_negative(self):
        self.simulator.load(self.test_addi_negative)
        
        state = self.simulator.step()
        self.assertEqual(state['status'], 'running')
        self.assertEqual(state['state']['registers'][16], 5)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][17], -3)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][8], 2)
        
        print('Successful test: ADDI (Negative)')
        
    
    def test_lw(self):
        self.simulator.load(self.test_lw)
        self.simulator.memory.write_word(12, 42)
        
        state = self.simulator.step()
        self.assertEqual(state['status'], 'running')
        self.assertEqual(state['state']['registers'][16], 12)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][8], 42)
        
        print('Successful test: LW')
        
    def test_sw(self):
        self.simulator.load(self.test_sw)
        
        state = self.simulator.step()
        self.assertEqual(state['status'], 'running')
        self.assertEqual(state['state']['registers'][8], 40)  # $t0 = 40
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][9], 11)
        
        state = self.simulator.step()
        value = self.simulator.memory.read_word(40)
        self.assertEqual(value, 40)
        
        print('Successful test: SW')
        
    def test_beq(self):
        self.simulator.load(self.test_beq)
        
        state = self.simulator.step()
        self.assertEqual(state['status'], 'running')
        self.assertEqual(state['state']['registers'][16], 5)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][17], 5)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][18], 0)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][19], 2)
        
        print('Successful test: BEQ (Equals)')
        
    def test_beq_neq(self):
        self.simulator.load(self.test_beq_neq)
        
        state = self.simulator.step()
        self.assertEqual(state['status'], 'running')
        self.assertEqual(state['state']['registers'][16], 5)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][17], 6)
        
        state = self.simulator.step() # extra step to execute the branch
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][18], 1)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][19], 2)
        
        print('Successful test: BEQ (Not Equals)')
        
    def test_bne(self):
        self.simulator.load(self.test_bne)
        
        state = self.simulator.step()
        self.assertEqual(state['status'], 'running')
        self.assertEqual(state['state']['registers'][16], 5)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][17], 6)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][18], 0)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][19], 2)
        
        print('Successful test: BNE')
        
    def test_bne_neq(self):
        self.simulator.load(self.test_bne_neq)
        
        state = self.simulator.step()
        self.assertEqual(state['status'], 'running')
        self.assertEqual(state['state']['registers'][16], 5)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][17], 5)
        
        state = self.simulator.step() # extra step to execute the branch
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][18], 1)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][19], 2)
        
        print('Successful test: BNE (Not Equals)')