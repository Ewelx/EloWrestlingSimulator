from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QComboBox, QPushButton, QMessageBox, QDateTimeEdit, QListWidget
from PyQt5.QtCore import Qt
import pyodbc
import sys
sys.path.insert(1, '/')
import BDConnection

class AddEventWindows(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #Fenêtre de base de l'écran
        self.setWindowTitle('Wrestling Elo Simulator')
        self.resize(1400, 700)
        self.center()

        # Création du label
        label = QLabel('Add Event', self)
        label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        font = label.font()
        font.setBold(True)
        font.setPointSize(24)
        label.setFont(font)

        # Ajout du label au layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        # Nom de l'évenement
        lbl_name = QLabel('Name * :', self)
        lbl_name.move(560, 150)
        self.txt_name = QLineEdit(self)
        self.txt_name.move(560, 180)
        self.txt_name.resize(280, 30)

        # Pays ou a lieu l'évènement
        lbl_country = QLabel('Country * :', self)
        lbl_country.move(560, 210)
        self.cmb_country = QComboBox(self)
        self.cmb_country.move(560, 240)
        self.cmb_country.resize(280, 30)

        # Date de l'évènement
        lbl_date = QLabel('Date * :', self)
        lbl_date.move(560, 270)
        self.date_edit = QDateTimeEdit(self)
        self.date_edit.setCalendarPopup(True)  # Affiche un calendrier lors de la sélection
        self.date_edit.setDisplayFormat("yyyy-MM-dd")  # Format d'affichage de la date
        self.date_edit.move(560, 300)
        self.date_edit.resize(280, 30)

        # Note cagematch de l'évènement
        lbl_cagematch = QLabel('Cagematch rating * :', self)
        lbl_cagematch.move(560, 330)
        self.txt_cagematch = QLineEdit(self)
        self.txt_cagematch.move(560, 360)
        self.txt_cagematch.resize(280, 30)

        # Note cagematch de l'évènement
        lbl_theme = QLabel('Theme :', self)
        lbl_theme.move(560, 390)
        self.txt_theme = QLineEdit(self)
        self.txt_theme.move(560, 420)
        self.txt_theme.resize(280, 30)

        # Federations ayant organisé l'évènement
        lbl_federation = QLabel('Federation(s) * :', self)
        lbl_federation.move(560, 450)
        self.lst_federation = QListWidget(self)
        self.lst_federation.move(560, 480)
        self.lst_federation.resize(280, 100)
        self.lst_federation.setSelectionMode(QListWidget.MultiSelection)

        # Boutton permettant d'ajouter l'évènement 
        btn_add = QPushButton('Add', self)
        btn_add.move(650, 610)
        btn_add.clicked.connect(self.submit_federation_clicked)

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
       
    def submit_federation_clicked(self):
        # Connection à la BD
        cnxn = BDConnection.BDConnection()
        cursor = cnxn.cursor()

        # préparation des paramètres de la bd
        name = self.txt_name.text()
        country = self.cmb_country.currentText()
        selected_date = self.date_edit.dateTime()  # Récupérer la date et l'heure sélectionnées
        formatted_date = selected_date.toString("yyyy-MM-dd HH:mm:ss")  # Formater la date dans le format datetime de SQL
        cagematch = self.txt_cagematch.text()
        theme = self.txt_theme.text()
        federations = self.lst_federation.selectedItems()
        federations = [item.text() for item in federations]

        if(len(federations) == 0):
            federations.append('Unknown')
            
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
        if name and country and formatted_date and cagematch:
            try:
                cagematch = float(cagematch)
            except ValueError:
                # Afficher un message d'erreur
                msg_box = QMessageBox()
                msg_box.setText("La forme de la note est invalide.")
                msg_box.exec_()
                return
            if cagematch > 0 or cagematch < 10:
                # Insérer la nouvelle fédération dans la base de données
                query = "INSERT INTO Events (EventName, EventCountryID, EventDate, EventCagematchRating, EventTheme) VALUES ('{}', '{}', {}, {}, '{}')"
                formatted_query = query.format(name, country, "'" + formatted_date + "'", cagematch, theme)
                cursor.execute(formatted_query)
                cnxn.commit()

                # Récupération de l'ID de l'événement inséré
                query = "SELECT MAX(EventID) FROM Events"
                cursor.execute(query)
                event_id = cursor.fetchone()[0]

                # Sauvegarde de la query
                with open('BD/InsertEventsEloDB.sql', 'a') as file:
                    file.write(formatted_query + "\n")
                file.close()
                
                for federation_id in federations:
                    query = "INSERT INTO HasOrganisedEvent (EventID, FederationID) VALUES ('{}', '{}')"
                    formatted_query = query.format(event_id, federation_id)
                    cursor.execute(formatted_query)
                    cnxn.commit()

                    # Sauvegarde de la query
                    with open('BD/InsertHasOrganisedEvent.sql', 'a') as file:
                        file.write(formatted_query + "\n")
                    file.close()

                # Afficher un message de confirmation
                msg_box = QMessageBox()
                msg_box.setText("The event have been added.")
                msg_box.exec_()
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

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())