from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame, QApplication, QSpacerItem, QSizePolicy, QTextEdit, QScrollArea, QCheckBox
)

from db.database_manager import UserType
from ui.notification_dialog import NotificationDialog


class MainWindow(QWidget):

    def __init__(self, database_manager):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.setGeometry(100, 100, 900, 450)

        self.db_manager = database_manager
        self.user_role = UserType[self.db_manager.get_user_role()]
        self.init_ui()
        self.center()

    def init_ui(self):
        content_frame = QFrame()

        main_layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        self.content_layout = QVBoxLayout()
        content_frame.setLayout(self.content_layout)
        scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        scroll_area.setWidget(content_frame)

        self.main_screen()

        main_layout.addLayout(self.header_layout())
        h_line = QFrame()
        h_line.setFrameShape(QFrame.Shape.HLine)
        h_line.setStyleSheet("color: black;")
        main_layout.addWidget(h_line)

        main_layout.addWidget(scroll_area)
        # main_layout.addStretch()
        self.setLayout(main_layout)

    def main_screen(self):
        self.clear_content()

        container = QWidget()
        container_layout = QVBoxLayout()

        actions_label = QLabel("Dostępne akcje:")
        actions_label.setFont(QFont("Arial", 14))
        container_layout.addWidget(actions_label, alignment=Qt.AlignmentFlag.AlignTop)

        self.add_actions(container_layout)
        container_layout.setSpacing(20)
        container.setLayout(container_layout)
        container_layout.addStretch()
        self.content_layout.addWidget(container)
        # self.content_layout.setSpacing(20)

    def protocols_screen_1(self):
        self.clear_content()
        container = QWidget()
        container_layout = QHBoxLayout()

        actions_label = QLabel("Dostępne protokoły:")
        actions_label.setFont(QFont("Arial", 14))
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        back_button = QPushButton("Powrót")
        back_button.clicked.connect(self.main_screen)
        container_layout.addWidget(actions_label)
        container_layout.addSpacerItem(spacer)
        container_layout.addWidget(back_button)
        container.setLayout(container_layout)

        self.content_layout.addWidget(container)

        if self.user_role == UserType.INSPECTED:
            protocols = self.db_manager.get_protocols(self.db_manager.logged_user)
        else:
            protocols = self.db_manager.get_all_protocols(self.db_manager.logged_user)

        for protocol in protocols:
            protocol_title = f"{self.db_manager.get_employee_full_name(protocol[0])} - {protocol[4]}"
            self.action_button(protocol_title, lambda : self.protocols_screen_2(protocol), self.content_layout, Qt.AlignmentFlag.AlignHCenter)

    def protocols_screen_2(self, protocol):
        self.clear_content()
        container = QWidget()
        container_layout = QHBoxLayout()
        print(protocol)
        actions_label = QLabel(f"Protokół hospitacji w semestrze \"{self.db_manager.get_semester_name(protocol[-1])}\"")
        actions_label.setFont(QFont("Arial", 14))
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        back_button = QPushButton("Powrót")
        back_button.clicked.connect(self.protocols_screen_1)
        container_layout.addWidget(actions_label)
        container_layout.addSpacerItem(spacer)
        container_layout.addWidget(back_button)
        container.setLayout(container_layout)
        self.content_layout.addWidget(container)

        protocol_container = QWidget()
        protocol_layout = QHBoxLayout()

        protocol_text = QTextEdit()
        protocol_text.setReadOnly(True)
        text = self.load_protocol_content(protocol[5])
        protocol_text.setText(text)
        protocol_text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        side_panel_container = QFrame()
        side_panel_container.setFrameShape(QFrame.Shape.Box)
        side_panel_container.setFrameShadow(QFrame.Shadow.Raised)
        side_panel_container.setStyleSheet("border: 2px solid black; border-radius: 5px; padding: 10px;")
        side_panel_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        side_panel = QVBoxLayout()
        side_panel.addWidget(QLabel(f"Ocena końcowa: {protocol[3]}"))
        side_panel.addWidget(QLabel(f"Data utworzenia: {protocol[4]}"))
        side_panel.addWidget(QLabel(f"Hospitowany: {self.db_manager.get_fullname(self.db_manager.get_employee_id_from_hospitalization(protocol[1]))}"))

        side_panel_container.setLayout(side_panel)
        protocol_layout.addWidget(protocol_text, 3)
        protocol_layout.addWidget(side_panel_container, 1)

        protocol_container.setLayout(protocol_layout)
        self.content_layout.addWidget(protocol_container)

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

    def header_layout(self):
        layout = QHBoxLayout()

        header_label = QLabel(f"Zalogowany jako: {self.user_role.value}")
        header_label.setFont(QFont("Arial", 16))
        header_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        layout.addWidget(header_label)

        user_info_layout = QHBoxLayout()

        user_label = QLabel(self.db_manager.get_fullname(self.db_manager.logged_user))
        user_label.setStyleSheet("border: 1px solid black; padding: 10px;")
        logout_button = QPushButton("Wyloguj")
        logout_button.setStyleSheet("padding: 10px;")

        user_info_layout.addWidget(user_label)
        user_info_layout.addWidget(logout_button)
        user_info_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addLayout(user_info_layout)
        layout.setContentsMargins(5, 10, 5, 10)
        return layout

    def add_actions(self, layout):
        if self.user_role == UserType.INSPECTED:
            self.action_button("Protokoły hospitacji", self.protocols_screen_1, layout)
        elif self.user_role == UserType.INSPECTION_TEAM_MEMBER:
            self.action_button("Protokoły hospitacji", self.protocols_screen_1, layout)
        elif self.user_role == UserType.ZJK_MEMBER:
            self.action_button("Zarządzanie wykazem osób proponowanych do hospitacji", self.list_of_recommended, layout)
        else:
            print("No action found for this UserType")


    def action_button(self, text, content, layout, alignment=Qt.AlignmentFlag.AlignTop):
        button = QPushButton(text)
        button.setStyleSheet("padding: 10px;")
        button.clicked.connect(content)
        layout.addWidget(button, alignment=alignment)

    def clear_content(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def load_protocol_content(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                return content
        except Exception as e:
            return f"Error loading file: {str(e)}"

    def center(self):
        frame_geometry = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
