from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QComboBox, QDateTimeEdit, QLabel, QLineEdit, QListWidget, QMessageBox, QPushButton, QVBoxLayout, QWidget
import sys
sys.path.insert(1, '/')
import DBConnection

class AddEventWindows(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Base screen window
        self.setWindowTitle('Wrestling Elo Simulator')
        self.setFixedSize(1400, 700)
        self.center()

        # Label creation
        label = QLabel('Add Event', self)
        label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        font = label.font()
        font.setBold(True)
        font.setPointSize(24)
        label.setFont(font)

        # Adding the label to the layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        # Name of the event
        lbl_name = QLabel('Name * :', self)
        lbl_name.move(560, 150)
        self.txt_name = QLineEdit(self)
        self.txt_name.move(560, 180)
        self.txt_name.resize(280, 30)

        # Country of the event
        lbl_country = QLabel('Country * :', self)
        lbl_country.move(560, 210)
        self.cmb_country = QComboBox(self)
        self.cmb_country.move(560, 240)
        self.cmb_country.resize(280, 30)

        # Date of the event
        lbl_date = QLabel('Date * :', self)
        lbl_date.move(560, 270)
        self.date_edit = QDateTimeEdit(self)
        self.date_edit.setCalendarPopup(True)  # Show a calender
        self.date_edit.setDisplayFormat("yyyy-MM-dd")  # Format of the date
        self.date_edit.move(560, 300)
        self.date_edit.resize(280, 30)

        # Cagematch rating of the event
        lbl_cagematch = QLabel('Cagematch rating * :', self)
        lbl_cagematch.move(560, 330)
        lbl_cagematch.resize(280, 20)
        self.txt_cagematch = QLineEdit(self)
        self.txt_cagematch.move(560, 360)
        self.txt_cagematch.resize(280, 30)

        # Theme of the event
        lbl_theme = QLabel('Theme :', self)
        lbl_theme.move(560, 390)
        self.txt_theme = QLineEdit(self)
        self.txt_theme.move(560, 420)
        self.txt_theme.resize(280, 30)

        # Federations that organised the event
        lbl_federation = QLabel('Federation(s) * :', self)
        lbl_federation.move(560, 450)
        self.lst_federation = QListWidget(self)
        self.lst_federation.move(560, 480)
        self.lst_federation.resize(280, 100)
        self.lst_federation.setSelectionMode(QListWidget.MultiSelection)

        # Button that permit to add the event 
        btn_add = QPushButton('Add', self)
        btn_add.move(650, 610)
        btn_add.clicked.connect(self.submit_event_clicked)

        # Connection to the DB
        cnxn = DBConnection.DBConnection()
        
        cursor = cnxn.cursor()

        # Request to get all nationalities
        query = "SELECT NationalityName FROM Nationalities"
        cursor.execute(query)

        results = cursor.fetchall()

        # Add nationalities to the dropdown menu
        for row in results:
            self.cmb_country.addItem(row[0])

        # Request to get all federations
        query = "SELECT FederationName FROM Federations"
        cursor.execute(query)

        results = cursor.fetchall()

        # Add federations to the dropdown menu
        for row in results:
            self.lst_federation.addItem(row[0])
       
    # When the add button is pressed
    def submit_event_clicked(self):
        # Connection to the DB
        cnxn = DBConnection.BDConnection()
        cursor = cnxn.cursor()

        # Preparate attributes of the new event
        name = self.txt_name.text()
        country = self.cmb_country.currentText()
        selected_date = self.date_edit.dateTime() # Get date and hours
        formatted_date = selected_date.toString("yyyy-MM-dd HH:mm:ss") # Format date to SQL datetime
        cagematch = self.txt_cagematch.text()
        theme = self.txt_theme.text()
        federations = self.lst_federation.selectedItems()
        federations = [item.text() for item in federations]

        # SQL request to get the country ID
        query = "SELECT NationalityID FROM Nationalities WHERE NationalityName = '{}'"
        formatted_query = query.format(country)
        cursor.execute(formatted_query)
        country = cursor.fetchone()[0] # Get the result
            
        # SQL request to get all federations ID
        query = "SELECT FederationID FROM Federations WHERE FederationName IN ({})"
        formatted_query = query.format(",".join(["'{}'".format(federation) for federation in federations]))
        cursor.execute(formatted_query)
        federations = [row[0] for row in cursor.fetchall()] # Get all results

        # Verify that all required fields are filled
        if name and country and formatted_date and cagematch:
            try:
                cagematch = float(cagematch)
            except ValueError:
                # Show an error message if we can't float cast 
                msg_box = QMessageBox()
                msg_box.setText("The cagematch rating is invalid (exemple of rating : 5.01)")
                msg_box.exec_()
                return
            if cagematch > 0 or cagematch < 10:
                self.insert_event(cursor, cnxn, name, country, formatted_date, cagematch, theme, federations)
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

    # Function to insert the event into the database
    def insert_event(self, cursor, cnxn, name, country, formatted_date, cagematch, theme, federations):
        query = "INSERT INTO Events (EventName, EventCountryID, EventDate, EventCagematchRating, EventTheme) VALUES ('{}', '{}', {}, {}, '{}')"
        formatted_query = query.format(name, country, "'" + formatted_date + "'", cagematch, theme)
        cursor.execute(formatted_query)
        cnxn.commit()

        # Get the ID of the new event
        query = "SELECT MAX(EventID) FROM Events"
        cursor.execute(query)
        event_id = cursor.fetchone()[0]

        # Save the query in a file
        with open('BD/InsertEventsEloDB.sql', 'a') as file:
            file.write(formatted_query + "\n")
        file.close()
        
        # Insert all the federations associated with the event
        for federation_id in federations:
            query = "INSERT INTO HasOrganisedEvent (EventID, FederationID) VALUES ('{}', '{}')"
            formatted_query = query.format(event_id, federation_id)
            cursor.execute(formatted_query)
            cnxn.commit()

            # Save the query in a file
            with open('BD/InsertHasOrganisedEvent.sql', 'a') as file:
                file.write(formatted_query + "\n")
            file.close()

        # Show a confirmation message
        msg_box = QMessageBox()
        msg_box.setText("The event have been added.")
        msg_box.exec_()

    # Center the window
    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())