from tkinter import *
from config_var import *
from tkinter import messagebox
from tkinter import ttk

def edit_profile(self, id, root):
    global new_fname, new_lname, new_sex
    # fetch necessary info of employees
    self.c.execute("SELECT first_name, last_name, sex FROM employees WHERE employee_id = '{}'".format(id))
    result = self.c.fetchone()
    self.connection.commit()

    # edit profile window
    edit_profile = Toplevel()
    edit_profile.title('EDIT PROFILE')
    edit_profile.geometry('400x300')
    edit_profile.config(bg=BGCOLOR)

    Label(edit_profile, height=3, width=400, bg=HEADER_COLOR, text='EDIT PROFILE', font=FONT).pack(pady=(0, 10))

    new_sex = StringVar()
    edit = Frame(edit_profile, bg=BGCOLOR)
    edit.pack()

    Label(edit, text='FIRST NAME: ', bg=BGCOLOR).grid(row=0, column=0, pady=10)
    new_fname = Entry(edit, width=20)
    new_fname.grid(row=0, column=1)
    new_fname.insert(0, result[0])

    Label(edit, text='LAST NAME: ', bg=BGCOLOR).grid(row=1, column=0, pady=10)
    new_lname = Entry(edit, width=20)
    new_lname.grid(row=1, column=1)
    new_lname.insert(0, result[1])

    Label(edit, text='SEX: ', bg=BGCOLOR).grid(row=2, column=0, pady=10)
    new_sex.set(result[2])
    option = OptionMenu(edit, new_sex, 'MALE', 'FEMALE')
    option.grid(sticky='W', row=2, column=1)

    Button(edit, text='SAVE', bg='#AAFE92',
           command=lambda: [edit_profile_query(self, (new_fname.get(), new_lname.get(), new_sex.get(), id)),
                            edit_profile.destroy(), self.employee_page(root, id)]).grid(row=3, column=2)

    Button(edit, text='CANCEL', bg='#e4bad4',
           command=lambda: [edit_profile.destroy(), self.employee_page(root, id)]).grid(row=3, column=1)

    # check if the Exit th Window Manually
    edit_profile.protocol("WM_DELETE_WINDOW", lambda: [edit_profile.destroy(), self.employee_page(root, id)])
    edit_profile.mainloop()


def edit_profile_query(self, data):
    # edit profile query
    self.c.execute(f"""UPDATE employees
    SET first_name = ?,
    last_name = ?,
    sex = ?
    WHERE employee_id = ?""", data)
    self.connection.commit()

def edit_password(self, id):
    # Edit password window
    edit_pass = Toplevel()
    edit_pass.geometry('400x300')
    edit_pass.resizable(False, False)
    edit_pass.title('EDIT PASSWORD')
    edit_pass.config(bg=BGCOLOR)

    # Label header
    Label(edit_pass, height=3, width=400, bg=HEADER_COLOR, text='EDIT PASSWORD', font=FONT).pack(pady=(0, 10))
    edit_pass_frame = Frame(edit_pass, bg=BGCOLOR)
    edit_pass_frame.pack(fill=BOTH)

    Label(edit_pass_frame, text='CURRENT PASSWORD:', bg=BGCOLOR).grid(sticky='W', row=0, column=0, padx=10, pady=10)
    current_password = Entry(edit_pass_frame, show='*')
    current_password.grid(row=0, column=1, columnspan=2)

    Label(edit_pass_frame, text='NEW PASSWORD:', bg=BGCOLOR).grid(sticky='W', row=1, column=0, padx=10, pady=10)
    new_password = Entry(edit_pass_frame)
    new_password.grid(row=1, column=1, columnspan=2)

    Button(edit_pass_frame, text='SAVE', bg='#AAFE92',
           command=lambda: [edit_password_query(self, id, current_password, new_password, edit_pass)]).grid(row=2,
                                                                                                           column=2,
                                                                                                           pady=10)

    Button(edit_pass_frame, text='CANCEL', bg='#FE9292', command=edit_pass.destroy).grid(row=2, column=1, pady=10)
    edit_pass.mainloop()


def edit_password_query(self, id, current, new, page):
    # Edit password query
    self.c.execute(f"SELECT * FROM employees WHERE employee_id = '{id}'")
    result = self.c.fetchone()
    self.connection.commit()
    if result[1] == current.get():
        self.c.execute(f"UPDATE employees SET password = '{new.get()}' WHERE employee_id = {id}")
        self.connection.commit()
        messagebox.showinfo('INFORMATION', 'CHANGED SUCCESSFULLY')
        page.destroy()
    else:
        messagebox.showinfo('WRONG PASSWORD', 'INCORRECT PASSWORD')


def employee_records(self, id):
    self.c.execute(f"SELECT * FROM employee_attendance WHERE employee_id = '{id}'")
    result = self.c.fetchall()
    employee_records_page = Toplevel()
    employee_records_page.title('Employee Records')
    employee_records_page.geometry('700x300')
    employee_records_page.config(bg=BGCOLOR)

    Label(employee_records_page, width=400, height=2, bg=HEADER_COLOR, text='EMPLOYEE RECORDS').pack()
    employee_records_frame = Frame(employee_records_page, bg=BGCOLOR)
    employee_records_frame.pack()

    scrollbar = Scrollbar(employee_records_frame, orient=VERTICAL)

    tree = ttk.Treeview(employee_records_frame, yscrollcommand=scrollbar.set, height=5)

    scrollbar.config(command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    tree['columns'] = ('DATE', 'TIME IN', 'STATUS', 'TIME OUT')
    tree.column('#0', width=0, stretch=NO)
    tree.column('DATE', width=160, minwidth=65, anchor=CENTER)
    tree.column('TIME IN', width=160, minwidth=65, anchor=CENTER)
    tree.column('STATUS', width=160, minwidth=65, anchor=CENTER)
    tree.column('TIME OUT', width=160, minwidth=65, anchor=CENTER)

    tree.heading('#0', text='')
    tree.heading('DATE', text='DATE', anchor=CENTER)
    tree.heading('TIME IN', text='TIME IN', anchor=CENTER)
    tree.heading('STATUS', text='STATUS', anchor=CENTER)
    tree.heading('TIME OUT', text='TIME OUT', anchor=CENTER)

    row = 0
    for data in result:
        tree.insert(parent='', index='end', iid=row, text='', values=(data[1], data[2], data[3], data[4]))
        row += 1

    tree.pack(pady=10)

    Button(employee_records_frame, bg='#ff79cd', text='Back', command=employee_records_page.destroy).pack(pady=10,
                                                                                                          anchor='w')
    employee_records_page.mainloop()