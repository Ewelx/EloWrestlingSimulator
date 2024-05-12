from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QComboBox, QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout, QWidget
import sys
sys.path.insert(1, '/')
import DBConnection

class AddFederationWindows(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Base screen window
        self.setWindowTitle('Wrestling Elo Simulator')
        self.setFixedSize(1400, 700)
        self.center()

        # Label creation
        label = QLabel('Add federation', self)
        label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        font = label.font()
        font.setBold(True)
        font.setPointSize(24)
        label.setFont(font)

        # Adding the label to the layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        # Acronym of the federation
        lbl_acronym = QLabel('Acronym (5) * :', self)
        lbl_acronym.move(560, 210)
        self.txt_acronym = QLineEdit(self)
        self.txt_acronym.move(560, 240)
        self.txt_acronym.resize(280, 30)

        # Name of the federation
        lbl_name = QLabel('Name * :', self)
        lbl_name.move(560, 270)
        self.txt_name = QLineEdit(self)
        self.txt_name.move(560, 300)
        self.txt_name.resize(280, 30)

        # Nationality of the federation
        lbl_nationality = QLabel('Nationality * :', self)
        lbl_nationality.move(560, 330)
        self.cmb_nationality = QComboBox(self)
        self.cmb_nationality.move(560, 360)
        self.cmb_nationality.resize(280, 30)

        # Button that permit to add the federation
        btn_add = QPushButton('Add', self)
        btn_add.move(650, 450)
        btn_add.clicked.connect(self.submit_federation_clicked)

        # Connection to the DB
        cnxn = DBConnection.BDConnection()
        
        cursor = cnxn.cursor()

        # Request to get all nationalities
        query = "SELECT NationalityName FROM Nationalities"
        cursor.execute(query)

        results = cursor.fetchall()
        
        # Add nationalities to the dropdown menu
        for row in results:
            self.cmb_nationality.addItem(row[0])
       
    # When the add button is pressed
    def submit_federation_clicked(self):
        # Connection to the DB
        cnxn = DBConnection.BDConnection()
        cursor = cnxn.cursor()
        
        # Preparate attributes of the new federation
        acronym = self.txt_acronym.text()
        name = self.txt_name.text()
        nationality = self.cmb_nationality.currentText()

        # SQL request to get the country ID
        query = "SELECT NationalityID FROM Nationalities WHERE NationalityName = '{}'"
        formatted_query = query.format(nationality)
        cursor.execute(formatted_query)
        nationality = cursor.fetchone()[0] # Get the result

        # Verify that all required fields are filled
        if acronym and name and nationality:
            if len(acronym) <= 5:
                query = "SELECT FederationName FROM Federations WHERE FederationName = ?"
                cursor.execute(query, name)
                result_name = cursor.fetchone()

                if result_name:
                    msg_box = QMessageBox()
                    msg_box.setText("The name already exists.")
                    msg_box.exec_()
                else :
                    self.insert_federation(cursor, cnxn, name, acronym, nationality)
            else:
                # Show an error message if the acronym is longer than 5 characters
                msg_box = QMessageBox()
                msg_box.setText("The limit of characters for acronym is 5.")
                msg_box.exec_()
        else:
            # Show an error message if one of required field isn't filled
            msg_box = QMessageBox()
            msg_box.setText("Please fill in all the required fields.")
            msg_box.exec_()

    # Function to insert the federation into the database
    def insert_federation(self, cursor, cnxn, name, acronym, nationality):
        query = "INSERT INTO Federations (FederationName, FederationAcronym, FederationNationalityID, FederationActive) VALUES ('{}', '{}', {}, 1)"
        formatted_query = query.format(name, acronym, nationality)
        cursor.execute(formatted_query)
        cnxn.commit()

        # Save the query in a file
        with open('BD/InsertFederationsEloDB.sql', 'a') as file:
            file.write(formatted_query + "\n")
        file.close()

        # Show a confirmation message
        msg_box = QMessageBox()
        msg_box.setText("The federation have been added.")
        msg_box.exec_()

    # Center the window
    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())