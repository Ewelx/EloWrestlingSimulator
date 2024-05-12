import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton 
import sys
import windows.AddWindows as AddWindows

# The windows that showed up at application launch
class MainWindows(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.add_window = None

    def initUI(self):
        # Base screen window
        self.setWindowTitle('Wrestling Elo Simulator')
        self.setFixedSize(1725, 800)
        self.center()

        # Charge the picture as a pixmap
        image_path = os.path.join("Images", "Fond", "resized_WES.png")
        pixmap = QPixmap(image_path)

        # Create a label to display the picture
        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setGeometry(0, 0, self.width(), self.height())

        # Button creation
        btn_add = QPushButton('Add', self)
        btn_modify = QPushButton('Modify', self)
        btn_delete = QPushButton('Delete', self)
        btn_ladder = QPushButton('Ladder', self)

        # Enlargement of the buttons
        btn_add.resize(150, 75)
        btn_modify.resize(150, 75)
        btn_delete.resize(150, 75)
        btn_ladder.resize(150, 75)

        # Placement of the buttons in the window
        btn_add.move(770, 100)
        btn_modify.move(770, 225)
        btn_delete.move(770, 350)
        btn_ladder.move(770, 475)

        # Change buttons font-size
        font = btn_add.font()
        font.setPointSize(13)
        btn_add.setFont(font)
        btn_modify.setFont(font)
        btn_delete.setFont(font)
        btn_ladder.setFont(font)

        # Connect clicked event of buttons to method (that will permit reach next windows)
        btn_add.clicked.connect(self.on_btn_add_clicked)
        btn_modify.clicked.connect(self.on_btn_modify_clicked)
        btn_delete.clicked.connect(self.on_btn_delete_clicked)
        btn_ladder.clicked.connect(self.on_btn_ladder_clicked)

    # Center the window
    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    # When the button 'Add' is clicked
    def on_btn_add_clicked(self):
        # Display 'add_window' window
        if self.add_window is None:  # Vérify if the window already exist
            self.add_window = AddWindows.AddWindows()
            self.add_window.show()
    
    # When the button 'Modify' is clicked
    def on_btn_modify_clicked(self):
        print('TODO : Modify')

    # When the button 'Delete' is clicked
    def on_btn_delete_clicked(self):
        print('TODO : Delete')

    # When the button 'Ladder' is clicked
    def on_btn_ladder_clicked(self):
        print('TODO : Ladder')

# Create the interface
def createInterface():
    app = QApplication(sys.argv)
    widget = MainWindows()
    widget.show()
    sys.exit(app.exec_())
