import tkinter as tk
from tkinter import ttk
from datetime import datetime

class GameBoard:
    def __init__(self, root):
        self.root = root
        self.root.title("遊戲板")
        
        self.setup_ui()

    def setup_ui(self):
        # 設置遊戲資訊表
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(side=tk.TOP, fill=tk.X)

        self.current_date_label = tk.Label(self.info_frame, text="當前日期: " + datetime.now().strftime("%Y-%m-%d"))
        self.current_date_label.pack(side=tk.LEFT, padx=10)

        self.events_label = tk.Label(self.info_frame, text="未來事件: 第四天 - 流言蜚語")
        self.events_label.pack(side=tk.LEFT, padx=10)

        self.loop_count_label = tk.Label(self.info_frame, text="剩餘輪迴數: 3")
        self.loop_count_label.pack(side=tk.LEFT, padx=10)

        self.exg_label = tk.Label(self.info_frame, text="EX G: 啟用", fg="red")
        self.exg_label.pack(side=tk.LEFT, padx=10)

        # 設置遊戲區域
        self.area_frame = tk.Frame(self.root)
        self.area_frame.pack(expand=True, fill=tk.BOTH)

        self.setup_area("醫院", 0, 0)
        self.setup_area("神社", 0, 1)
        self.setup_area("鬧區", 1, 0)
        self.setup_area("學校", 1, 1)

    def setup_area(self, name, row, column):
        frame = tk.Frame(self.area_frame, borderwidth=2, relief=tk.SUNKEN)
        frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        label = tk.Label(frame, text=name)
        label.pack()

        # Add additional widgets to each area as needed
        # Example: List of characters in this area
        character_list = tk.Listbox(frame)
        character_list.pack(expand=True, fill=tk.BOTH)
        character_list.insert(tk.END, "角色1")
        character_list.insert(tk.END, "角色2")

        # Example: Add more detailed information if necessary
        details_label = tk.Label(frame, text="詳細資訊")
        details_label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = GameBoard(root)
    root.mainloop()
