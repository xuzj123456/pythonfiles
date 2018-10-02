# coding=utf-8
import Tkinter as tk


class APP:
    def __init__(self, master):
        frame = tk.Frame(master)
        frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.say_hi_there = tk.Button(frame, text='打招呼', fg='blue', bg='black', command=say_hi)
        self.say_hi_there.pack()


def say_hi():
    print('大家好')


root = tk.Tk()
app = APP(root)

root.mainloop()
