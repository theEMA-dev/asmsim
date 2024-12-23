import os
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from sim.simulator import Simulator
import unittest as ut

class FullExecution(ut.TestCase):
    def test_run(self):
        self.simulator = Simulator()
        self.simulator.simulateFromFile('./test/bin/demo.asm')
        
        print('Successful test: EXTERNAL FILE LOADING')