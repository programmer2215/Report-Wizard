import tkinter as tk
from tkinter import ttk
from matplotlib import pyplot as plt
import tkcalendar as tkcal 
from datetime import datetime
import datetime as dt
import tkinter.font as tk_font
import database as db


root = tk.Tk()
root.title("Report Wizard")

FONT = tk_font.Font(family='Segoe UI',
              size=12,
              weight='bold',
              underline=0,
              overstrike=0)


status_var = tk.StringVar(root)
status_lab = tk.Label(root, textvariable=status_var, font=FONT)
status_lab.pack()

# -----------------------------------------------------------------------



style = ttk.Style()
style.configure("Treeview", font=('Britannic', 11, 'bold'), rowheight=25)
style.configure("Treeview.Heading", font=('Britannic' ,13, 'bold'))

# Tkinter Bug Work Around
if root.getvar('tk_patchLevel')=='8.6.9': #and OS_Name=='nt':
    def fixed_map(option):
        # Fix for setting text colour for Tkinter 8.6.9
        # From: https://core.tcl.tk/tk/info/509cafafae
        #
        # Returns the style map for 'option' with any styles starting with
        # ('!disabled', '!selected', ...) filtered out.
        #
        # style.map() returns an empty list for missing options, so this
        # should be future-safe.
        return [elm for elm in style.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]
    style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))

# -----------------------------------------------------------------------

entry_frame = tk.Frame(root)
entry_frame.pack(padx=10, pady=10)

cal_lab = tk.Label(entry_frame, text='Date: ', font=FONT)
cal = tkcal.DateEntry(entry_frame, selectmode='day', locale='en_IN')
cal_lab.grid(row=0, column=0, padx=20)
cal.grid(row=1, column=0, padx=20)

capital_lab = tk.Label(entry_frame, text="Capital", font=FONT)
capital_lab.grid(row=0, column=1, padx=10, pady=5)

capital_entry = ttk.Entry(entry_frame, width=10)
capital_entry.grid(row=1, column=1, padx=10, pady=5)

def add_capital():
    complete = db.connect(db.add_capital, cal.get(), capital_entry.get())
    if complete: print("done")
    else: print("ERROR")

capital_btn = ttk.Button(entry_frame, text="Add Capital", command=add_capital).grid(column=2, row=0, rowspan=2, padx=10)

daily_cal_lab = tk.Label(entry_frame, text='Date', font=FONT)
daily_cal = tkcal.DateEntry(entry_frame, selectmode='day', locale='en_IN')
daily_cal_lab.grid(row=0, column=3, padx=20)
daily_cal.grid(row=1, column=3, padx=20)

profit_lab = tk.Label(entry_frame, text="Profit", font=FONT)
profit_lab.grid(row=0, column=4, padx=10, pady=5)
profit_entry = ttk.Entry(entry_frame, width=10)
profit_entry.grid(row=1, column=4, padx=10, pady=5)

def add_profit():
    complete = db.connect(db.add_profit, daily_cal.get(), profit_entry.get())
    if complete: print("done")
    else: print("ERROR")

profit_btn = ttk.Button(entry_frame, text="Add Profit", command=add_profit).grid(column=5, row=0, rowspan=2, padx=10)



root.mainloop()
