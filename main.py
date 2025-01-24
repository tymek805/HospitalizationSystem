import sys

from PyQt6.QtWidgets import QApplication, QMainWindow

from db.database_manager import DatabaseManager
from ui.login_screen import LoginDialog
from ui.main_screen import MainWindow


def main():
    app = QApplication(sys.argv)
    db = DatabaseManager()
    main_window: QMainWindow|None = None

    def login():
        nonlocal main_window
        nonlocal db
        print("logowanie")
        if main_window is not None:
            print("not none")
            main_window.close()
            db.logged_user = None
        loginDialog = LoginDialog(db)
        result = loginDialog.exec()
        if result:
            main_window = MainWindow(db, login)
            main_window.show()

    login()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
