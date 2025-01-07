
def construct_scenario(self):
    # 劇本家從公開規則表中選擇一張
    self.rules = self.choose_public_rule()

    # 劇本家秘密選擇數條規則
    self.secret_rules = self.choose_secret_rules()

    # 從角色庫中選擇角色
    self.characters = self.select_characters()

    # 依據規則賦予角色身分
    self.assign_roles()

    # 決定輪迴次數
    self.rounds = self.choose_rounds()

    # 決定每輪回合數
    self.days_per_round = self.choose_days_per_round()

    # 決定哪些日子會發生事件
    self.events = self.schedule_events()

    # 決定事件犯人
    self.assign_event_criminals()
