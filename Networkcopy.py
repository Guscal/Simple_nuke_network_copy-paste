import nuke
import os
import socket
from PySide2 import QtWidgets

# Base network drive path
NETWORK_PATH = r"DRIVE:\network\path"

# Temporary file to store nodes
TEMP_FILE_NAME = "network_copy_nodes.nk"

def get_local_ip():
    ip = socket.gethostbyname(socket.gethostname())
    print("Retrieved IP:", ip)  # Print retrieved IP
    return ip

USER_DIRS = {
    'User1 name': 'ipv4',
    'User2 name': 'ipv4',
    'User3 name': 'ipv4',
    'user4 name': 'ipv4',
    # add users as you need
}

current_ip = get_local_ip()
current_user = None
for user, ip in USER_DIRS.items():
    if ip == current_ip:
        current_user = user
        break

last_selected_user = None

class UserSelectionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(UserSelectionDialog, self).__init__(parent)
        self.setWindowTitle("Select User")
        self.layout = QtWidgets.QVBoxLayout()

        self.search_box = QtWidgets.QLineEdit()
        self.search_box.setPlaceholderText("Search for a user...")
        self.search_box.textChanged.connect(self.filter_list)

        self.user_list_widget = QtWidgets.QListWidget()
        self.user_list_widget.addItems(USER_DIRS.keys())

        self.send_button = QtWidgets.QPushButton("Send Nodes")
        self.cancel_button = QtWidgets.QPushButton("Cancel")

        self.layout.addWidget(self.search_box)
        self.layout.addWidget(self.user_list_widget)
        self.layout.addWidget(self.send_button)
        self.layout.addWidget(self.cancel_button)
        self.setLayout(self.layout)

        self.user_list_widget.itemDoubleClicked.connect(self.accept)
        self.send_button.clicked.connect(self.send_nodes)
        self.cancel_button.clicked.connect(self.reject)

    def filter_list(self):
        search_text = self.search_box.text().lower()
        for i in range(self.user_list_widget.count()):
            item = self.user_list_widget.item(i)
            item.setHidden(search_text not in item.text().lower())

    def get_selected_user(self):
        selected_items = self.user_list_widget.selectedItems()
        return selected_items[0].text() if selected_items else None

    def send_nodes(self):
        selected_user = self.get_selected_user()
        if selected_user:
            global last_selected_user
            last_selected_user = selected_user
            copy_nodes_to_network(selected_user)
            self.accept()

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def copy_nodes_to_network(user):
    user_network_path = os.path.join(NETWORK_PATH, f"{user}_Networkcopy")
    ensure_directory_exists(user_network_path)

    temp_file_path = os.path.join(user_network_path, TEMP_FILE_NAME)

    try:
        nuke.nodeCopy(temp_file_path)
    except Exception as e:
        nuke.message(f"Error while copying nodes: {str(e)}")

def paste_nodes_from_network():
    global current_user

    user_network_path = os.path.join(NETWORK_PATH, f"{current_user}_Networkcopy")
    temp_file_path = os.path.join(user_network_path, TEMP_FILE_NAME)

    if not os.path.exists(temp_file_path):
        nuke.message("No nodes to paste.")
        return

    try:
        nuke.nodePaste(temp_file_path)
    except Exception as e:
        nuke.message(f"Error while pasting nodes: {str(e)}")

def display_user_selection_dialog():
    dialog = UserSelectionDialog()
    dialog.exec_()
    
    
nuke.menu('Nodes').addCommand('Custom/Copy to User', 'display_user_selection_dialog()', "ctrl+alt+c")
nuke.menu('Nodes').addCommand('Custom/Paste', 'paste_nodes_from_network()', "ctrl+alt+v")
