from game_phases.player_detective.player_detective_action_phase import PlayerDetectiveActionPhase
from game_phases.player_detective.player_RA_phase import PlayerRAPhase
from game_phases.player_detective.player_FA_phase import PlayerFriendshipAbilityPhase
from game_phases.player_detective.player_event_phase import EventPhase
from game_phases.player_detective.player_night_phase import NightPhase
from game_phases.player_detective.player_final_battle import FinalBattle
from enum import Enum

class Phase(Enum):
    ACTION = "Action Phase"
    RA = "RA Phase"
    FA = "FA Phase"
    EVENT = "Event Phase"
    NIGHT = "Night Phase"
    CYCLE_END = "Cycle End"
    FINAL_BATTLE = "Final Battle"
    NONE = "None"  # 初始狀態


class PhaseManager:
    def __init__(self,game = None ):
        self.running = True
        self.game = game  # 傳入 Game 物件
        self.action_phase = PlayerDetectiveActionPhase(self.game, game.game_gui)
        self.RA_phase = PlayerRAPhase(self.game)        
        self.FA_phase = PlayerFriendshipAbilityPhase(self.game, game.game_gui)
        self.event_phase = EventPhase(self.game)
        self.final_battle_phase = FinalBattle(self.game)
        self.current_phase = self.action_phase  # 初始設定當前階段

    def update(self):
        """遊戲主迴圈，每幀檢查是否需要推進"""
        if self.current_phase == Phase.NONE:
            if self.cycle_end_flag:  # ⬅️ 如果輪迴需要立刻結束，直接進入 Cycle End
                print("輪迴立即結束，進入 Cycle End。")
                self.start_phase(Phase.CYCLE_END)
                self.cycle_end_flag = False  # 重置旗標
            else:
                self.advance_phase()

    def advance_phase(self):
        """推進到下一個階段"""
        if self.current_phase != Phase.NONE:
            self.end_phase()  # 統一結束當前階段

        next_phase = self.determine_next_phase()
        self.start_phase(next_phase)
    
    def determine_next_phase(self):
        """決定下一個階段"""
        phase_order = [Phase.ACTION, Phase.RA, Phase.FA, Phase.EVENT, Phase.NIGHT]
        if self.current_phase in phase_order:
            index = phase_order.index(self.current_phase)
            return phase_order[index + 1] if index + 1 < len(phase_order) else Phase.CYCLE_END
        return Phase.ACTION  # 預設回到 Action Phase

    
    def run(self):
        """啟動遊戲主迴圈"""
        # 1. 遊戲準備階段
        self.game.time_manager.current_day = 1
        while self.running:
            # 2. 每日流程
            while self.game.time_manager.current_day <= self.game.time_manager.total_days:
                
                # 1-1. Action Phase
                self.current_phase = self.action_phase
                self.current_phase.execute()
                
                # 1-2. RA Phase
                self.current_phase = self.ra_phase
                self.current_phase.execute()
                
                # 1-3. FA Phase
                self.current_phase = self.fa_phase
                self.current_phase.execute()
                
                # 1-4. Event Phase
                self.current_phase = self.event_phase
                self.current_phase.execute()
                
                # 1-5. Night Phase
                self.current_phase = self.night_phase
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
    
    def start_phase(self, new_phase: Phase):
        """開始新階段"""
        self.current_phase = new_phase
        self.phase_instance = self.create_phase_instance(new_phase)
        if self.phase_instance:
            self.phase_instance.on_start()
    
    def end_current_phase(self):
        """結束當前階段"""
        if self.current_phase:
            self.current_phase.on_end()  # 每個 Phase 負責自己的清理工作
        
        self.current_phase = Phase.NONE
        self.phase_instance = None
        print("當前階段已結束，等待進入下一階段")