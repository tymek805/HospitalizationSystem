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
        if main_window is not None:
            main_window.close()
            db.logged_user = None
        login_dialog = LoginDialog(db)
        result = login_dialog.exec()
        if result:
            main_window = MainWindow(db, login)
            main_window.show()

    login()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
