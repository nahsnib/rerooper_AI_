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
