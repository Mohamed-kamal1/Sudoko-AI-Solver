import tkinter as tk
import GUI.Utilities.Style as S

def menu (parent):
    menu_frame = tk.Frame(parent, bg=S.MENU_BG, width=400)
    menu_frame.pack_propagate(False)
    menu_frame.pack(side=tk.LEFT, fill=tk.Y)
    return menu_frame

def label(parent, text, fontSize, anchor, pady, version=1):
    fg_color = S.LABEL_COLOR if version == 1 else "#f20c4d"
    title = tk.Label(parent, text=text, font=(S.FONT_STYLE, fontSize, "bold"), bg=S.MENU_BG, fg=fg_color)
    title.pack(anchor=anchor, pady=pady)
    return title

def radioButton(parent, variable, text, value, side, function):
    radio = tk.Radiobutton(parent, text=text, variable=variable, value=value, font=S.FONT_STYLE, bg=S.MENU_BG, fg=S.LABEL_COLOR, 
                           activebackground=S.MENU_BG, activeforeground=S.LABEL_COLOR, selectcolor=S.BUTTON_COLOR, command=function)
    radio.pack(pady=5, side=side, padx=5)
    return radio

def button(parent, text, function, expand=False, side=None):
    button = tk.Button(parent, text=text, font=(S.FONT_STYLE, 12), bg= S.BUTTON_COLOR, fg=S.LABEL_COLOR, command=function)
    button.pack(pady=10, fill=tk.X, padx=10, expand=expand, side=side)
    return button