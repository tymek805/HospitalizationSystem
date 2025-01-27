from PyQt6.QtWidgets import QSpacerItem, QTableWidget, QTableWidgetItem, QHeaderView

from ui.main_componenets import *

from ui.protocols import Protocols

class HeadOfDepartmentController(UserController):
    def __init__(self, content_layout, db_manager):
        super().__init__(content_layout)
        self.db_manager = db_manager
        self.main_screen()

    def main_screen(self):
        self.clear_content()
        container = self.main_container()
        self.action_button("Wybieranie członków zespołu hospitacyjnego", self.choose_inspected, container.layout())
        container.layout().addItem( QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.content_layout.addWidget(container)

    def head(self, title, auto_button_action, back_button_action) -> QWidget:
        container = QWidget()
        container_layout = QHBoxLayout()

        actions_label = QLabel(title)
        actions_label.setFont(QFont("Arial", 14))
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        container_layout.addWidget(actions_label)
        container_layout.addSpacerItem(spacer)
        if auto_button_action is not None:
            auto_button = QPushButton("Generuj automatycznie")
            auto_button.clicked.connect(auto_button_action)
            container_layout.addWidget(auto_button)
        back_button = QPushButton("Powrót")
        back_button.clicked.connect(back_button_action)
        container_layout.addWidget(back_button)
        container.setLayout(container_layout)
        return container

    def choose_inspected(self):
        self.clear_content()
        self.content_layout.addWidget(self.head("Osoby proponowane do hospitacji", None, self.main_screen))

        inspected_list = self.db_manager.get_newest_recommended_list()
        self.table = QTableWidget()
        self.table.setRowCount(len(inspected_list))  # Liczba wierszy
        self.table.setColumnCount(5)  # Liczba kolumn
        self.table.setHorizontalHeaderLabels(["Imię", "Nazwisko", "Katedra", "Czas od ostatniej hospitacji", ""])

        # Wypełnianie tabeli danymi
        for row, (employee_id, name, last_name, department, time) in enumerate(inspected_list):
            item_name = QTableWidgetItem(name)
            item_last_name = QTableWidgetItem(last_name)
            item_department = QTableWidgetItem(department)

            # Ustawianie tooltipów dla komórek
            item_name.setToolTip(name)
            item_last_name.setToolTip(last_name)
            item_department.setToolTip(department)

            self.table.setItem(row, 0, item_name)
            self.table.setItem(row, 1, item_last_name)
            self.table.setItem(row, 2, item_department)

            self.table.setItem(row, 3, QTableWidgetItem(str(time) + " dni"))
            choose_button = QPushButton("Wybierz członków zespołu")
            choose_button.clicked.connect(lambda: self.choose_inspection_team(employee_id))
            self.table.setCellWidget(row, 4, choose_button)

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)


        # Włączenie wyświetlania pełnego tekstu po najechaniu kursorem
        self.table.setToolTipDuration(-1)
        self.table.setMouseTracking(True)
        self.table.setWordWrap(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.content_layout.addWidget(self.table)



    def choose_inspection_team(self, employee_id):
        self.clear_content()
        self.content_layout.addWidget(self.head("Członkowie zespołu hospitacyjnego", lambda: self.auto_generated_teams(employee_id), self.choose_inspected))
        self.content_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def auto_generated_teams(self, employee_id):
        self.clear_content()
        self.content_layout.addWidget(self.head("Automatycznie wygenerowane zespoły", None, lambda: self.choose_inspection_team(employee_id)))
        self.content_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

