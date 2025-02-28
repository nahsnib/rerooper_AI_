from game_phases.player_detective.player_detective_action_phase import PlayerDetectiveActionPhase
from game_phases.player_detective.player_RA_phase import PlayerRAPhase
from game_phases.player_detective.player_FA_phase import PlayerFriendshipAbilityPhase
from game_phases.player_detective.player_event_phase import EventPhase
from game_phases.player_detective.player_night_phase import NightPhase
from game_phases.player_detective.player_final_battle import FinalBattle
from game_phases.player_detective.player_cycle_end import CycleEnd
import tkinter as tk
from game_gui import GameGUI


class PhaseManager:
    def __init__(self,game = None ):
        self.running = True
        self.game = game  # 傳入 Game 物件
        self.action_phase = None
        self.ra_phase = None
        self.fa_phase = None
        self.event_phase = None
        self.final_battle_phase = None
        self.current_phase = None

    def set_phases(self, game):
        self.game = game  # 傳入 Game 物件
        root = tk.Tk()
        game_gui = GameGUI(root, game, None)    
        game.set_gui(game_gui)

        self.action_phase = PlayerDetectiveActionPhase(game)
        self.ra_phase = PlayerRAPhase(game)        
        self.fa_phase = PlayerFriendshipAbilityPhase(game)
        self.event_phase = EventPhase(game)
        self.night_phase = NightPhase(game)
        self.cycle_end = CycleEnd(game)
        self.final_battle_phase = FinalBattle(game)
        self.current_phase = self.action_phase  # 初始設定當前階段為行動階段


    
    def determine_next_phase(self):
        """決定下一個階段"""
        phase_order = [self.action_phase, self.ra_phase, self.fa_phase, self.event_phase, self.night_phase]
        if self.current_phase in phase_order:
            index = phase_order.index(self.current_phase)
            return phase_order[index + 1] if index + 1 < len(phase_order) else self.cycle_end
        return self.action_phase  # 預設回到 Action Phase

    
    def run(self):
        """啟動遊戲主迴圈"""
        # 1. 遊戲準備階段
        print(f"game: {self.game}")  
        print(f"game.game_gui: {getattr(self.game, 'game_gui', None)}")  

        self.game.time_manager.current_day = 1
        while self.running:
            # 2. 每日流程
            while self.game.time_manager.current_day <= self.game.time_manager.total_days:
                
                # 1-1. Action Phase
                
                self.current_phase = self.action_phase         
                self.current_phase.execute()
                self.game.game_gui.update_area_widgets()  # ✅ 這行確保地區顯示
                self.game.game_gui.set_phase(self.current_phase)
                
                # 1-2. RA Phase
                self.current_phase = self.ra_phase
                print(f"目前階段: {self.current_phase}")
                self.current_phase.execute()
                
                # 1-3. FA Phase
                self.current_phase = self.fa_phase
                print(f"目前階段: {self.current_phase}")
                self.current_phase.execute()
                self.game.game_gui.update_area_widgets()  # ✅ 這行確保地區顯示
                self.game.game_gui.set_phase(self.current_phase)
                
                # 1-4. Event Phase
                self.current_phase = self.event_phase                
                print(f"目前階段: {self.current_phase}")
                self.current_phase.execute()
                
                # 1-5. Night Phase
                self.current_phase = self.night_phase                
                print(f"目前階段: {self.current_phase}")
                self.current_phase.execute()
                
                # 進入下一天
                self.game.time_manager.advance_day()
                
                # 檢查是否需要進入 Cycle End
                if self.game.time_manager.is_final_day() or self.cycle_end_triggered:
                    break
                
            # 2. Cycle End
            self.end_current_phase()
            cycle_result = self.cycle_end.execute()
            
            if cycle_result == "scriptwriter_win":
                print("劇本家勝利！遊戲結束。")
                break
            elif cycle_result == "detective_win":
                print("偵探勝利！遊戲結束。")
                break
            elif cycle_result == "final_battle":
                self.end_current_phase()
                self.run_final_battle()
                break
            elif cycle_result == "cycle_reset":
                self.cycle_reset()
                
        print("遊戲結束")
    
    def run_final_battle(self):
        """執行最終決戰"""
        final_battle = self.final_battle
        final_battle.execute()
        if final_battle.result == "detective_win":
            print("偵探成功揭露真相！")
        else:
            print("劇本家成功隱藏真相……")
        self.running = False
    
    def start_phase(self, new_phase):
        """開始新階段"""
        self.current_phase = new_phase
        if self.current_phase:
            self.current_phase.on_start()
    
    def update(self):
        """遊戲主迴圈，每幀檢查是否需要推進"""
        if self.current_phase == None:
            if self.cycle_end_flag:  # ⬅️ 如果輪迴需要立刻結束，直接進入 Cycle End
                print("輪迴立即結束，進入 Cycle End。")
                self.start_phase(self.cycle_end)
                self.cycle_end_flag = False  # 重置旗標
            else:
                self.advance_phase()

    def advance_phase(self):
        """推進到下一個階段"""
        if self.current_phase != None:
            self.end_current_phase()  # 統一結束當前階段

        next_phase = self.determine_next_phase()
        self.start_phase(next_phase)

    def end_current_phase(self):
        """結束當前階段"""
        if self.current_phase:
            self.current_phase.on_end()  # 每個 Phase 負責自己的清理工作
        
        self.current_phase = None
        print("當前階段已結束，等待進入下一階段")