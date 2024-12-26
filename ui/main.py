import os
import sys
import pywinstyles
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel, QPushButton, QLineEdit, QFileDialog, QComboBox
from sim.simulator import Simulator
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtGui import QIcon

class AssemblyEditorApp(QWidget):
    def __init__(self):
        super().__init__()
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(os.path.dirname(__file__))
        self.translation_option = 'binary'
        self.simulator = Simulator()
        self.setWindowTitle("ASMsim - 32 Bit MIPS Assembly Simulator")
        icon_path = os.path.join(base_path, 'ui', 'assets', 'icon.ico')
        self.setWindowIcon(QIcon(icon_path))
        if os.name == 'nt':  
            import ctypes
            myappid = 'asmsim.1.0.0'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        screen = QDesktopWidget().screenGeometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()
        window_width = 1800
        window_height = 1000
        x = (self.screen_width - window_width) / 2
        y = (self.screen_height - window_height) / 2
        self.setGeometry(int(x), int(y), window_width, window_height)
        
        # Dark theme
        pywinstyles.apply_style(self, 'mica')

        # Main layout
        root = QHBoxLayout()
        main = QVBoxLayout()
        root.addLayout(main)
        self.setLayout(root)

        # Top section (Assembly and Machine Code)
        self.top_panel = QHBoxLayout()
        
        self.bottom_panel = QHBoxLayout()
        
        # Assembly code display
        self.assembly_block = QVBoxLayout()
        self.assembly_title = QHBoxLayout()
        self.assembly_label = QLabel("Assembly Code", self)
        self.assembly_label.setAlignment(Qt.AlignLeft)
        self.button_clear = QPushButton("Clear", self)
        self.button_clear.setProperty("class", "tertiary")
        self.button_clear.setCursor(Qt.PointingHandCursor)
        self.button_clear.clicked.connect(lambda: (self.assembly_input.clear(), self.machine_code_display.clear(), self.counter_pc.clear(), self.im_text.clear(), self.dm_text.clear(), self.register_display.clear(), self.load_program()))
        self.button_clear.setVisible(False)
        self.assembly_title.addWidget(self.assembly_label, stretch=1)
        self.assembly_title.addWidget(self.button_clear)
        self.assembly_input = QTextEdit(self)
        self.assembly_input.setMinimumSize(600, 400)
        self.assembly_input.textChanged.connect(self.load_program)
        self.assembly_input.setPlaceholderText("Write assembly code here...")
        self.assembly_buttons = QHBoxLayout()
        self.button_upload = QPushButton("Load File", self)
        self.button_upload.setProperty("class", "secondary")
        self.button_upload.setCursor(Qt.PointingHandCursor)
        self.button_upload.clicked.connect(self.load_file)
        self.button_step = QPushButton("Step", self)
        self.button_step.setCursor(Qt.PointingHandCursor)
        self.button_step.clicked.connect(self.step_code)
        self.button_run = QPushButton("Run", self)
        self.button_run.setCursor(Qt.PointingHandCursor)
        self.button_run.clicked.connect(self.execute_code)
        self.assembly_buttons.addWidget(self.button_upload)
        self.assembly_buttons.addWidget(self.button_step, stretch=1)
        self.assembly_buttons.addWidget(self.button_run, stretch=1)
        self.assembly_block.addLayout(self.assembly_title)
        self.assembly_block.addWidget(self.assembly_input)
        self.assembly_block.addLayout(self.assembly_buttons)
        
        # Machine code display
        self.machine_code_block = QVBoxLayout()
        self.machine_code_title = QHBoxLayout()
        self.machine_code_label = QLabel("Machine Code", self)
        self.machine_code_label.setAlignment(Qt.AlignLeft)
        self.machine_code_dropdown = QComboBox(self)
        self.machine_code_dropdown.addItems(["Binary", "Hex"])
        self.machine_code_dropdown.setCurrentIndex(0)
        self.machine_code_dropdown.currentIndexChanged.connect(self.updateTranslationOption)
        self.machine_code_title.addWidget(self.machine_code_label, stretch=1)
        self.machine_code_title.addWidget(self.machine_code_dropdown)
        self.machine_code_display = QTextEdit(self)
        self.machine_code_display.setReadOnly(True)
        self.machine_code_display.setMinimumSize(600, 400)
        self.status_indicators = QHBoxLayout()
        self.counter_pc = QLineEdit(self)
        self.counter_pc.setReadOnly(True)
        self.counter_pc.setPlaceholderText("PC Counter")
        self.status_indicators.addWidget(self.counter_pc)
        self.machine_code_block.addLayout(self.machine_code_title)
        self.machine_code_block.addWidget(self.machine_code_display)
        self.machine_code_block.addLayout(self.status_indicators)
        
        self.top_panel.addLayout(self.assembly_block)
        self.top_panel.addLayout(self.machine_code_block)
        main.addLayout(self.top_panel, stretch=1)
        
        # TAGS
        self.tag_authors = QLabel("Emir Kaynar & Şamil Keklikoğlu")
        self.tag_authors.setAlignment(Qt.AlignRight)
        self.tag_authors.setProperty("class", "tag")
        self.tag_app = QLabel("Build 1.0.2: 27-12-2024")
        self.tag_app.setAlignment(Qt.AlignLeft)
        self.tag_app.setProperty("class", "tag")
        
        # IM and DM memory display
        self.im_block = QVBoxLayout()
        self.im_label = QLabel("Instruction Memory", self)
        self.im_label.setAlignment(Qt.AlignLeft)
        self.im_text = QTextEdit(self)
        self.im_text.setReadOnly(True)
        self.im_text.setMinimumSize(600, 200)
        self.im_text.setMaximumHeight(200)
        self.im_block.addWidget(self.im_label)
        self.im_block.addWidget(self.im_text)
        self.im_block.addWidget(self.tag_app)
        
        self.dm_block = QVBoxLayout()
        self.dm_label = QLabel("Data Memory", self)
        self.dm_label.setAlignment(Qt.AlignLeft)
        self.dm_text = QTextEdit(self)
        self.dm_text.setReadOnly(True)
        self.dm_text.setMinimumSize(600, 200)
        self.dm_text.setMaximumHeight(200)
        self.dm_block.addWidget(self.dm_label)
        self.dm_block.addWidget(self.dm_text)
        self.dm_block.addWidget(self.tag_authors)
        
        self.bottom_panel.addLayout(self.im_block)
        self.bottom_panel.addLayout(self.dm_block)
        main.addLayout(self.bottom_panel)
        
        # Register display
        self.register_block = QVBoxLayout()
        self.register_label = QLabel("Registers", self)
        self.register_label.setAlignment(Qt.AlignCenter)
        self.register_display = QTextEdit(self)
        self.register_display.setReadOnly(True)
        self.register_display.setMinimumSize(150, 400)
        self.register_display.setMaximumWidth(150)
        self.register_block.addWidget(self.register_label)
        self.register_block.addWidget(self.register_display)
        
        root.addLayout(self.register_block)
        
        self.update()

    def update(self, result=None):
        current_state = self.simulator.get_state()
        reg_state = [f"{name}: {val}" for name, val in current_state['reg_labels'].items()]
        self.register_display.setText("\n".join(reg_state))
        
        if self.translation_option == 'binary':
            # Format memory displays with binary values
            im_state = [f"0x{addr*4:08x}: {val:032b}" for addr, val in enumerate(current_state['memory']['instructions']) if val != 0]
            dm_state = [f"0x{addr*4:08x}: {val:032b}" for addr, val in enumerate(current_state['memory']['data']) if val != 0]
        else:
            im_state = [f"0x{addr*4:08x}: 0x{val:08x}" for addr, val in enumerate(current_state['memory']['instructions']) if val != 0]
            dm_state = [f"0x{addr*4:08x}: 0x{val:08x}" for addr, val in enumerate(current_state['memory']['data']) if val != 0]
        
        self.im_text.setText("\n".join(im_state))
        self.dm_text.setText("\n".join(dm_state))
            
        if result and 'instruction_info' in result:
            self.counter_pc.setText(f"PC: 0x{result['pc']:08x} | OP: {result['instruction_info']['opcode']} | FUNCT: {result['instruction_info']['fields']['funct']} | RS: {result['instruction_info']['fields']['rs']} | RT: {result['instruction_info']['fields']['rt']} | RD: {result['instruction_info']['fields']['rd']}")
            
    def updateTranslationOption(self, index):
        self.translation_option = (index == 0) and 'binary' or 'hex'
        self.load_program()
        
    def load_file(self):
        file_path = QFileDialog.getOpenFileName(self, "Open Assembly File", "", "Assembly Files (*.asm)")[0]
        if file_path:
            with open(file_path, 'r') as f:
                self.assembly_input.setText(f.read())
                self.load_program()
        
    def load_program(self):
        try:
            self.button_clear.setVisible(True)
            assembly_code = self.assembly_input.toPlainText()
            if not assembly_code.strip():  # Skip if empty
                self.button_clear.setVisible(False)
                self.machine_code_display.clear()
                self.counter_pc.clear()
                return

            # Load and assemble code
            machine_code = self.simulator.load(assembly_code, self.translation_option)
            
            self.update()
            # Update machine code display
            self.machine_code_display.setStyleSheet("color: hsl(0, 0%, 63%);")
            self.machine_code_display.setText(machine_code)
            self.counter_pc.setText("PC: 0x00000000")
        except Exception as e:
            self.machine_code_display.setStyleSheet("color: red;")
            self.machine_code_display.setText(f"{str(e)}")
        
    def execute_code(self):
        result = self.simulator.run()
        self.update(result)
        self.counter_pc.setText("Execution Complete")
    
    def step_code(self):
        try:
            result = self.simulator.step()
            self.update(result)
        except Exception as e:
            self.counter_pc.setText(f"Error: {str(e)}")

def main():
    app = QApplication(sys.argv)
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))
        
    style_file = os.path.join(base_path, 'ui', 'styles.qss')
    with open(style_file, 'r') as f:
        app.setStyleSheet(f.read())
            
    window = AssemblyEditorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()