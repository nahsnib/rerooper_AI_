# game_phases/event_phase.py

class EventPhase:
    def __init__(self, board):
        self.board = board

    def execute(self):
        print("執行事件階段...")
        # 實現事件階段邏輯
        for event in self.board.events:
            print(f"處理事件: {event}")
            # 在這裡添加更多事件處理邏輯
            # 例如，事件影響角色或區域
