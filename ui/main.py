import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QGridLayout
from PyQt5.QtGui import QColor, QPalette

class AssemblyEditorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Assembly ve Makine Kod Editörü")
        self.setGeometry(100, 100, 1200, 800)

        # Karanlık tema
        self.setStyleSheet("background-color: #2E2E2E; color: white;")

        # Ana düzeni oluşturuyoruz
        main_layout = QVBoxLayout()

        # Üst kısmı oluşturuyoruz (Assembly ve Makine Kodları)
        top_layout = QHBoxLayout()

        # Sol kısmı (Assembly code kısmı)
        self.assembly_text = QTextEdit(self)
        self.assembly_text.setPlaceholderText("Assembly kodunu buraya yazın...")
        self.assembly_text.setStyleSheet("background-color: #444444;")
        self.assembly_text.setFixedWidth(300)

        # Ortadaki kısmı (Machine code kısmı)
        self.machine_code_text = QTextEdit(self)
        self.machine_code_text.setPlaceholderText("Makine kodunu buraya yazın...")
        self.machine_code_text.setStyleSheet("background-color: #444444;")
        self.machine_code_text.setFixedWidth(300)

        # Sağdaki kısmı (Register kısmı)
        self.register_text = QTextEdit(self)
        self.register_text.setPlaceholderText("Register'ları buraya yazın...")
        self.register_text.setStyleSheet("background-color: #444444;")
        self.register_text.setFixedWidth(300)

        # Üst kısmı yerleştiriyoruz
        top_layout.addWidget(self.assembly_text)
        top_layout.addWidget(self.machine_code_text)
        top_layout.addWidget(self.register_text)

        # Alt kısmı oluşturuyoruz (IM ve DM memoryler)
        bottom_layout = QHBoxLayout()

        # IM (Instruction Memory) kısmı
        self.im_text = QTextEdit(self)
        self.im_text.setPlaceholderText("Instruction Memory (IM)...")
        self.im_text.setStyleSheet("background-color: #444444;")
        self.im_text.setFixedHeight(200)

        # DM (Data Memory) kısmı
        self.dm_text = QTextEdit(self)
        self.dm_text.setPlaceholderText("Data Memory (DM)...")
        self.dm_text.setStyleSheet("background-color: #444444;")
        self.dm_text.setFixedHeight(200)

        # Alt kısmı yerleştiriyoruz
        bottom_layout.addWidget(self.im_text)
        bottom_layout.addWidget(self.dm_text)

        # Buton kısmı (isteğe bağlı, çalıştırma gibi)
        self.execute_button = QPushButton("Çalıştır", self)
        self.execute_button.setStyleSheet("background-color: #555555; color: white;")
        self.execute_button.clicked.connect(self.execute_code)

        # Ana layout'a üst ve alt kısımları ekliyoruz
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)
        main_layout.addWidget(self.execute_button)

        self.setLayout(main_layout)

    def execute_code(self):
        # Kodu çalıştırma butonuna tıklanınca yapılacak işlem
        print("Assembly Kodu:\n", self.assembly_text.toPlainText())
        print("Makine Kodu:\n", self.machine_code_text.toPlainText())
        print("Registerlar:\n", self.register_text.toPlainText())
        print("Instruction Memory (IM):\n", self.im_text.toPlainText())
        print("Data Memory (DM):\n", self.dm_text.toPlainText())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AssemblyEditorApp()
    window.show()
    sys.exit(app.exec_())
