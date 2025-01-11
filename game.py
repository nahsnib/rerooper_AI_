# game.py
class Player:
    def __init__(self, role):
        self.role = role

    def perform_role_action(self):
        if self.role == "偵探":
            self.detective_action()
        elif self.role == "劇本家":
            self.scriptwriter_action()

    def detective_action(self):
        print("偵探行動：調查案件")

    def scriptwriter_action(self):
        print("劇本家行動：設置情節")
