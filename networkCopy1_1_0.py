import nuke
import os
import socket
import json
from PySide2 import QtWidgets

NETWORK_PATH = r"network location path"
TEMP_FILE_NAME = "temp_nodes.nk"

def get_local_ip():
    ip = socket.gethostbyname(socket.gethostname())
    print "Retrieved IP:", ip
    return ip

def load_users_from_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_dir, 'users_config.json')
    with open(config_file_path, 'r') as f:
        return json.load(f)

USER_DIRS = load_users_from_config()
current_ip = get_local_ip()
current_user = None

for user, ip in USER_DIRS.iteritems():  # Change items() to iteritems()
    if ip == current_ip:
        current_user = user
        break


class UserSelectionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(UserSelectionDialog, self).__init__(parent)
        self.setWindowTitle("Network copy-paste")

        self.layout = QtWidgets.QVBoxLayout()

        self.search_box = QtWidgets.QLineEdit()
        self.search_box.setPlaceholderText("Search for a user...")
        self.search_box.textChanged.connect(self.filter_list)

        self.user_list_widget = QtWidgets.QListWidget()
        self.user_list_widget.addItems(USER_DIRS.keys())

        self.send_button = QtWidgets.QPushButton("Send Nodes")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.advanced_options_button = QtWidgets.QPushButton("Advanced Options")

        # Connect the button to the function
        self.advanced_options_button.clicked.connect(display_advanced_options_dialog)

        self.layout.addWidget(self.search_box)
        self.layout.addWidget(self.user_list_widget)
        self.layout.addWidget(self.send_button)
        self.layout.addWidget(self.cancel_button)
        self.layout.addWidget(self.advanced_options_button)  # Add the button to the layout

        self.setLayout(self.layout)

        self.user_list_widget.itemDoubleClicked.connect(self.accept)
        self.send_button.clicked.connect(self.send_nodes)
        self.cancel_button.clicked.connect(self.reject)

    def filter_list(self):
        search_text = self.search_box.text().toLower()
        for i in range(self.user_list_widget.count()):
            item = self.user_list_widget.item(i)
            item.setHidden(search_text not in item.text().toLower())

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
    user_network_path = os.path.join(NETWORK_PATH, "{}_Networkcopy".format(user))
    ensure_directory_exists(user_network_path)

    temp_file_path = os.path.join(user_network_path, TEMP_FILE_NAME)

    try:
        nuke.nodeCopy(temp_file_path)
    except Exception, e:
        nuke.message("Error while copying nodes: {}".format(str(e)))

def paste_nodes_from_network():
    global current_user

    user_network_path = os.path.join(NETWORK_PATH, "{}_Networkcopy".format(current_user))
    temp_file_path = os.path.join(user_network_path, TEMP_FILE_NAME)

    if not os.path.exists(temp_file_path):
        nuke.message("No nodes to paste.")
        return

    try:
        nuke.nodePaste(temp_file_path)
    except Exception, e:
        nuke.message("Error while pasting nodes: {}".format(str(e)))

def display_user_selection_dialog():
    dialog = UserSelectionDialog()
    dialog.exec_()


class AdvancedOptionsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AdvancedOptionsDialog, self).__init__(parent)
        self.setWindowTitle("Advanced Options")

        self.layout = QtWidgets.QVBoxLayout()

        # Dropdown to select a user to edit
        self.user_combo_box = QtWidgets.QComboBox()
        self.user_combo_box.addItems(list(USER_DIRS.keys()))
        self.user_combo_box.currentIndexChanged.connect(self.update_edit_fields)

        # Fields to display/edit the user's details
        self.edit_user_line_edit = QtWidgets.QLineEdit()
        self.edit_ip_line_edit = QtWidgets.QLineEdit()

        # Update the fields with the current selected user's details
        self.update_edit_fields()

        # Buttons and their connections
        self.edit_button = QtWidgets.QPushButton("Edit User")
        self.edit_button.clicked.connect(self.edit_user)

        self.delete_button = QtWidgets.QPushButton("Delete User")
        self.delete_button.clicked.connect(self.delete_user)

        self.add_user_line_edit = QtWidgets.QLineEdit()
        self.add_user_line_edit.setPlaceholderText("New User Name")

        self.add_ip_line_edit = QtWidgets.QLineEdit()
        self.add_ip_line_edit.setPlaceholderText("New User IP")

        self.add_button = QtWidgets.QPushButton("Add User")
        self.add_button.clicked.connect(self.add_user)

        # Adding widgets to the layout
        self.layout.addWidget(QtWidgets.QLabel("Edit User:"))
        self.layout.addWidget(self.user_combo_box)
        self.layout.addWidget(self.edit_user_line_edit)
        self.layout.addWidget(self.edit_ip_line_edit)
        self.layout.addWidget(self.edit_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(QtWidgets.QLabel("Add User:"))
        self.layout.addWidget(self.add_user_line_edit)
        self.layout.addWidget(self.add_ip_line_edit)
        self.layout.addWidget(self.add_button)

        self.setLayout(self.layout)

    def update_edit_fields(self):
        current_user = self.user_combo_box.currentText()
        self.edit_user_line_edit.setText(current_user)
        self.edit_ip_line_edit.setText(USER_DIRS.get(current_user, ''))

    def edit_user(self):
        user_to_edit = self.user_combo_box.currentText()
        new_name = self.edit_user_line_edit.text()
        new_ip = self.edit_ip_line_edit.text()

        if new_name and new_ip and (new_name != user_to_edit or new_ip != USER_DIRS[user_to_edit]):
            prev_name = user_to_edit
            prev_ip = USER_DIRS.pop(user_to_edit)
            USER_DIRS[new_name] = new_ip
            self.save_changes()
            self.user_combo_box.addItem(new_name)
            self.user_combo_box.removeItem(self.user_combo_box.findText(prev_name))
            QtWidgets.QMessageBox.information(self, "Edited Successfully",
                                              "{} ({}) changed to {} ({})".format(prev_name, prev_ip, new_name, new_ip))
        else:
            QtWidgets.QMessageBox.warning(self, "Edit Warning", "No changes detected!")

    def delete_user(self):
        user_to_delete = self.user_combo_box.currentText()
        confirmation = QtWidgets.QMessageBox.question(self, "Delete User",
                                                      "Are you sure you want to delete {}?".format(user_to_delete),
                                                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if confirmation == QtWidgets.QMessageBox.Yes:
            del USER_DIRS[user_to_delete]
            self.user_combo_box.removeItem(self.user_combo_box.findText(user_to_delete))
            self.save_changes()

    def add_user(self):
        new_user = self.add_user_line_edit.text()
        new_ip = self.add_ip_line_edit.text()
        if new_user and new_ip:
            USER_DIRS[new_user] = new_ip
            self.save_changes()
            self.user_combo_box.addItem(new_user)

    def save_changes(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(script_dir, 'users_config.json')
        with open(config_file_path, 'w') as f:
            json.dump(USER_DIRS, f, indent=4)

def display_advanced_options_dialog():
    dialog = AdvancedOptionsDialog()
    dialog.exec_()

nuke.menu('Nodes').addCommand('Custom/Copy to User', 'display_user_selection_dialog()', "ctrl+alt+c")
nuke.menu('Nodes').addCommand('Custom/Paste', 'paste_nodes_from_network()', "ctrl+alt+v")
nuke.menu('Nodes').addCommand('Custom/Advanced Options', 'display_advanced_options_dialog()')
