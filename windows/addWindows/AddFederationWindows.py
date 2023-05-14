from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QComboBox, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
import pyodbc

#The windows that show up when click on "Ajouter"
class AddFederationWindows(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #Fenêtre de base de l'écran
        self.setWindowTitle('Wrestling Elo Simulator')
        self.resize(1400, 700)
        self.center()

        # Création du label
        label = QLabel('Add federation', self)
        label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        font = label.font()
        font.setBold(True)
        font.setPointSize(24)
        label.setFont(font)

        # Ajout du label au layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        # Acronyme de la federation
        lbl_acronym = QLabel('Acronym (5) * :', self)
        lbl_acronym.move(560, 210)
        self.txt_acronym = QLineEdit(self)
        self.txt_acronym.move(560, 240)
        self.txt_acronym.resize(280, 30)

        # Nom de la federation
        lbl_name = QLabel('Name * :', self)
        lbl_name.move(560, 270)
        self.txt_name = QLineEdit(self)
        self.txt_name.move(560, 300)
        self.txt_name.resize(280, 30)

        # Nationnalité de la federation
        lbl_nationality = QLabel('Nationalité * :', self)
        lbl_nationality.move(560, 330)
        self.cmb_nationality = QComboBox(self)
        self.cmb_nationality.move(560, 360)
        self.cmb_nationality.resize(280, 30)

        #Boutton permettant d'ajouter la federation 
        btn_add = QPushButton('Ajouter', self)
        btn_add.move(600, 450)
        btn_add.clicked.connect(self.submit_federation_clicked)

        #Requête permettant  de récupérer l'ensemble des nationnalités
        server = 'PIERRENOTE\MSSQLSERVER01'
        database = 'WrestlingEloDB'
    
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                           SERVER=' + server + '; \
                           DATABASE=' + database +';\
                           Trusted_Connection=yes;')
        
        cursor = cnxn.cursor()
        query = "SELECT NationalityName FROM Nationalities"
        cursor.execute(query)

        results = cursor.fetchall()

        #Ajoute les nationnalités dans le menu déroulant
        for row in results:
            self.cmb_nationality.addItem(row[0])
       
    def submit_federation_clicked(self):
        acronym = self.txt_acronym.text()
        name = self.txt_name.text()
        nationality = self.cmb_nationality.currentText()

        # Vérifier que tous les champs sont remplis
        if acronym and name and nationality:
            # Insérer la nouvelle fédération dans la base de données
            server = 'PIERRENOTE\MSSQLSERVER01'
            database = 'WrestlingEloDB'
            cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                               SERVER=' + server + '; \
                               DATABASE=' + database +';\
                               Trusted_Connection=yes;')
            cursor = cnxn.cursor()
            query = "INSERT INTO Federations (FederationName, FederationAcronym, FederationNationality, FederationActive) VALUES (?, ?, ?, 1)"
            cursor.execute(query, (acronym, name, nationality))
            cnxn.commit()

            # Afficher un message de confirmation
            msg_box = QMessageBox()
            msg_box.setText("La fédération a été ajoutée avec succès.")
            msg_box.exec_()
        else:
            # Afficher un message d'erreur si un champ est manquant
            msg_box = QMessageBox()
            msg_box.setText("Veuillez remplir tous les champs.")
            msg_box.exec_()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())