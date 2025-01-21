import sys

from PyQt6.QtWidgets import QApplication

from db.database_manager import DatabaseManager
from ui.login_screen import LoginDialog
from ui.main_screen import MainWindow


def main():
    app = QApplication(sys.argv)
    db = DatabaseManager()
    login = LoginDialog(db)
    result = login.exec()

    if result:
        main_screen = MainWindow(db)
        main_screen.show()

    # login.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
