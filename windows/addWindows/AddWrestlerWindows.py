from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QCheckBox, QComboBox, QDateTimeEdit, QLabel, QLineEdit, QListWidget, QMessageBox, QPushButton, QVBoxLayout, QWidget
import sys
sys.path.insert(1, '/')
import DBConnection

class AddWrestlerWindows(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Base screen window
        self.setWindowTitle('Wrestling Elo Simulator')
        self.setFixedSize(1400, 700)
        self.center()

        # Label creation
        label = QLabel('Add Wrestler', self)
        label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        font = label.font()
        font.setBold(True)
        font.setPointSize(24)
        label.setFont(font)

        # Adding the label to the layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        # Name of the wrestler
        lbl_name = QLabel('Name * :', self)
        lbl_name.move(280, 150)
        self.txt_name = QLineEdit(self)
        self.txt_name.move(280, 180)
        self.txt_name.resize(280, 30)

        # Gender of the wrestler
        lbl_gender = QLabel('Gender :', self)
        lbl_gender.move(280, 210)
        self.cmb_gender = QComboBox(self)
        self.cmb_gender.addItem("Man")
        self.cmb_gender.addItem("Woman")
        self.cmb_gender.move(280, 240)
        self.cmb_gender.resize(280, 30)

        # Nationalities of the wrestler
        lbl_nationality = QLabel('Nationality * :', self)
        lbl_nationality.move(280, 270)
        self.lst_nationality = QListWidget(self)
        self.lst_nationality.move(280, 300)
        self.lst_nationality.resize(280, 100)
        self.lst_nationality.setSelectionMode(QListWidget.MultiSelection)

        # Birthday of the wrestler
        lbl_date_of_birth = QLabel('Date of birth :', self)
        lbl_date_of_birth.move(280, 400)
        self.date_of_birth_edit = QDateTimeEdit(self)
        self.date_of_birth_edit.setCalendarPopup(True)  # Show a calender
        self.date_of_birth_edit.setDisplayFormat("yyyy-MM-dd")  # Format of the date
        self.date_of_birth_edit.move(280, 430)
        self.date_of_birth_edit.resize(280, 30)

        # Alignment of the wrestler
        lbl_alignment = QLabel('Alignment * :', self)
        lbl_alignment.move(280, 460)
        self.cmb_alignment = QComboBox(self)
        self.cmb_alignment.addItem("Face")
        self.cmb_alignment.addItem("Heel")
        self.cmb_alignment.addItem("Tweener")
        self.cmb_alignment.move(280, 490)
        self.cmb_alignment.resize(280, 30)

        # If the wrestler is still active
        lbl_active = QLabel('Active wrestler :', self)
        lbl_active.move(840, 150)
        self.chk_active = QCheckBox(self)
        self.chk_active.setChecked(True)  # Selectionned at display
        self.chk_active.move(840, 180)

        # Cagematch rating of the wrestler
        lbl_cagematch = QLabel('Cagematch rating :', self)
        lbl_cagematch.move(840, 210)
        lbl_cagematch.resize(280, 20)
        self.txt_cagematch = QLineEdit(self)
        self.txt_cagematch.move(840, 240)
        self.txt_cagematch.resize(280, 30)

        # Theme of the wrestler
        lbl_theme = QLabel('Theme :', self)
        lbl_theme.move(840, 270)
        self.txt_theme = QLineEdit(self)
        self.txt_theme.move(840, 300)
        self.txt_theme.resize(280, 30)

        # Federations where the wrestler is
        lbl_federation = QLabel('Federation(s) * :', self)
        lbl_federation.move(840, 330)
        self.lst_federation = QListWidget(self)
        self.lst_federation.move(840, 360)
        self.lst_federation.resize(280, 100)
        self.lst_federation.setSelectionMode(QListWidget.MultiSelection)

        # Button that permit to add the wrestler 
        btn_add = QPushButton('Add', self)
        btn_add.move(650, 550)
        btn_add.clicked.connect(self.submit_wrestler_clicked)

        # Connection to the DB
        cnxn = DBConnection.DBConnection()
        
        cursor = cnxn.cursor()

        # Request to get all nationalities
        query = "SELECT NationalityName FROM Nationalities"
        cursor.execute(query)

        results = cursor.fetchall()

        # Add nationalities to the dropdown menu
        for row in results:
            self.lst_nationality.addItem(row[0])

        # Request to get all federations
        query = "SELECT FederationName FROM Federations"
        cursor.execute(query)

        results = cursor.fetchall()

        # Add federations to the dropdown menu
        for row in results:
            self.lst_federation.addItem(row[0])
    
    # When the add button is pressed
    def submit_wrestler_clicked(self):
        # Connection to the DB
        cnxn = DBConnection.DBConnection()
        cursor = cnxn.cursor()
        
        # Preparate attributes of the new wrestler
        name = self.txt_name.text()
        gender = self.cmb_gender.currentText()
        nationalities = self.lst_nationality.selectedItems()
        nationalities = [item.text() for item in nationalities]
        selected_date_of_birth = self.date_of_birth_edit.dateTime() # Get date and hours
        formatted_date = selected_date_of_birth.toString("yyyy-MM-dd HH:mm:ss") # Format date to SQL datetime
        alignement = self.cmb_alignment.currentText()
        active = self.chk_active.isChecked()
        cagematch = self.txt_cagematch.text()
        theme = self.txt_theme.text()
        federations = self.lst_federation.selectedItems()
        federations = [item.text() for item in federations]

        # SQL request to get all countries ID
        query = "SELECT NationalityID FROM Nationalities WHERE NationalityName IN ({})"
        formatted_query = query.format(",".join(["'{}'".format(nationality) for nationality in nationalities]))
        cursor.execute(formatted_query)
        nationalities = [row[0] for row in cursor.fetchall()]
            
        # SQL request to get all federations ID
        query = "SELECT FederationID FROM Federations WHERE FederationName IN ({})"
        formatted_query = query.format(",".join(["'{}'".format(federation) for federation in federations]))
        cursor.execute(formatted_query)
        federations = [row[0] for row in cursor.fetchall()] # Get all results

        # Verify that all required fields are filled
        if name and nationalities and federations:
            if active is True:
                active = 1
            else:
                active = 0
            if cagematch == "":
                self.insert_wrestler(cursor, cnxn, name, gender, nationalities, formatted_date, alignement, active, -1.0, theme, federations)
            else:
                try:
                    cagematch = float(cagematch)
                except ValueError:
                    # Show an error message if we can't float cast 
                    msg_box = QMessageBox()
                    msg_box.setText("The cagematch rating is invalid (exemple of rating : 5.01)")
                    msg_box.exec_()
                    return
                if cagematch > 0 or cagematch < 10:
                    self.insert_wrestler(cursor, cnxn, name, gender, nationalities, formatted_date, alignement, active, cagematch, theme, federations)
                else:
                    # Show an error message if the cagematch rating isn't between 0 and 10 (include)
                    msg_box = QMessageBox()
                    msg_box.setText("The cagematch rating is unvalid (it should be between 0 and 10)")
                    msg_box.exec_()
        else:
            # Show an error message if one of required field isn't filled
            msg_box = QMessageBox()
            msg_box.setText("Please fill in all required fields.")
            msg_box.exec_()

    # Function to insert the wrestler into the database
    def insert_wrestler(self, cursor, cnxn, name, gender, nationalities, formatted_date, alignement, active, cagematch, theme, federations):
        query = "INSERT INTO Wrestlers (WrestlerName, WrestlerGender, WrestlerDateOfBirth, WrestlerAlignment, WrestlerActive, WrestlerCagematchRating, WrestlerTheme) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')"
        formatted_query = query.format(name, gender, formatted_date, alignement, active, cagematch, theme)
        cursor.execute(formatted_query)
        cnxn.commit()

        # Get the ID of the new wrestler
        query = "SELECT MAX(WrestlerID) FROM Wrestlers"
        cursor.execute(query)
        wrestler_id = cursor.fetchone()[0]

        # Save the query in a file
        with open('BD/InsertWrestlersEloDB.sql', 'a') as file:
            file.write(formatted_query + "\n")
        file.close()

        # Insert all the nationalities associated with the wrestler
        for nationality_id in nationalities:
            query = "INSERT INTO HaveNationality (WrestlerID, NationalityID) VALUES ('{}', '{}')"
            formatted_query = query.format(wrestler_id, nationality_id)
            cursor.execute(formatted_query)
            cnxn.commit()

            # Save the query in a file
            with open('BD/InsertHaveNationality.sql', 'a') as file:
                file.write(formatted_query + "\n")
            file.close()
        
        # Insert all the federations associated with the wrestler
        for federation_id in federations:
            query = "INSERT INTO IsPartFederation (WrestlerID, FederationID) VALUES ('{}', '{}')"
            formatted_query = query.format(wrestler_id, federation_id)
            cursor.execute(formatted_query)
            cnxn.commit()

            # Save the query in a file
            with open('BD/InsertIsPartFederation.sql', 'a') as file:
                file.write(formatted_query + "\n")
            file.close()

        # Show a confirmation message
        msg_box = QMessageBox()
        msg_box.setText("The wrestler have been added.")
        msg_box.exec_()

    # Center the window
    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())