import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMainWindow, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image
import os

import qtpy

#The windows that showed up at application launch
class MainWindows(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.add_window = None

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
        btn_ajouter = QPushButton('Add', self)
        btn_modifier = QPushButton('Modify', self)
        btn_supprimer = QPushButton('Delete', self)
        btn_classement = QPushButton('Ladder', self)
        # Aggrandissement des boutons
        btn_ajouter.resize(150, 75)
        btn_modifier.resize(150, 75)
        btn_supprimer.resize(150, 75)
        btn_classement.resize(150, 75)
        # Placer les boutons dans la fenêtre
        btn_ajouter.move(770, 100)
        btn_modifier.move(770, 225)
        btn_supprimer.move(770, 350)
        btn_classement.move(770, 475)
        # Changement de la taille du texte des boutons
        font = btn_ajouter.font()
        font.setPointSize(13)
        btn_ajouter.setFont(font)
        btn_modifier.setFont(font)
        btn_supprimer.setFont(font)
        btn_classement.setFont(font)
        # Connecter le signal clicked des boutons à des méthodes
        btn_ajouter.clicked.connect(self.on_btn_ajouter_clicked)
        btn_modifier.clicked.connect(self.on_btn_modifier_clicked)
        btn_supprimer.clicked.connect(self.on_btn_supprimer_clicked)
        btn_classement.clicked.connect(self.on_btn_classement_clicked)

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def on_btn_ajouter_clicked(self):
        if self.add_window is None:  # Vérifier si la fenêtre existe déjà
            self.add_window = AddWindows()
        self.add_window.show()
    
    def on_btn_modifier_clicked(self, event):
        print('1')

    def on_btn_supprimer_clicked(self, event):
        print('3')

    def on_btn_classement_clicked(self, event):
        print('4')

#The windows that show up when click on "Ajouter"
class AddWindows(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #Fenêtre de base de l'écran
        self.setWindowTitle('Wrestling Elo Simulator')
        self.resize(1400, 700)
        self.center()

        # Création du label
        label = QLabel('Add', self)
        label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        font = label.font()
        font.setBold(True)
        font.setPointSize(24)
        label.setFont(font)

        # Ajout du label au layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        # Création des boutons
        btn_wrestler = QPushButton('Wrestler', self)
        btn_tag_team = QPushButton('Tag-Team', self)
        btn_stable = QPushButton('Stable', self)
        btn_federation = QPushButton('Federation', self)
        btn_event = QPushButton('Event', self)
        btn_tag_title = QPushButton('Title', self)
        btn_match = QPushButton('Match', self)
        # Aggrandissement des boutons
        btn_wrestler.resize(150, 75)
        btn_tag_team.resize(150, 75)
        btn_stable.resize(150, 75)
        btn_federation.resize(150, 75)
        btn_event.resize(150, 75)
        btn_tag_title.resize(150, 75)
        btn_match.resize(600, 75)
        # Placer les boutons dans la fenêtre
        btn_wrestler.move(400, 150)
        btn_tag_team.move(850, 150)
        btn_stable.move(400, 275)
        btn_federation.move(850, 275)
        btn_event.move(400, 400)
        btn_tag_title.move(850, 400)
        btn_match.move(400, 525)

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

def createInterface():
    app = QApplication(sys.argv)
    widget = MainWindows()
    widget.show()
    sys.exit(app.exec_())
