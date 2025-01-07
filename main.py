from rules.main_rules import load_main_rules
from rules.character_database import load_character_database
from scriptwriter.script_edit import ScriptEditor
from game_phases.action_phase import ActionPhase
from game_phases.event_phase import EventPhase
from game_phases.night_phase import NightPhase
from game_phases.cycle_end import CycleEnd
from game_phases.final_battle import FinalBattle
from ai.scriptwriter_ai import ScriptwriterAI
from ai.detective_ai import DetectiveAI
from history.game_history import GameHistory
from common.board import Board

def main():
    # 初始化主要規則表和角色資料庫
    main_rules = load_main_rules()
    character_database = load_character_database()
    
    # 劇本家進行劇本編輯
    script_editor = ScriptEditor(main_rules, character_database)
    script_editor.edit_script()
    
    # 初始化遊戲板和階段
    board = Board()
    action_phase = ActionPhase(board)
    event_phase = EventPhase(board)
    night_phase = NightPhase(board)
    cycle_end = CycleEnd(board)
    final_battle = FinalBattle(board)
    game_history = GameHistory()
    
    # 遊戲主循環
    while not cycle_end.is_game_over():
        action_phase.execute()
        event_phase.execute()
        night_phase.execute()
        cycle_end.check_end_conditions()
    
    # 最終決戰
    final_battle.execute()

if __name__ == "__main__":
    main()
