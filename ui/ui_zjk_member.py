from ui.main_componenets import *

from ui.protocols import Protocols
from ui.notification_dialog import NotificationDialog
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame, QApplication, QSpacerItem, QSizePolicy, QTextEdit, QScrollArea, QCheckBox
)

class ZJKMemberController(UserController):
    def __init__(self, content_layout, db_manager):
        super().__init__(content_layout)
        self.db_manager = db_manager
        self.main_screen()

    def main_screen(self):
        self.clear_content()
        container = self.main_container()
        self.action_button("Zarządzanie wykazem osób proponowanych do hospitacji", self.list_of_recommended, container.layout())
        container.layout().addItem( QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.content_layout.addWidget(container)


    def list_of_recommended(self):
        self.clear_content()
        container = QWidget()
        container_layout = QHBoxLayout()

        actions_label = QLabel("Osoby proponowane do hospitacji:")
        actions_label.setFont(QFont("Arial", 14))
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        buttons = QWidget()
        buttons_layout = QHBoxLayout()

        back_button = QPushButton("Powrót")
        back_button.clicked.connect(self.main_screen)

        continue_button = QPushButton("Podsumowanie")

        buttons_layout.addWidget(back_button)
        buttons_layout.addWidget(continue_button)
        buttons.setLayout(buttons_layout)

        container_layout.addWidget(actions_label)
        container_layout.addSpacerItem(spacer)
        container_layout.addWidget(buttons)
        container.setLayout(container_layout)

        self.content_layout.addWidget(container)

        con = QWidget()
        main_layout = QVBoxLayout()

        subtext_label = QLabel("Pracownicy nie hospitowani w terminach podanych w zarządzeniu wewnętrznym")
        subtext_label.setStyleSheet("font-style: italic; font-size: 14px;")
        main_layout.addWidget(subtext_label)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        employees = self.db_manager.get_recommended_employees()

        overdue_employees = []
        for employee in employees:
            if employee[-1] >= 800:
                row_frame = self.create_employee_row(*employee, overdue_employees)
                scroll_layout.addWidget(row_frame)

        main_layout.addWidget(scroll_content)

        subtext_label_2 = QLabel("Pracownicy hospitowani w terminach podanych w zarządzeniu wewnętrznym")
        subtext_label_2.setStyleSheet("font-style: italic; font-size: 14px;")
        main_layout.addWidget(subtext_label_2)

        c = QWidget()
        c_layout = QVBoxLayout(c)

        employees = self.db_manager.get_recommended_employees()
        suggested_employees = []

        for employee in employees:
            if employee[-1] < 800:
                row_frame = self.create_employee_row(*employee, suggested_employees)
                c_layout.addWidget(row_frame)

        main_layout.addWidget(c)

        continue_button.clicked.connect(lambda : self.summary_screen(overdue_employees, suggested_employees))

        con.setLayout(main_layout)
        self.content_layout.addWidget(con)

    def create_employee_row(self, employee_id, name, surname, department, time_from_last_hospitation, employee_list):
        row_frame = QFrame()
        row_frame.setStyleSheet("border: 1px solid black; padding: 5px;")

        row_layout = QHBoxLayout(row_frame)

        name_label = QLabel(name)
        surname_label = QLabel(surname)
        department_label = QLabel(department)
        last_hospitation_label = QLabel(f"Czas od ostatniej hospitacji: {time_from_last_hospitation}")

        select_frame = QFrame()
        select_frame.setStyleSheet("border: 1px solid black; padding: 2px;")
        select_layout = QHBoxLayout(select_frame)

        select_checkbox = QCheckBox()
        select_checkbox.setStyleSheet("border: 0px solid black;")
        select_label = QLabel("Wybierz")
        select_label.setStyleSheet("border: 0px solid black;")

        select_layout.addWidget(select_checkbox)
        select_layout.addWidget(select_label)
        select_layout.setContentsMargins(5, 2, 5, 2)
        select_layout.setSpacing(5)

        employee_list.append((select_checkbox, (employee_id, name, surname, department, time_from_last_hospitation)))

        row_layout.addWidget(name_label)
        row_layout.addWidget(surname_label)
        row_layout.addWidget(department_label)
        row_layout.addWidget(last_hospitation_label)
        row_layout.addStretch()
        row_layout.addWidget(select_frame)

        return row_frame

    def summary_screen(self, overdue_list, normal_list):
        selected_employees = self.get_all_selected_users(overdue_list)

        if len(selected_employees) != len(overdue_list):
            dialog = NotificationDialog()

            if dialog.exec():
                print("Kontynuuj clicked")
            else:
                return

    def get_all_selected_users(self, employee_list):
        selected_employees = []

        for checkbox, employee_info in employee_list:
            if checkbox.isChecked():
                selected_employees.append(employee_info)

        return selected_employees
