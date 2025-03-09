from game_phases.player_detective.player_detective_action_phase import PlayerDetectiveActionPhase
from game_phases.player_detective.player_RA_phase import PlayerRAPhase
from game_phases.player_detective.player_FA_phase import PlayerFriendshipAbilityPhase
from game_phases.player_detective.player_event_phase import EventPhase
from game_phases.player_detective.player_night_phase import NightPhase
from game_phases.player_detective.player_final_battle import FinalBattle
from game_phases.player_detective.player_cycle_end import CycleEnd

import tkinter as tk


class PhaseManager:
    def __init__(self):
        self.running = True
        self.action_phase = None
        self.ra_phase = None
        self.fa_phase = None
        self.event_phase = None
        self.final_battle_phase = None
        self.current_phase = None
        self.cycle_end_triggered = False # 強制結束的旗標，預設非        
        self.history_callback = None
     
    def set_phases(self, game):
        self.game = game
        self.action_phase = PlayerDetectiveActionPhase(game)
        self.ra_phase = PlayerRAPhase(game)        
        self.fa_phase = PlayerFriendshipAbilityPhase(game)
        self.event_phase = EventPhase(game)
        self.night_phase = NightPhase(game)
        self.cycle_end = CycleEnd(game)
        self.final_battle_phase = FinalBattle(game)
        self.current_phase = self.night_phase  # 初始設定當前階段為行動階段
   
    def determine_next_phase(self):
        """決定下一個階段"""
        phase_order = [self.action_phase, self.ra_phase, self.fa_phase, self.event_phase, self.night_phase]
        if self.game.cycle_end_flag:
            print("偵測到 cycle_end_flag，直接進入 Cycle End。")
            return self.cycle_end

        elif self.current_phase in phase_order:
            index = phase_order.index(self.current_phase)
            return phase_order[index + 1] if index + 1 < len(phase_order) else self.cycle_end
        else:
            return self.action_phase
    
    def run_final_battle(self):
        """執行最終決戰"""
        self.running = False
        final_battle = self.final_battle
        final_battle.execute()
        if final_battle.result == "detective_win":
            print("偵探成功揭露真相！")
        else:
            print("劇本家成功隱藏真相……")
    
    def start_phase(self, new_phase = None):
        """開始新階段"""
        if new_phase:
            self.current_phase = new_phase
        else:
            self.current_phase = self.action_phase
        self.game.game_gui.set_phase(self.current_phase)
        self.current_phase.execute()
        self.game.game_gui.root.update_idletasks()

    def advance_phase(self):
        """推進到下一個階段"""
        if self.history_callback:
            self.history_callback()  # 讓外部的 `GameGUI` 記錄歷史

        next_phase = self.determine_next_phase()
        self.start_phase(next_phase)

    def end_current_phase(self):
        """結束當前階段"""
        if self.current_phase:
            self.current_phase.on_end()  # 每個 Phase 負責自己的清理工作
        
        self.current_phase = None
        print("當前階段已結束，等待進入下一階段")

    def set_history_callback(self, callback):
        """設定記錄歷史的回調函數"""
        self.history_callback = callback