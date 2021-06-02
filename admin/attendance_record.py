from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime, date
from config_var import *

def attendance_record(self, root_page, date):
    # Making attendance window
    attendance_page = Toplevel()
    attendance_page.title('Attendance')
    attendance_page.geometry('1100x600')
    attendance_page.config(bg=BGCOLOR)
    th_font = 'Arial 12 bold'
    cell_size = 150
    mid_cell_size = 25
    # Attendance Header
    Label(attendance_page, width=400, height=3, text='ATTENDANCE RECORD', bg=HEADER_COLOR, font=FONT).pack()

    # Attendance Frame
    attendance_header = Frame(attendance_page, bg=BGCOLOR)
    attendance_header.pack()

    # Date now
    Label(attendance_header, text='Attendance Date for:', bg=BGCOLOR).grid(row=1, column=3, padx=(30, 0))

    # Date and time now
    current_date = Label(attendance_header, text=date, bg=BGCOLOR)
    current_date.grid(row=1, column=4, padx=(0, 70))

    # Picked attendance date
    Button(attendance_header, text='SET ATTENDANCE DATE', bg='#1eae98', command=lambda: [choose_date(self,attendance_page,root_page)]).grid(row=1, column=1)

    # day and time today
    dates = Label(attendance_header, bg=BGCOLOR, font=FONT)
    dates.grid(row=0, column=5, pady=10, columnspan=3)
    self.current_time(dates)
    
    table_frame = Frame(attendance_page)
    table_frame.pack(pady=10)

    #for table's scrollbar
    scrollbary = Scrollbar(table_frame, orient=VERTICAL)
    # Field data
    self.attendance_tree = ttk.Treeview(table_frame,selectmode=BROWSE,yscrollcommand=scrollbary.set,height=15)
    scrollbary.config(command=self.attendance_tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    self.attendance_tree['columns'] = ('EMPLOYEE ID', 'FIRST NAME', 'LAST NAME', 'DATE','TIME IN','STATUS', 'TIME OUT')
    self.attendance_tree.column('#0',width=0,stretch=NO)
    self.attendance_tree.column('EMPLOYEE ID',width=cell_size,minwidth=mid_cell_size,anchor=CENTER)
    self.attendance_tree.column('FIRST NAME',width=cell_size,minwidth=mid_cell_size,anchor=W)
    self.attendance_tree.column('LAST NAME',width=cell_size,minwidth=mid_cell_size,anchor=W)
    self.attendance_tree.column('DATE',width=cell_size,minwidth=mid_cell_size,anchor=CENTER)
    self.attendance_tree.column('TIME IN',width=cell_size,minwidth=mid_cell_size,anchor=CENTER)
    self.attendance_tree.column('STATUS',width=cell_size,minwidth=mid_cell_size,anchor=CENTER)
    self.attendance_tree.column('TIME OUT', width=cell_size, minwidth=mid_cell_size, anchor=CENTER)

    self.attendance_tree.heading('#0',text='')
    self.attendance_tree.heading('EMPLOYEE ID',text='EMPLOYEE ID',anchor=CENTER)
    self.attendance_tree.heading('FIRST NAME',text='FIRST NAME',anchor=CENTER)
    self.attendance_tree.heading('LAST NAME',text='LAST NAME',anchor=CENTER)
    self.attendance_tree.heading('DATE',text='DATE',anchor=CENTER)
    self.attendance_tree.heading('TIME IN',text='TIME IN',anchor=CENTER)
    self.attendance_tree.heading('STATUS',text='STATUS',anchor=CENTER)
    self.attendance_tree.heading('TIME OUT', text='TIME OUT', anchor=CENTER)
    # Query for getting the data with status
    if date == '':
        self.c.execute(f'''SELECT A.employee_id, first_name, last_name, attendance_date, time_in, status, time_out, A.oid
                    FROM employee_attendance A, employees B
                    where A.employee_id = B.employee_id
					ORDER BY A.oid DESC''')
    else:
        self.c.execute(f'''SELECT A.employee_id, first_name, last_name, attendance_date, time_in, status, time_out
                                FROM employee_attendance A, employees B
                                where A.employee_id = B.employee_id AND attendance_date = "{date}"''')

    records = self.c.fetchall()        
    #insert data
    count=0
    for record in records:
        self.attendance_tree.insert(parent='',index='end',iid=count,text='',
        values=(record[0],record[1],record[2],record[3],record[4],record[5], record[6]))
        count+=1

    self.attendance_tree.pack()

    # Save Button
    # Button(attendance_header, text='Save', bg='#3edbf0', width=10, command=lambda: [attendance_page.destroy(), root_page.deiconify()]).grid(row=data_row + 1, column=4, pady=10)

    # Cancel Button
    back_btn=Button(attendance_page, image=self.back_img, bd=0, bg=BGCOLOR, command=lambda: [attendance_page.destroy(), root_page.deiconify()])
    back_btn.place(x=990,y=525)

    # Check if the User Manually Exit Window
    attendance_page.protocol("WM_DELETE_WINDOW", lambda: [attendance_page.destroy(), root_page.deiconify()])

def choose_date(self,root ,root_root):
    # Window Creation
    date_page = Toplevel()
    date_page.geometry('300x150')
    date_page.title('Date')
    # Getting the Date Today
    today = date.today()
    current_day = today.strftime('%d')
    current_month = today.strftime('%b')
    current_year = today.strftime('%Y')

    # Header Frame
    Label(date_page, text='Set Attendance Date', width=400, height=2, bg=HEADER_COLOR).pack()
    date_frame = Frame(date_page)
    date_frame.pack()

    # Month, Day, Year Label
    Label(date_frame, text='Month').grid(row=0, column=0, pady=5)
    Label(date_frame, text='Day').grid(row=0, column=1, pady=5)
    Label(date_frame, text='Year').grid(row=0, column=2, pady=5)

    # Month Dropdown
    choice = StringVar()
    choice.set(current_month)
    option = OptionMenu(date_frame, choice, 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
    option.grid(row=1, column=0, padx=5)

    # Day
    day = Entry(date_frame, width=10)
    day.grid(row=1, column=1, padx=10)
    day.insert(0, current_day)

    # Year
    year = Entry(date_frame, width=10)
    year.grid(row=1, column=2, padx=10)
    year.insert(0, current_year)

    # Confirm Button
    Button(date_frame, text='Confirm', bg='#AAFE92', command=lambda : [root.destroy(), attendance_record(self,root_root, f'{choice.get()}-{day.get()}-{year.get()}'), date_page.destroy()]).grid(row=2, column=2, pady=10)

    # Cancel Button
    Button(date_frame, text='Cancel', bg='#e4bad4', command=date_page.destroy).grid(row=2, column=1, pady=10)

    date_page.mainloop()