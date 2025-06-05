import tkinter as tk
from tkinter import ttk
import math

root = tk.Tk()
root.title("Next-Gen Calculator")
root.geometry("600x650")
root.resizable(False, False)

expression = ""
history = []
display_var = tk.StringVar()
is_dark_mode = True

style = ttk.Style()
style.theme_use("clam")
buttons_list = []

# --- Theme Logic ---
def apply_theme():
    bg = "#1e1e1e" if is_dark_mode else "#f9f9f9"
    fg = "#ffffff" if is_dark_mode else "#000000"
    btn_bg = "#333333" if is_dark_mode else "#e0e0e0"
    btn_fg = "#ffffff" if is_dark_mode else "#000000"

    root.configure(bg=bg)
    style.configure("TEntry", fieldbackground=bg, foreground=fg, font=("Segoe UI", 24), borderwidth=0)
    style.configure("TButton", font=("Segoe UI", 14), padding=10)
    
    for btn in buttons_list:
        btn.configure(background=btn_bg, foreground=btn_fg, borderwidth=0, relief="flat")
        btn.bind("<Enter>", lambda e, b=btn: b.configure(background="#555555" if is_dark_mode else "#c0c0c0"))
        btn.bind("<Leave>", lambda e, b=btn: b.configure(background=btn_bg))

# --- UI Elements ---
main_frame = tk.Frame(root, bg="black")
main_frame.pack(side=tk.LEFT, fill="both", expand=True)

display = ttk.Entry(main_frame, textvariable=display_var, justify="right", font=("Segoe UI", 24))
display.pack(fill="both", padx=10, pady=10, ipady=20)

# --- History Listbox ---
history_frame = tk.Frame(root, width=180, bg="#222222")
history_frame.pack(side=tk.RIGHT, fill="y")

tk.Label(history_frame, text="History", font=("Segoe UI", 12, "bold"), bg="#222222", fg="white").pack(pady=(10, 0))
history_listbox = tk.Listbox(history_frame, font=("Consolas", 11), bg="#111", fg="white", height=25)
history_listbox.pack(fill="both", expand=True, padx=5, pady=5)
tk.Button(history_frame, text="Clear History", command=lambda: history_listbox.delete(0, tk.END)).pack(pady=5)

# --- Button Layout ---
buttons = [
    ("7", "8", "9", "/"),
    ("4", "5", "6", "*"),
    ("1", "2", "3", "-"),
    (".", "0", "=", "+"),
    ("(", ")", "π", "e"),
    ("sin", "cos", "sqrt", "log"),
    ("C", "⌫", "↑", "Theme")
]

def press(key):
    global expression
    if key == "π": key = "math.pi"
    if key == "e": key = "math.e"
    if key in ("sin", "cos", "sqrt", "log"): key = f"math.{key}("
    expression += str(key)
    display_var.set(expression)

def clear():
    global expression
    expression = ""
    display_var.set("")

def backspace():
    global expression
    expression = expression[:-1]
    display_var.set(expression)

def repeat_last():
    if history:
        display_var.set(history[-1].split(" = ")[0])
        global expression
        expression = display_var.get()

def equals():
    global expression
    try:
        result = str(eval(expression, {"__builtins__": None}, math.__dict__))
        entry = f"{expression} = {result}"
        history_listbox.insert(tk.END, entry)
        history.append(entry)
        display_var.set(result)
        expression = result
    except:
        display_var.set("Error")
        expression = ""

def toggle_theme():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    apply_theme()

# --- Create Buttons ---
buttons_frame = tk.Frame(main_frame)
buttons_frame.pack(fill="both", expand=True)

for row in buttons:
    row_frame = tk.Frame(buttons_frame)
    row_frame.pack(expand=True, fill="both")
    for char in row:
        def make_action(c=char):
            if c == "=": return equals
            elif c == "C": return clear
            elif c == "⌫": return backspace
            elif c == "Theme": return toggle_theme
            elif c == "↑": return repeat_last
            else: return lambda: press(c)

        btn = tk.Button(row_frame, text=char, command=make_action())
        btn.pack(side="left", expand=True, fill="both", padx=4, pady=4)
        buttons_list.append(btn)

# --- Keyboard Bindings ---
def key_handler(event):
    key = event.keysym
    if key in "0123456789":
        press(key)
    elif key in ("plus", "minus", "slash", "asterisk", "period"):
        symbols = {"plus": "+", "minus": "-", "slash": "/", "asterisk": "*", "period": "."}
        press(symbols[key])
    elif key == "Return":
        equals()
    elif key == "BackSpace":
        backspace()
    elif key == "c":
        clear()
    elif key == "Up":
        repeat_last()
    elif key == "parenleft":
        press("(")
    elif key == "parenright":
        press(")")

root.bind("<Key>", key_handler)

apply_theme()
root.mainloop()


