from ui.main_componenets import *

from ui.protocols import Protocols

class InspectedController(UserController):
    def __init__(self, content_layout, db_manager):
        super().__init__(content_layout)
        self.db_manager = db_manager
        self.main_screen()

    def main_screen(self):
        self.clear_content()
        container = self.main_container()
        self.action_button("Protokoły hospitacji", self.protocols_screen, container.layout())
        self.content_layout.addWidget(container)

    def protocols_screen(self):
        c = Protocols(self, self.db_manager.get_protocols(self.db_manager.logged_user))
        c.protocols_screen_1()
