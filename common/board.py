class Area:
    def __init__(self, id, name):
        self.id = id  # 新增的編號屬性
        self.name = name
        self.characters = []  # 該地區內的角色列表
        self.conspiracy_points = 0  # 該地區的陰謀值

    def add_character(self, character):
        self.characters.append(character)

    def remove_character(self, character):
        self.characters.remove(character)

    def add_conspiracy_points(self, points):
        self.conspiracy_points += points

    def remove_conspiracy_ban(self):
        # 移除陰謀禁止卡片的邏輯
        pass

    def display_area_info(self):
        print(f"地區編號: {self.id}")
        print(f"名稱: {self.name}")
        print(f"陰謀值: {self.conspiracy_points}")
        print("角色:")
        for character in self.characters:
            print(f"  - {character.name}")


# 定義地區
school = Area(1, "學校")
shrine = Area(2, "神社")
city = Area(3, "都市")
hospital = Area(4, "醫院")

# 添加地區到地圖
areas = {
    school.id: school,
    shrine.id: shrine,
    city.id: city,
    hospital.id: hospital,
}

def display_all_areas():
    for area in areas.values():
        area.display_area_info()

def get_area_by_id(area_id):
    return areas.get(area_id, None)
