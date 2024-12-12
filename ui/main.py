import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QSize
#from simulator.interface import load_program, step_execution, get_state

class MIPSApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("MIPS Simulator")
        self.setGeometry(100, 100, 800, 600)
        
        self.apply_styles()

        # Initialize UI components
        self.code_input = self.create_text_edit(placeholder="Enter MIPS assembly code here...")
        self.load_button = self.create_button("Load Program", self.load_program)
        self.step_button = self.create_button("Step Execution", self.step_execution)
        self.output = self.create_text_edit(read_only=True)

        # Arrange components in the layout
        layout = QVBoxLayout()
        layout.addWidget(self.code_input)
        layout.addWidget(self.load_button)
        layout.addWidget(self.step_button)
        layout.addWidget(self.output)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def apply_styles(self):
        """Apply dark theme to the entire application."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2e2e2e;
            }
            QTextEdit, QLineEdit {
                background-color: #3c3c3c;
                color: #f0f0f0;
                border: 1px solid #555;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #555;
                color: #f0f0f0;
                border: 1px solid #444;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)

    def create_text_edit(self, placeholder=None, read_only=False):
        """Helper method to create a QTextEdit widget."""
        text_edit = QTextEdit(self)
        if placeholder:
            text_edit.setPlaceholderText(placeholder)
        if read_only:
            text_edit.setReadOnly(True)
        return text_edit

    def create_button(self, text, action):
        """Helper method to create a QPushButton widget."""
        button = QPushButton(text, self)
        button.clicked.connect(action)
        
        # Set fixed size for the buttons (taller and less wide)
        button.setFixedSize(200, 50)  # 200px width, 50px height
        return button

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
