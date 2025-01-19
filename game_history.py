import datetime
import copy

class GameHistory:
    def __init__(self):
        self.history = []

    def add_snapshot(self, timestamp, gameboard_state):
        snapshot = {
            'timestamp': timestamp,
            'gameboard_state': copy.deepcopy(gameboard_state)
        }
        self.history.append(snapshot)

    def get_snapshot(self, timestamp):
        for snapshot in self.history:
            if snapshot['timestamp'] == timestamp:
                return snapshot['gameboard_state']
        return None

    def display_snapshots(self):
        for snapshot in self.history:
            print(f"Timestamp: {snapshot['timestamp']}")
            # 可以在此處添加更多顯示快照狀態的邏輯
            print(snapshot['gameboard_state'])

# 測試遊戲履歷功能
if __name__ == "__main__":
    game_history = GameHistory()

    # 假設這是某個時間點的遊戲狀態
    gameboard_state = {
        'areas': {
            'hospital': {'conspiracy_points': 1, 'characters': ['男學生']},
            'shrine': {'conspiracy_points': 2, 'characters': ['女學生']},
            'city': {'conspiracy_points': 0, 'characters': ['刑警']},
            'school': {'conspiracy_points': 3, 'characters': ['老師']}
        },
        'time_manager': {'current_day': 4, 'remaining_cycles': 2}
    }
    timestamp = datetime.datetime.now()

    game_history.add_snapshot(timestamp, gameboard_state)
    game_history.display_snapshots()
