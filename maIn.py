
import tkinter as tk
from tkinter import ttk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import tkcalendar as tkcal 
from datetime import datetime
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
style.configure("Treeview", font=('Britannic', 12, 'bold'), columnwidth=5)
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
cal = tkcal.DateEntry(entry_frame, selectmode='day')
cal_lab.grid(row=0, column=0, padx=20)
cal.grid(row=1, column=0, padx=20)

capital_lab = tk.Label(entry_frame, text="Capital", font=FONT)
capital_lab.grid(row=0, column=1, padx=10, pady=5)
capital_var = tk.StringVar(root, value="0")
capital_entry = ttk.Entry(entry_frame, textvariable= capital_var, width=10)
capital_entry.grid(row=1, column=1, padx=10, pady=5)
capital_var.set("0")

'''capital_btn = ttk.Button(entry_frame, text="Add Capital", command=add_capital).grid(column=2, row=0, rowspan=2, padx=10)

daily_cal_lab = tk.Label(entry_frame, text='Date', font=FONT)
daily_cal = tkcal.DateEntry(entry_frame, selectmode='day', locale='en_IN')
daily_cal_lab.grid(row=0, column=3, padx=20)
daily_cal.grid(row=1, column=3, padx=20)'''

profit_lab = tk.Label(entry_frame, text="Profit", font=FONT)
profit_lab.grid(row=0, column=2, padx=10, pady=5)
profit_var = tk.StringVar(root)
profit_entry = ttk.Entry(entry_frame, textvariable= profit_var, width=10)
profit_entry.grid(row=1, column=2, padx=10, pady=5)

def save_data():
    date = cal.get_date().strftime('%Y%m%d')
    profit = float(profit_var.get())
    capital = float(capital_var.get())
    if not db.connect(db.valid_date, date):
        print("ERROR")
        return
    last_data = db.connect(db.fetch_last_row)
    if last_data:
        opening = last_data[-1]        
    else:
        opening = 0
    closing = opening + profit + capital

    db.connect(db.add_record, date, opening, profit, closing, capital) 
    show_query()


save_btn = ttk.Button(entry_frame, text="Save", command=save_data).grid(column=3, row=0, rowspan=2, padx=10)

query_frame_top = tk.Frame(root)
query_frame_top.pack()

query_lab = tk.Label(query_frame_top, text="Query", font=FONT)
query_lab.pack(pady=5)

query_frame = tk.Frame(query_frame_top)
query_frame.pack()

from_cal_lab = tk.Label(query_frame, text='From: ', font=FONT)
from_cal = tkcal.DateEntry(query_frame, selectmode='day')
from_cal_lab.grid(row=0, column=0, padx=20)
from_cal.grid(row=1, column=0, padx=20)

to_cal_lab = tk.Label(query_frame, text='To: ', font=FONT)
to_cal = tkcal.DateEntry(query_frame, selectmode='day')
to_cal_lab.grid(row=0, column=1, padx=20)
to_cal.grid(row=1, column=1, padx=20)

def plot_graph(start, end):
    try:
        plt.close()
    except Exception as e:
        print(e)

    data = db.connect(db.get_data, start, end)
    x = [datetime.strptime(i[0], '%Y%m%d').strftime('%d-%m-%y') for i in data]
    y = [i[-1] for i in data]
    for i, v in enumerate(y):
        plt.text(i, v+100, "%d" %v, ha="center")
    plt.plot(x, y)

    opening = data[0][1]
    if opening == 0.0:
        opening = data[0][3]
    with open("config.txt") as f:
        percents = [float(x.strip()) / 100 for x in f.readlines()]
        for i , percent in enumerate(percents):
            target = opening + (percent * opening)
            plt.axhline(target)
            plt.text(len(y) - 1, target+2500, "%d" %target, ha="center")

    plt.xlabel('Date')
    plt.ylabel('Closing in Rs.')
    plt.title(f'Daily Closing between {x[0]} and {x[-1]}')
    plt.show()

def show_query():
    from_date = from_cal.get_date().strftime('%Y%m%d')
    to_date = to_cal.get_date().strftime('%Y%m%d')
    for i in tv.get_children():
        tv.delete(i)
    data = db.connect(db.get_data, from_date, to_date)
    
    for i,row in enumerate(data):
        formatted_date = datetime.strptime(row[0], '%Y%m%d').strftime('%d-%m-%Y')
        tv.insert(parent='', index=i, iid=i, values=(formatted_date, *row[1:]))
    plot_graph(from_date, to_date)
    
    

query_btn = ttk.Button(query_frame, text="Show", command=show_query).grid(column=2, row=0, rowspan=2, padx=10)

result_frame = tk.Frame(root)
result_frame.pack()

tv = ttk.Treeview(
    result_frame, 
    columns=(1, 2, 3, 4, 5), 
    show='headings', 
    height=10
)
tv.grid(row=0, column=0, pady=10)

tv.heading(1, text='Day')
tv.column(1, minwidth=10, width=100) 
tv.heading(2, text='Opening')
tv.column(2, minwidth=10, width=100)
tv.heading(3, text='Result')
tv.column(3, minwidth=10, width=100)
tv.heading(4, text='Capital Add.')    
tv.column(4, minwidth=10, width=100)
tv.heading(5, text='Closing')    
tv.column(5, minwidth=10, width=100)


root.mainloop()
