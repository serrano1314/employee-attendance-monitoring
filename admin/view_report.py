from config_var import *

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image

def view_report(self,menu_page):
    view_report_page = Tk()
    view_report_page.title('Add Record')
    view_report_page.geometry(WINDOW_SIZE)
    view_report_page.config(bg=BGCOLOR)

    btn= Button(view_report_page,text='hello',bg='#ffffff',bd=0)
    btn.pack()

    view_report_page.protocol("WM_DELETE_WINDOW", lambda: [view_report_page.destroy(), menu_page.deiconify()])
    view_report_page.mainloop