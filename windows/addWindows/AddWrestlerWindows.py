from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QComboBox, QPushButton, QMessageBox, QDateTimeEdit, QListWidget, QCheckBox
from PyQt5.QtCore import Qt
import pyodbc
import sys
sys.path.insert(1, '/')
import BDConnection

class AddWrestlerWindows(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #Fenêtre de base de l'écran
        self.setWindowTitle('Wrestling Elo Simulator')
        self.setFixedSize(1400, 700)
        self.center()

        # Création du label
        label = QLabel('Add Wrestler', self)
        label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        font = label.font()
        font.setBold(True)
        font.setPointSize(24)
        label.setFont(font)

        # Ajout du label au layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        # Nom du catcheur
        lbl_name = QLabel('Name * :', self)
        lbl_name.move(280, 150)
        self.txt_name = QLineEdit(self)
        self.txt_name.move(280, 180)
        self.txt_name.resize(280, 30)

        # Genre du catcheur
        lbl_gender = QLabel('Gender * :', self)
        lbl_gender.move(280, 210)
        self.cmb_gender = QComboBox(self)
        self.cmb_gender.addItem("Man")
        self.cmb_gender.addItem("Woman")
        self.cmb_gender.move(280, 240)
        self.cmb_gender.resize(280, 30)

        # Nationalité du catcheur
        lbl_country = QLabel('Nationality * :', self)
        lbl_country.move(280, 270)
        self.cmb_country = QComboBox(self)
        self.cmb_country.move(280, 300)
        self.cmb_country.resize(280, 30)

        # Date de naissance du catcheur
        lbl_date_of_birth = QLabel('Date of birth * :', self)
        lbl_date_of_birth.move(280, 330)
        self.date_of_birth_edit = QDateTimeEdit(self)
        self.date_of_birth_edit.setCalendarPopup(True)  # Affiche un calendrier lors de la sélection
        self.date_of_birth_edit.setDisplayFormat("yyyy-MM-dd")  # Format d'affichage de la date
        self.date_of_birth_edit.move(280, 360)
        self.date_of_birth_edit.resize(280, 30)

        # Alignement du catcheur
        lbl_alignment = QLabel('Alignment * :', self)
        lbl_alignment.move(280, 390)
        self.cmb_alignment = QComboBox(self)
        self.cmb_alignment.addItem("Face")
        self.cmb_alignment.addItem("Heel")
        self.cmb_alignment.addItem("Tweener")
        self.cmb_alignment.move(280, 420)
        self.cmb_alignment.resize(280, 30)

        # Activité du catcheur
        lbl_active = QLabel('Active wrestler * :', self)
        lbl_active.move(840, 150)
        self.chk_active = QCheckBox(self)
        self.chk_active.setChecked(True)  # Coché par défaut
        self.chk_active.move(840, 180)

        # Note cagematch du catcheur
        lbl_cagematch = QLabel('Cagematch rating :', self)
        lbl_cagematch.move(840, 210)
        lbl_cagematch.resize(280, 20)
        self.txt_cagematch = QLineEdit(self)
        self.txt_cagematch.move(840, 240)
        self.txt_cagematch.resize(280, 30)

        # Theme du catcheur
        lbl_theme = QLabel('Theme :', self)
        lbl_theme.move(840, 270)
        self.txt_theme = QLineEdit(self)
        self.txt_theme.move(840, 300)
        self.txt_theme.resize(280, 30)

        # Federations ayant organisé l'évènement
        lbl_federation = QLabel('Federation(s) * :', self)
        lbl_federation.move(840, 330)
        self.lst_federation = QListWidget(self)
        self.lst_federation.move(840, 360)
        self.lst_federation.resize(280, 100)
        self.lst_federation.setSelectionMode(QListWidget.MultiSelection)

        # Boutton permettant d'ajouter l'évènement 
        btn_add = QPushButton('Add', self)
        btn_add.move(650, 720)
        btn_add.clicked.connect(self.submit_wrestler_clicked)

        # Requête permettant  de récupérer l'ensemble des nationnalités
        cnxn = BDConnection.BDConnection()
        
        cursor = cnxn.cursor()

        query = "SELECT NationalityName FROM Nationalities"
        cursor.execute(query)

        results = cursor.fetchall()

        # Ajoute les nationnalités dans le menu déroulant
        for row in results:
            self.cmb_country.addItem(row[0])

        query = "SELECT FederationName FROM Federations"
        cursor.execute(query)

        results = cursor.fetchall()

        # Ajoute les fédérations dans le menu déroulant
        for row in results:
            self.lst_federation.addItem(row[0])
       
    def submit_wrestler_clicked(self):
        # Connection à la BD
        cnxn = BDConnection.BDConnection()
        cursor = cnxn.cursor()
        
        # préparation des paramètres de la bd
        name = self.txt_name.text()
        gender = self.cmb_gender.currentText()
        country = self.cmb_country.currentText()
        selected_date_of_birth = self.date_of_birth_edit.dateTime()  # Récupérer la date et l'heure sélectionnées
        formatted_date = selected_date_of_birth.toString("yyyy-MM-dd HH:mm:ss")  # Formater la date dans le format datetime de SQL
        alignement = self.cmb_alignment.currentText()
        active = self.chk_active.isChecked()
        cagematch = self.txt_cagematch.text()
        theme = self.txt_theme.text()
        federations = self.lst_federation.selectedItems()
        federations = [item.text() for item in federations]
            
        # Requête pour récuperer les ID des fédérations ayant organisé l'évènement
        query = "SELECT FederationID FROM Federations WHERE FederationName IN ({})"
        formatted_query = query.format(",".join(["'{}'".format(federation) for federation in federations]))
        cursor.execute(formatted_query)
        federations = [row[0] for row in cursor.fetchall()]  # Liste des IDs de fédérations

        # Requête pour récupérer l'ID du pays
        query = "SELECT NationalityID FROM Nationalities WHERE NationalityName = '{}'"
        formatted_query = query.format(country)
        cursor.execute(formatted_query)
        country = cursor.fetchone()[0]  # Récupérer la première colonne du résultat

        # Vérifier que tous les champs sont remplis
        if name and gender and country and formatted_date:
            if active is True:
                active = 1
            else:
                active = 0
            if cagematch == "":
                self.insert_wrestler(cursor, cnxn, name, gender, country, formatted_date, alignement, active, -1.0, theme, federations)
            else:
                try:
                    cagematch = float(cagematch)
                except ValueError:
                    # Afficher un message d'erreur
                    msg_box = QMessageBox()
                    msg_box.setText("La forme de la note est invalide.")
                    msg_box.exec_()
                    return
                if cagematch > 0 or cagematch < 10:
                    self.insert_wrestler(cursor, cnxn, name, gender, country, formatted_date, alignement, active, cagematch, theme, federations)
                else:
                    # Afficher un message d'erreur si un champ est manquant
                    msg_box = QMessageBox()
                    msg_box.setText("The cagematch rating is unvalid (it should be between 0 and 10)")
                    msg_box.exec_()
        else:
            # Afficher un message d'erreur si un champ est manquant
            msg_box = QMessageBox()
            msg_box.setText("Please fill in all required fields.")
            msg_box.exec_()

    def insert_wrestler(cursor, cnxn, name, gender, country, formatted_date, alignement, active, cagematch, theme, federations):
        # Insérer la nouvelle fédération dans la base de données
        query = "INSERT INTO Wrestler (WrestlerName, WrestlerGender, WrestlerNationalityID, WrestlerDateOfBirth, WrestlerAlignment, WrestlerActive, EventCagematchRating, EventTheme) VALUES ('{}', '{}', {}, {}, '{}')"
        formatted_query = query.format(name, gender, country, "'" + formatted_date + "'", alignement, active, cagematch, theme)
        cursor.execute(formatted_query)
        cnxn.commit()

        # Récupération de l'ID de l'événement inséré
        query = "SELECT MAX(WrestlerID) FROM Wrestlers"
        cursor.execute(query)
        wrestler_id = cursor.fetchone()[0]

        # Sauvegarde de la query
        with open('BD/InsertWrestlersEloDB.sql', 'a') as file:
            file.write(formatted_query + "\n")
        file.close()
        
        for federation_id in federations:
            query = "INSERT INTO HasOrganisedEvent (EventID, FederationID) VALUES ('{}', '{}')"
            formatted_query = query.format(wrestler_id, federation_id)
            cursor.execute(formatted_query)
            cnxn.commit()

            # Sauvegarde de la query
            with open('BD/InsertIsPartFederation.sql', 'a') as file:
                file.write(formatted_query + "\n")
            file.close()

        # Afficher un message de confirmation
        msg_box = QMessageBox()
        msg_box.setText("The wrestler have been added.")
        msg_box.exec_()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())