import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
#from simulator.interface import load_program, step_execution, get_state

class MIPSApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("MIPS Simulator")
        self.setGeometry(100, 100, 800, 600)

        # Textbox for assembly code input
        self.code_input = QTextEdit(self)
        self.code_input.setPlaceholderText("Enter MIPS assembly code here...")

        # Button to load program
        self.load_button = QPushButton("Load Program", self)
        self.load_button.clicked.connect(self.load_program)

        # Button for step execution
        self.step_button = QPushButton("Step Execution", self)
        self.step_button.clicked.connect(self.step_execution)

        # Output box for registers/memory state
        self.output = QTextEdit(self)
        self.output.setReadOnly(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.code_input)
        layout.addWidget(self.load_button)
        layout.addWidget(self.step_button)
        layout.addWidget(self.output)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_program(self):
        """Load program into the simulator."""
        code = self.code_input.toPlainText().strip().split("\n")
        load_program(code)
        self.output.append("Program loaded successfully!")

    def step_execution(self):
        """Perform step-by-step execution."""
        state = step_execution()
        self.output.append(f"PC: {state['pc']}")
        self.output.append(f"Registers: {state['registers']}")
        self.output.append(f"Memory: {state['memory'][:64]}...")  # Show a snippet

def main():
    app = QApplication(sys.argv)
    mips_app = MIPSApp()
    mips_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
