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


    # login_action(db)
    main_screen: MainWindow
    if result:
        main_screen = MainWindow(db, lambda: logout_action(main_screen, db))
        main_screen.show()

    def logout_action(db):
        main_screen.hide()
        # main_screen = None
        db.logged_user = None
        login = LoginDialog(db)
        result = login.exec()
        if result:
            main_screen = MainWindow(db, lambda: logout_action(main_screen, db))
            main_screen.show()
    # login.show()
    sys.exit(app.exec())

def login_action(db):
    db.logged_user = None
    login = LoginDialog(db)
    result = login.exec()
    if result:
        print("resutl")
        main_screen = MainWindow(db, lambda: login_action(db))
        main_screen.show()

if __name__ == "__main__":
    main()
