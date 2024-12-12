import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QColor, QPalette

class AssemblyEditorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Assembly and Machine Code Editor")
        self.setGeometry(100, 100, 1200, 800)

        # Dark theme
        self.setStyleSheet("background-color: #2E2E2E; color: white;")

        # Main layout
        main_layout = QVBoxLayout()

        # Top section (Assembly and Machine Code)
        top_layout = QHBoxLayout()

        # Left section (Assembly code area)
        self.assembly_text = QTextEdit(self)
        self.assembly_text.setPlaceholderText("Write assembly code here...")
        self.assembly_text.setStyleSheet("background-color: #444444; font-size: 14pt;")
        self.assembly_text.setFixedWidth(400)

        # Middle section (Machine code area)
        self.machine_code_label = QLabel("Machine Code Display Area", self)
        self.machine_code_label.setStyleSheet("background-color: #444444; padding: 10px; font-size: 14pt;")
        self.machine_code_label.setFixedWidth(400)

        # Right section (Register display area)
        self.register_label = QLabel("Register Display Area", self)
        self.register_label.setStyleSheet("background-color: #444444; padding: 10px; font-size: 14pt;")
        self.register_label.setFixedWidth(400)

        # Spacer to fill the gaps
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Adding widgets to the top layout
        top_layout.addWidget(self.assembly_text)
        top_layout.addItem(spacer)
        top_layout.addWidget(self.machine_code_label)
        top_layout.addItem(spacer)
        top_layout.addWidget(self.register_label)

        # Bottom section (IM and DM memory)
        bottom_layout = QHBoxLayout()

        # IM (Instruction Memory) section
        self.im_text = QTextEdit(self)
        self.im_text.setPlaceholderText("Instruction Memory (IM)...")
        self.im_text.setStyleSheet("background-color: #444444; font-size: 14pt;")
        self.im_text.setFixedHeight(200)

        # DM (Data Memory) section
        self.dm_text = QTextEdit(self)
        self.dm_text.setPlaceholderText("Data Memory (DM)...")
        self.dm_text.setStyleSheet("background-color: #444444; font-size: 14pt;")
        self.dm_text.setFixedHeight(200)

        # Adding widgets to the bottom layout
        bottom_layout.addWidget(self.im_text)
        bottom_layout.addWidget(self.dm_text)

        # Button (optional, for running the code)
        self.execute_button = QPushButton("Run", self)
        self.execute_button.setStyleSheet("background-color: #555555; color: white; font-size: 14pt;")
        self.execute_button.clicked.connect(self.execute_code)

        # Adding top and bottom layouts to the main layout
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)
        main_layout.addWidget(self.execute_button)

        self.setLayout(main_layout)

    def execute_code(self):
        # This function is triggered when the Run button is clicked
        print("Assembly Code:\n", self.assembly_text.toPlainText())
        print("Machine Code:\n", self.machine_code_label.text())
        print("Registers:\n", self.register_label.text())
        print("Instruction Memory (IM):\n", self.im_text.toPlainText())
        print("Data Memory (DM):\n", self.dm_text.toPlainText())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AssemblyEditorApp()
    window.show()
    sys.exit(app.exec_())
