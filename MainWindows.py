import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PIL import Image
import os

class MainWindows(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #Fenêtre de base de l'écran
        self.setWindowTitle('Wrestling Elo Simulator')
        self.resize(1725, 800)
        self.center()

        # Charger l'image en tant que pixmap
        image_path = os.path.join("Images", "Fond", "resized_WES.png")
        pixmap = QPixmap(image_path)

        # Créer un label pour afficher l'image
        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setGeometry(0, 0, self.width(), self.height())

        # Création des boutons
        btn_explorer = QPushButton('Explorer', self)
        btn_ajouter = QPushButton('Ajouter', self)
        btn_supprimer = QPushButton('Supprimer', self)
        btn_classement = QPushButton('Classement', self)
        # Aggrandissement des boutons
        btn_explorer.resize(150, 75)
        btn_ajouter.resize(150, 75)
        btn_supprimer.resize(150, 75)
        btn_classement.resize(150, 75)
        # Placer les boutons dans la fenêtre
        btn_explorer.move(770, 100)
        btn_ajouter.move(770, 225)
        btn_supprimer.move(770, 350)
        btn_classement.move(770, 475)
        # Changement de la taille du texte des boutons
        font = btn_explorer.font()
        font.setPointSize(13)
        btn_explorer.setFont(font)
        btn_ajouter.setFont(font)
        btn_supprimer.setFont(font)
        btn_classement.setFont(font)
        # Connecter le signal clicked des boutons à des méthodes
        btn_explorer.clicked.connect(self.on_btn_explorer_clicked)
        btn_ajouter.clicked.connect(self.on_btn_ajouter_clicked)
        btn_supprimer.clicked.connect(self.on_btn_supprimer_clicked)
        btn_classement.clicked.connect(self.on_btn_classement_clicked)

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def on_btn_explorer_clicked(self, event):
        print('1')

    def on_btn_ajouter_clicked(self, event):
        print('2')

    def on_btn_supprimer_clicked(self, event):
        print('3')

    def on_btn_classement_clicked(self, event):
        print('4')

def createInterface():
    app = QApplication(sys.argv)
    widget = MainWindows()
    widget.show()
    sys.exit(app.exec_())
