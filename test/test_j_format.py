import os
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from sim.simulator import Simulator
import unittest as ut

class RFormatInstructionsTest(ut.TestCase):
    def setUp(self):
        self.simulator = Simulator()
        self.test_j = """
        addi $s0, $zero, 5    # s0 = 5
        j skip
        addi $s1, $zero, 3    # s1 = 3
        skip:
        """
        self.test_jal = """
        addi $s0, $zero, 5    # s0 = 5
        jal skip
        addi $s1, $zero, 3    # s1 = 3
        skip:
        """
        self.test_jr = """
        addi $s0, $zero, 5    # s0 = 5
        addi $t0, $zero, 16   # address of 'skip' (3rd instruction * 4 bytes)
        jr $t0                # jump to skip label
        addi $s1, $zero, 3    # s1 = 3 (should be skipped)
        addi $s2, $zero, 7    # s2 = 7
        """
        
    def test_j(self):
        self.simulator.load(self.test_j)
        
        state = self.simulator.step()
        self.assertEqual(state['status'], 'running')
        self.assertEqual(state['state']['registers'][16], 5)
        
        state = self.simulator.step()
        self.assertEqual(state['status'], 'running')
        self.assertEqual(state['state']['registers'][17], 0)
        
        print('Successful test: J')
        
    def test_jal(self):
        self.simulator.load(self.test_jal)
        
        # First instruction (addi)
        state = self.simulator.step()
        self.assertEqual(state['status'], 'running')
        self.assertEqual(state['state']['registers'][16], 5)  # $s0 = 5
        
        # JAL instruction
        state = self.simulator.step()
        self.assertEqual(state['status'], 'running')
        self.assertEqual(state['state']['registers'][17], 0)  # $s1 should stay 0
        self.assertNotEqual(state['state']['registers'][31], 0)  # $ra should contain return address
        
        print('Successful test: JAL')
        
    def test_jr(self):
        self.simulator.load(self.test_jr)
        
        # First instruction (addi $s0)
        state = self.simulator.step()
        self.assertEqual(state['status'], 'running')
        self.assertEqual(state['state']['registers'][16], 5)
        
        # Second instruction (addi $t0)
        state = self.simulator.step()
        self.assertEqual(state['status'], 'running')
        self.assertEqual(state['state']['registers'][8], 16)
        
        # Third instruction (jr)
        state = self.simulator.step()
        self.assertEqual(state['status'], 'running')
        self.assertEqual(state['state']['registers'][17], 0)  # Verify skip
        
        # Fifth instruction (addi $s2)
        state = self.simulator.step()
        self.assertEqual(state['status'], 'running')
        self.assertEqual(state['state']['registers'][18], 7)
        
        print('Successful test: JR')
        