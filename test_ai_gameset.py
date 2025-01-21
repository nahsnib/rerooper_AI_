import tkinter as tk
from scriptwriter.ai_gameset import AIGameSet
from common.character import CharacterManager
class DummyParent:
    pass

def test_ai_gameset():
    root = tk.Tk()  # 創建一個 tkinter 根窗口
    character_manager = CharacterManager(root)  # 傳遞 parent 參數
    gameset = AIGameSet(character_manager)

    public_info = gameset.get_public_info()
    secret_info = gameset.get_secret_info()

    print("公開信息:")
    for key, value in public_info.items():
        print(f"{key}: {value}")

    print("\n秘密信息:")
    for key, value in secret_info.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    test_ai_gameset()
