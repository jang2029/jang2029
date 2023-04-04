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

        label_widget = QLabel('Hello World!')
        button_widget = QPushButton('Click Me')


        combobox_widget = QComboBox()
        combobox_widget.addItem('Python')
        combobox_widget.addItem('C')
        combobox_widget.addItem('C++')
        combobox_widget.addItem('Fortran')
        combobox_widget.addItem('Basic')



        check_box_widget_summer = QCheckBox('Summer')
        check_box_widget_winter = QCheckBox('Winter')

        radio_button_widget_male = QRadioButton('Male')
        radio_button_widget_female = QRadioButton('Female')

        spinbox_widget = QSpinBox()

        date_widget = QDateEdit()
        time_widget = QTimeEdit()



        list_widget = QListWidget()
        item_1 = QListWidgetItem('Cat')
        item_2 = QListWidgetItem('Dog')
        list_widget.addItem(item_1)
        list_widget.addItem(item_2)




        main_layout.addWidget(label_widget)
        main_layout.addWidget(button_widget)
        main_layout.addWidget(combobox_widget)
        main_layout.addWidget(check_box_widget_summer)
        main_layout.addWidget(check_box_widget_winter)
        main_layout.addWidget(radio_button_widget_male)
        main_layout.addWidget(radio_button_widget_female)
        main_layout.addWidget(spinbox_widget)
        main_layout.addWidget(date_widget)
        main_layout.addWidget(time_widget)
        main_layout.addWidget(list_widget)



        self.setLayout(main_layout)

        self.resize(170, 300)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
    