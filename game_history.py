import datetime

class GameHistory:
    def __init__(self):
        self.history = []

    def add_record(self, start_time, end_time, actions):
        record = {
            'start_time': start_time,
            'end_time': end_time,
            'actions': actions
        }
        self.history.append(record)

    def get_history(self):
        return self.history

    def display_history(self):
        for record in self.history:
            print(f"Start Time: {record['start_time']}")
            print(f"End Time: {record['end_time']}")
            print("Actions:")
            for action in record['actions']:
                print(f"  - {action}")
            print("\n")

# 測試遊戲履歷功能
if __name__ == "__main__":
    game_history = GameHistory()

    # 添加測試記錄
    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(hours=1)
    actions = ["角色A 移動到 地區1", "角色B 執行了 行動X"]

    game_history.add_record(start_time, end_time, actions)
    game_history.display_history()