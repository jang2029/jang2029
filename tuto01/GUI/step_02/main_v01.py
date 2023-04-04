import sys, os
import PyQt5
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *




class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        layout_attacker = QHBoxLayout()
        layout_midfielder = QHBoxLayout()
        layout_defender = QHBoxLayout()

        W_1 = QPushButton('Widget_1')
        W_2 = QPushButton('Widget_2')
        W_3 = QPushButton('Widget_3')
        W_4 = QPushButton('Widget_4')
        W_5 = QPushButton('Widget_5')
        W_6 = QPushButton('Widget_6')
        W_7 = QPushButton('Widget_7')
        W_8 = QPushButton('Widget_8')
        W_9 = QPushButton('Widget_9')
        W_10 = QPushButton('Widget_10')
        W_11 = QPushButton('Widget_11')
        
        layout_attacker.addWidget(W_1)
        layout_attacker.addWidget(W_2)
        layout_attacker.addWidget(W_3)

        layout_midfielder.addWidget(W_4)
        layout_midfielder.addWidget(W_5)
        layout_midfielder.addWidget(W_6)

        layout_defender.addWidget(W_7)
        layout_defender.addWidget(W_8)
        layout_defender.addWidget(W_9)
        layout_defender.addWidget(W_10)

        main_layout.addLayout(layout_attacker)
        main_layout.addLayout(layout_midfielder)
        main_layout.addLayout(layout_defender)
        main_layout.addWidget(W_11)

        self.setLayout(main_layout)
        self.resize(170, 300)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
    