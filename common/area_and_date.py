

class Area:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.characters = []  # 該地區內的角色列表
        self.conspiracy = 0   # 該地區的陰謀值

    def add_character(self, character):
        self.characters.append(character)

    def remove_character(self, character):
        if character in self.characters:
            self.characters.remove(character)

    def change_conspiracy(self,game, amount):
        self.conspiracy = max(0, self.conspiracy + amount)  # 陰謀值最低為 0
        game.check_passive_ability("area_conspiracy")

    def __repr__(self):
        return f"Area({self.id}, {self.name})"

    def move_horizontal(self):
        pass

    def move_vertical(self):
        pass

    def move_diagonal(self):
        pass

    def move_anywhere(self):
        pass

    def change_anxiety(self, amount):
        pass

    def change_friendship(self, amount):
        pass

class AreaManager:
    def __init__(self):
        self.areas = []  # 存儲所有區域
        self.initialize_areas()

    def initialize_areas(self):
        self.areas.append(Area(1, "醫院"))
        self.areas.append(Area(2, "神社"))
        self.areas.append(Area(3, "都市"))
        self.areas.append(Area(4, "學校"))


    def fetch_area_by_id(self, area_id):
        return self.areas.get(area_id, None)
    
    def fetch_area_by_name(self, name):
        for area in self.areas:
            if area.name == name:
                return area
        return None
   
    def display_all_areas(self):
        for area in self.areas:
            area.display_area_info()


class TimeManager:
    def __init__(self, current_day ,total_days, total_cycles):
        self.total_days = total_days
        self.total_cycles = total_cycles
        self.current_cycle = 1      # 預設從1開始
        self.current_day = 1      # 預設從1開始
        self.remaining_cycles = total_cycles

    def increment_day(self):
        self.current_day += 1
        if self.current_day > self.total_days:
            self.current_day = 1
            self.remaining_cycles -= 1

    def get_scheduled_events(self, scheduled_events):
        return scheduled_events

