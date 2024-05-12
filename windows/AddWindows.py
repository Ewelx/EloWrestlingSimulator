from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
import windows.addWindows.AddEventWindows as AddEventWindows
import windows.addWindows.AddFederationWindows as AddFederationWindows
import windows.addWindows.AddWrestlerWindows as AddWrestlerWindows

# The windows that show up when clicked on "Add"
class AddWindows(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.add_window = None
        
    # Init the window UI
    def initUI(self):
        # Base screen window
        self.setWindowTitle('Wrestling Elo Simulator')
        self.setFixedSize(1400, 700)
        self.center()

        # Label creation
        label = QLabel('Add', self)
        label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        font = label.font()
        font.setBold(True)
        font.setPointSize(24)
        label.setFont(font)

        # Adding the label to the layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        # Button creation
        btn_wrestler = QPushButton('Wrestler', self)
        btn_tag_team = QPushButton('Tag-Team', self)
        btn_stable = QPushButton('Stable', self)
        btn_federation = QPushButton('Federation', self)
        btn_event = QPushButton('Event', self)
        btn_title = QPushButton('Title', self)
        btn_match = QPushButton('Match', self)

        # Enlargement of the buttons
        btn_wrestler.resize(150, 75)
        btn_tag_team.resize(150, 75)
        btn_stable.resize(150, 75)
        btn_federation.resize(150, 75)
        btn_event.resize(150, 75)
        btn_title.resize(150, 75)
        btn_match.resize(600, 75)

        # Placer les boutons dans la fenêtre
        btn_wrestler.move(400, 150)
        btn_tag_team.move(850, 150)
        btn_stable.move(400, 275)
        btn_federation.move(850, 275)
        btn_event.move(400, 400)
        btn_title.move(850, 400)
        btn_match.move(400, 525)

        # Placement of the buttons in the window
        font = btn_wrestler.font()
        font.setPointSize(13)
        btn_wrestler.setFont(font)
        btn_tag_team.setFont(font)
        btn_stable.setFont(font)
        btn_federation.setFont(font)
        btn_event.setFont(font)
        btn_title.setFont(font)
        btn_match.setFont(font)

        # Connect clicked event of buttons to method (that will permit reach next windows)
        btn_wrestler.clicked.connect(self.on_btn_wrestler_clicked)
        btn_tag_team.clicked.connect(self.on_btn_tag_team_clicked)
        btn_stable.clicked.connect(self.on_btn_stable_clicked)
        btn_federation.clicked.connect(self.on_btn_federation_clicked)
        btn_event.clicked.connect(self.on_btn_event_clicked)
        btn_title.clicked.connect(self.on_btn_title_clicked)
        btn_match.clicked.connect(self.on_btn_match_clicked)

    # When the button 'Wrestler' is clicked
    def on_btn_wrestler_clicked(self):
        # Add wrestler window
        self.add_window = None
        self.add_window = AddWrestlerWindows.AddWrestlerWindows()
        self.add_window.show()
    
    # When the button 'Tag-Team' is clicked
    def on_btn_tag_team_clicked(self):
        print('2')

    # When the button 'Stable' is clicked
    def on_btn_stable_clicked(self):
        print('3')

    # When the button 'Federation' is clicked
    def on_btn_federation_clicked(self):
        # Add federation window
        self.add_window = None
        self.add_window = AddFederationWindows.AddFederationWindows()
        self.add_window.show()

    def on_btn_event_clicked(self):
        # Add event window
        self.add_window = None
        self.add_window = AddEventWindows.AddEventWindows()
        self.add_window.show()

    # When the button 'Title' is clicked
    def on_btn_title_clicked(self):
        print('6')

    # When the button 'Match' is clicked
    def on_btn_match_clicked(self):
        print('7')

    # Center the window
    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())