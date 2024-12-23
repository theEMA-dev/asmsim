import os
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from sim.simulator import Simulator
import unittest as ut

class RFormatInstructionsTest(ut.TestCase):
    def setUp(self):
        self.simulator = Simulator()
        self.test_add = """
        addi $s0, $zero, 5    # s0 = 5
        addi $s1, $zero, 3    # s1 = 3
        add $t0, $s0, $s1    # t0 = 8
        """
        self.test_sub = """
        addi $s0, $zero, 5    # s0 = 5
        addi $s1, $zero, 3    # s1 = 3
        sub $t0, $s0, $s1    # t0 = 2
        """
        self.test_and = """
        addi $s0, $zero, 5    # s0 = 5
        addi $s1, $zero, 3    # s1 = 3
        and $t0, $s0, $s1    # t0 = 1
        """
        self.test_or = """
        addi $s0, $zero, 5    # s0 = 5
        addi $s1, $zero, 3    # s1 = 3
        or $t0, $s0, $s1    # t0 = 7
        """
        self.test_slt = """
        addi $s0, $zero, 5    # s0 = 5
        addi $s1, $zero, 3    # s1 = 3
        slt $t0, $s0, $s1    # t0 = 0
        """
        self.test_sll = """
        addi $s0, $zero, 5    # s0 = 5
        sll $t0, $s0, 2    # t0 = 20
        """
        self.test_srl = """
        addi $s0, $zero, 5    # s0 = 5
        srl $t0, $s0, 2    # t0 = 1
        """
        
    def test_add(self):
        self.simulator.load(self.test_add)
        
        state = self.simulator.step()
        self.assertEqual(state['status'], 'running')
        self.assertEqual(state['state']['registers'][16], 5)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][17], 3)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][8], 8)
        
        print('Successful test: ADD')
        
    def test_sub(self):
        self.simulator.load(self.test_sub)
        
        state = self.simulator.step()
        self.assertEqual(state['status'], 'running')
        self.assertEqual(state['state']['registers'][16], 5)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][17], 3)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][8], 2)
        
        print('Successful test: SUB')
        
    def test_and(self):
        self.simulator.load(self.test_and)
        
        state = self.simulator.step()
        self.assertEqual(state['status'], 'running')
        self.assertEqual(state['state']['registers'][16], 5)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][17], 3)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][8], 1)
        
        print('Successful test: AND')
        
    def test_or(self):
        self.simulator.load(self.test_or)
        
        state = self.simulator.step()
        self.assertEqual(state['status'], 'running')
        self.assertEqual(state['state']['registers'][16], 5)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][17], 3)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][8], 7)
        
        print('Successful test: OR')
        
    def test_slt(self):
        self.simulator.load(self.test_slt)
        
        state = self.simulator.step()
        self.assertEqual(state['status'], 'running')
        self.assertEqual(state['state']['registers'][16], 5)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][17], 3)
        
        
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][8], 0)
        
        print('Successful test: SLT')
    
    def test_sll(self):
        self.simulator.load(self.test_sll)
        
        state = self.simulator.step()
        self.assertEqual(state['status'], 'running')
        self.assertEqual(state['state']['registers'][16], 5)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][8], 20)
        
        print('Successful test: SLL')
    
    def test_srl(self):
        self.simulator.load(self.test_srl)
        
        state = self.simulator.step()
        self.assertEqual(state['status'], 'running')
        self.assertEqual(state['state']['registers'][16], 5)
        
        state = self.simulator.step()
        self.assertEqual(state['state']['registers'][8], 1)
        
        print('Successful test: SRL')
    
        