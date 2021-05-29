# Imports
from sqlite3.dbapi2 import Row
from tkinter import *
from tkinter import messagebox, ttk
from PIL import ImageTk, Image
from datetime import datetime, date
import sqlite3
import re

WINDOW_SIZE = '1000x580'
FONT = ('Verdana', 15)
BGCOLOR='#FAF1E6'
HEADER_COLOR='#7EE5FF'

class Main:
    def __init__(self):
        # Root window creation
        root = Tk()
        root.title('Student Attendance Monitoring System')
        root.geometry(WINDOW_SIZE)
        root.config(bg=BGCOLOR)

        # Employee Information Initialization
        self.employee_id = ''
        self.password = ''
        self.first_name = ''
        self.last_name = ''
        self.sex = StringVar()
        self.schedule_in = ''
        self.schedule_out = ''
        # Creating database& Table & connecting
        self.connection = sqlite3.connect('database employee.db')

        # Creating Cursor to the Database
        self.c = self.connection.cursor()
        # Creating Table

        try:
            self.c.execute("""CREATE TABLE employees(
                                       employee_id text,
                                       password text,
                                       first_name text,
                                       last_name text,
                                       sex text,
                                       schedule_in,
                                       schedule_out
                               )""")
            self.connection.commit()

        except sqlite3.OperationalError:
            print('Table already made')

        #create table for employee attendance
        try:
            self.c.execute("""CREATE TABLE employee_attendance(
                                       employee_id text,
                                       attendance_date text,
                                       time_in text,
                                       status text
                               )""")
            self.connection.commit()

        except sqlite3.OperationalError:
            print('Table for attendance already made')

        else:
            # Creating admin account
            # self.c.execute(f"""INSERT INTO employees VALUES(
            # 'admin',
            # '1234',
            # 'Steven',
            # 'Serrano',
            # 'MALE',
            # 'MANAGER',
            # 'MANAGER'
            # )""")
            # self.connection.commit()
            pass

        # App Logo
        self.app_logo = ImageTk.PhotoImage(Image.open('1622028910602.png').resize((150, 150), Image.ANTIALIAS))

        # Opening root window
        self.starting(root)

    def starting(self, root):
        global username, password
        # Creating frame to center widgets
        login_bg = ImageTk.PhotoImage(Image.open('bg/login_bg.png').resize((1000, 580), Image.ANTIALIAS))
        login_img = ImageTk.PhotoImage(Image.open('bts_biot/login_btn.png').resize((80, 30), Image.ANTIALIAS))
        exit_img = ImageTk.PhotoImage(Image.open('bts_biot/exit_btn.png').resize((80, 30), Image.ANTIALIAS))
        login_bg_lbl = Label(root,image=login_bg)
        login_bg_lbl.place(x=0,y=0)
        main_frame = Frame(root)
        # main_frame.pack()

        
        # Application Logo
        # Label(main_frame, image=self.app_logo, bg=BGCOLOR).grid(row=0, column=1,pady=(50,0))

        # User name Entry
        # Label(root, text='Username/ID', bg=BGCOLOR).grid(row=1, column=1, pady=(20, 10), padx=(50, 180))
        username = Entry(root, width=30, bd=0)
        username.pack(pady=(260,50))

        # Password Entry
        # Label(root, text='Password', bg=BGCOLOR).grid(row=3, column=1,pady=(20, 10), padx=(50, 180))
        password = Entry(root, width=30, show="*",bd=0)
        password.pack(pady=(3,50))

        # Log in Button
        login_button = Button(root, image=login_img, border=0, command=lambda: [self.menu(root)])
        login_button.pack(pady=10)

        # Exit Button
        exit_button = Button(root, image=exit_img, border=0, command=lambda: [root.destroy(), self.connection.close()])
        exit_button.pack()

        # Hover ek ek
        login_button.bind("<Enter>", self.enter)
        login_button.bind("<Leave>", self.exit)
        exit_button.bind("<Enter>", self.enter)
        exit_button.bind("<Leave>", self.exit)

        # pressing Enter key will trigger the menu function, same what login button does
        global temp_root
        temp_root=root
        password.bind('<Return>',self.pressed_enter)
        username.bind('<Return>',self.pressed_enter)
        
        root.mainloop()

    def pressed_enter(self,e):
        self.menu(temp_root)

    def enter(self, e):
        e.widget['background'] = '#c8c2bc'

    def exit(self, e):
        e.widget['background'] = BGCOLOR

    def menu(self, root):
        # Checking if the Username exist
        self.c.execute(f"SELECT * FROM employees WHERE employee_id = '{username.get()}'")
        content = self.c.fetchone()
        self.connection.commit()

        if content != None and username.get() != '' and password != '':
            # Checking if it is an admin account
            if username.get() == 'admin' and password.get() == content[1]:
                # Hide Main Window
                root.withdraw()
                username.delete(0, END)
                password.delete(0, END)

                # Create Menu Window
                menu_page = Toplevel()
                menu_page.title('Student Attendance Monitoring System')
                menu_page.config(bg=BGCOLOR)
                menu_page.geometry(WINDOW_SIZE)

                # CREATING FRAME TO CENTER WIDGETS
                menu_frame = Frame(menu_page, bg=BGCOLOR)
                menu_frame.pack()

                # Current Time Label
                time_label = Label(menu_frame, bg=BGCOLOR,font=FONT)
                time_label.grid(row=0, column=3, padx=(0, 30), pady=20)
                self.current_time(time_label)

                button_h=4
                button_w=15

                # Logo
                Label(menu_frame, image=self.app_logo, bg=BGCOLOR).grid(row=1, column=3, rowspan=2, pady=20, padx=20)

                # Add Button
                add_employee = ImageTk.PhotoImage(Image.open("bts_biot/add_record_logo.png").resize((120, 120), Image.ANTIALIAS))
                add_button = Button(menu_frame, image=add_employee, bg=BGCOLOR, border=0,command=lambda: [menu_page.withdraw(), self.add_record(menu_page)])
                add_button.grid(row=1, column=1, pady=20, padx=(0, 100))

                # View Report Button
                view_report = ImageTk.PhotoImage(Image.open('bts_biot/view_report logo.png').resize((120, 120), Image.ANTIALIAS))
                view_report_button = Button(menu_frame, image=view_report, bg=BGCOLOR, border=0)
                view_report_button.grid(row=1, column=2, pady=20, padx=(20, 0))

                # View Record Button
                view_record = ImageTk.PhotoImage(Image.open('bts_biot/view_record_logo.png').resize((120, 120), Image.ANTIALIAS))
                view_button = Button(menu_frame, image=view_record, bg=BGCOLOR, border=0,command=lambda: [menu_page.withdraw(), self.show_records(menu_page)], relief=RAISED)
                view_button.grid(row=2, column=1, pady=20, padx=(0, 100))

                # Attendance
                attendance = ImageTk.PhotoImage(Image.open('bts_biot/attendance_logo.png').resize((120, 120), Image.ANTIALIAS))
                attendance_button = Button(menu_frame, image=attendance, bg=BGCOLOR, border=0, command=lambda: [self.attendance(menu_page, ""), menu_page.withdraw()])
                attendance_button.grid(row=2, column=2, pady=20, padx=(20, 0))

                # Cancel Button
                Button(menu_frame, text='Log Out', bg='#ff79cd',command=lambda: [menu_page.destroy(), root.deiconify()]).grid(row=3, column=0, pady=20, padx=20)

                # check if the Exit th Window Manually
                menu_page.protocol("WM_DELETE_WINDOW", lambda: [menu_page.destroy(), root.deiconify()])

                # Hover ek ek
                add_button.bind("<Enter>", self.enter)
                add_button.bind("<Leave>", self.exit)
                view_report_button.bind("<Enter>", self.enter)
                view_report_button.bind("<Leave>", self.exit)
                view_button.bind("<Enter>", self.enter)
                view_button.bind("<Leave>", self.exit)
                attendance_button.bind("<Enter>", self.enter)
                attendance_button.bind("<Leave>", self.exit)
                menu_page.mainloop()
            elif username.get() != 'admin' and content[0] == username.get() and content[1] == password.get():
                # Hide Main Window
                root.withdraw()
                username.delete(0, END)
                password.delete(0, END)

                # THIS IS AN EMPLOYEE ACCOUNT
                self.employee_page(root, content[0])
            else:
                messagebox.showwarning('Warning', 'Invalid Password')
        else:
            messagebox.showwarning('Warning', 'Invalid Password')

    #convert the string time format into maderpaking list 
    def format_time_to_list(self,time_str):
        time_list = [int(i) for i in re.findall('[0-9][0-9]', time_str)]
        if 'PM' in time_str and time_list[0]<12:
            time_list[0]+=12

        if 'AM' in time_str and time_list[0]==12:
            time_list[0]-=12

        return time_list

    def time_in_query(self,id):
        date_time_now = datetime.now()
        date_now = date_time_now.strftime('%b-%d-%Y')
        time_now = date_time_now.strftime('%I:%M %p')
        
        # check if the user already time in today
        self.c.execute(f"SELECT time_in FROM employee_attendance WHERE employee_id = ? AND attendance_date = ?",
                       (id, date_now))
        result = self.c.fetchall()
        self.connection.commit()
        if len(result) <= 0:
            self.c.execute(f"SELECT schedule_in, schedule_out FROM employees WHERE employee_id = '{id}'")
            status={
                'present':'PRESENT',
                'late':'LATE',
                'absent':'ABSENT'
            }
            attendance_status=''
            result = self.c.fetchone()
            sched_in = self.format_time_to_list(result[0])
            sched_out = self.format_time_to_list(result[1])

            time_in = self.format_time_to_list(date_time_now.strftime('%I:%M %p'))
            if sched_in[0] == time_in[0]:
                if time_in[1] <= sched_in[1]:
                    attendance_status=status['present']
                elif time_in[1] > sched_in[1] and time_in[1] <= sched_out[1]:
                    attendance_status=status['late']
                elif time_in[1] > sched_out[1]:
                    attendance_status=status['absent']
            else:
                if time_in[0] <= sched_in[0]:
                    attendance_status=status['present']
                elif time_in[0] > sched_in[0] and time_in[0] <= sched_out[0]:
                    attendance_status=status['late']
                elif time_in[0] > sched_out[0]:
                    attendance_status=status['absent']

            self.c.execute(f"""INSERT INTO employee_attendance VALUES(
                '{id}',
                '{date_now}',
                '{time_now}',
                '{attendance_status}',
                'None'
                )""")
            self.connection.commit()
            messagebox.showinfo('INFORMATION', f'You are {attendance_status.title()} for today.')
        else:
            messagebox.showinfo('INFORMATION', 'You Already Time in Today')

    def time_out_query(self, id):
        date = datetime.now()
        time_now = date.strftime('%I:%M %p')
        self.c.execute(f"SELECT * FROM employee_attendance WHERE employee_id = '{id}' and time_out = 'None'")
        result = self.c.fetchone()
        self.connection.commit()
        if result != None:
            self.c.execute(f"UPDATE employee_attendance SET time_out = ? WHERE employee_id = ? AND time_out = 'None'", (time_now, id))
            self.connection.commit()
            messagebox.showinfo('INFORMATION', 'THANK YOU')
        else:
            messagebox.showinfo('INFORMATION', 'YOU ALREADY TIMED OUT OR NOT TIMED IN YET')

    def employee_records(self, id):
        self.c.execute(f"SELECT * FROM employee_attendance WHERE employee_id = '{id}'")
        result = self.c.fetchall()
        employee_records_page = Toplevel()
        employee_records_page.title('Employee Records')
        employee_records_page.geometry('700x300')

        Label(employee_records_page, width=400, height=2, bg=HEADER_COLOR, text='EMPLOYEE RECORDS').pack()
        employee_records_frame = Frame(employee_records_page)
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

        row=0
        for data in result:
            tree.insert(parent='', index='end', iid=row, text='', values=(data[1], data[2], data[3], data[4]))
            row +=1

        tree.pack(pady=10)

        Button(employee_records_frame, bg='#ff79cd', text='Back', command=employee_records_page.destroy).pack(pady=10, anchor='w')
        employee_records_page.mainloop()

    def employee_page(self, root, id):
        # Fetch employee profile
        self.c.execute(f"SELECT * FROM employees WHERE employee_id = '{id}'")
        content = self.c.fetchone()

        # Create Employee  Window
        employee_menu_page = Toplevel()
        employee_menu_page.title('Student Attendance Monitoring System')
        employee_menu_page.config(bg=BGCOLOR)
        employee_menu_page.geometry('500x400')

        button_h = 4
        button_w = 15

        Label(employee_menu_page, height=3, width=400, bg=HEADER_COLOR, text='EMPLOYEE', font=FONT).pack(pady=(0, 10))

        employee_menu_frame = Frame(employee_menu_page, bg=BGCOLOR)
        employee_menu_frame.pack()

        # Header
        Label(employee_menu_frame, text='WELCOME,', bg=BGCOLOR, font=FONT).grid(sticky='W', row=0, column=0,
                                                                                  columnspan=2)
        Label(employee_menu_frame, text=content[2], bg=BGCOLOR, font=FONT).grid(sticky='W', row=1, column=0, padx=5)
        Label(employee_menu_frame, text=content[3], bg=BGCOLOR, font=FONT).grid(sticky='W', row=1, column=1, padx=5,
                                                                                  columnspan=2)
        Label(employee_menu_frame, text=f'YOUR SCHEDULE: {content[5]} to {content[6]}', bg=BGCOLOR,).grid(sticky='W', row=1, column=2, padx=5,
                                                                                  columnspan=2)

        # time and date today
        emp = Label(employee_menu_frame, bg=BGCOLOR, font=('Verdana', 10), width=40)
        emp.grid(row=2, column=1, columnspan=2)
        self.current_time(emp)

        # time in button
        Button(employee_menu_frame, text='TIME IN', width=button_w, height=button_h, bg='#a5e1ad',
               font=('Verdana', 10),command=lambda: self.time_in_query(id)).grid(sticky='W', row=3, column=1, rowspan=2, pady=10, padx=20)

        # time out button
        Button(employee_menu_frame, text='TIME OUT', width=button_w, height=button_h, bg='#f29191',
               font=('Verdana', 10), command=lambda: self.time_out_query(id)).grid(sticky='W', row=5, column=1, pady=10, rowspan=2, padx=20)

        # View Records Button
        Button(employee_menu_frame, text='VIEW RECORDS', bg='#c0fefc', width=20, command=lambda: self.employee_records(content[0])).grid(sticky='S', row=3, column=2,
                                                                                      pady=10, padx=20)

        # Edit Profile Button
        Button(employee_menu_frame, text='EDIT PROFILE', bg='#c0fefc', width=20,
               command=lambda: [employee_menu_page.destroy(), self.edit_profile(content[0], root)]).grid(sticky='N', row=4, column=2,
                                                                                         pady=10, padx=20)

        # Edit Password Button
        Button(employee_menu_frame, text='CHANGE PASSWORD', bg='#c0fefc', width=20, command=lambda: self.edit_password(id)).grid(sticky='N', row=5, column=2,
                                                                                         pady=10, padx=20)
                                                                            
        Button(employee_menu_frame, text='Log Out', bg='#ff79cd',command=lambda: [employee_menu_page.destroy(), root.deiconify()]).grid(row=6, column=2)
        # check if the Exit th Window Manually
        employee_menu_page.protocol("WM_DELETE_WINDOW", lambda: [employee_menu_page.destroy(), root.deiconify()])

        employee_menu_page.mainloop()

    def edit_password(self, id):
        # Edit password window
        edit_pass = Toplevel()
        edit_pass.geometry('400x300')
        edit_pass.title('EDIT PASSWORD')

        # Label header
        Label(edit_pass, height=3, width=400, bg=HEADER_COLOR, text='EDIT PASSWORD', font=FONT).pack(pady=(0, 10))
        edit_pass_frame = Frame(edit_pass)
        edit_pass_frame.pack(fill=BOTH)

        Label(edit_pass_frame, text='CURRENT PASSWORD:').grid(sticky='W', row=0, column=0, padx=10, pady=10)
        current_password = Entry(edit_pass_frame, show='*')
        current_password.grid(row=0, column=1, columnspan=2)

        Label(edit_pass_frame, text='NEW PASSWORD:').grid(sticky='W',row=1, column=0, padx=10, pady=10)
        new_password = Entry(edit_pass_frame)
        new_password.grid(row=1, column=1, columnspan=2)

        Button(edit_pass_frame, text='SAVE', bg='#AAFE92', command=lambda :[self.edit_password_query(id, current_password, new_password, edit_pass)]).grid(row=2, column=2, pady=10)

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

        Label(edit_profile, height=3, width=400, bg=HEADER_COLOR, text='EDIT PROFILE', font=FONT).pack(pady=(0, 10))

        new_sex = StringVar()
        edit = Frame(edit_profile)
        edit.pack()

        Label(edit, text='FIRST NAME: ').grid(row=0, column=0, pady=10)
        new_fname = Entry(edit, width=20)
        new_fname.grid(row=0, column=1)
        new_fname.insert(0, result[0])

        Label(edit, text='LAST NAME: ').grid(row=1, column=0, pady=10)
        new_lname = Entry(edit, width=20)
        new_lname.grid(row=1, column=1)
        new_lname.insert(0, result[1])

        Label(edit, text='SEX: ').grid(row=2, column=0, pady=10)
        new_sex.set(result[2])
        option = OptionMenu(edit, new_sex, 'MALE', 'FEMALE')
        option.grid(sticky='W', row=2, column=1)

        Button(edit, text='SAVE',bg='#AAFE92', command=lambda :[self.edit_profile_query((new_fname.get(), new_lname.get(), new_sex.get(), id)), edit_profile.destroy(), self.employee_page(root, id)]).grid(row=3, column=2)

        Button(edit, text='CANCEL',bg='#FE9292', command=lambda :[edit_profile.destroy(), self.employee_page(root, id)]).grid(row=3, column=1)

        # check if the Exit th Window Manually
        edit_profile.protocol("WM_DELETE_WINDOW", lambda :[edit_profile.destroy(), self.employee_page(root, id)])
        edit_profile.mainloop()

    def edit_profile_query(self, data):
        # edit profile query
        self.c.execute(f"""UPDATE employees
        SET first_name = ?,
        last_name = ?,
        sex = ?
        WHERE employee_id = ?""", data)
        self.connection.commit()

    def add_record(self, menu_page):
        # Create Window
        global morning, night
        add_record_page = Toplevel()
        add_record_page.title('Add Record')
        add_record_page.geometry('600x580')
        add_record_page.config(bg=BGCOLOR)
        morning = StringVar()
        night = StringVar()
        Label(add_record_page, height=3, width=400, bg=HEADER_COLOR, text='Add Record', font=FONT).pack(pady=(0, 10))

        add_record_frame = Frame(add_record_page, bg=BGCOLOR)
        add_record_frame.pack()

        # Getting the Employee Id
        Label(add_record_frame, text='EMPLOYEE ID:', bg=BGCOLOR).grid(sticky='W', row=0, column=1, pady=(10, 0), padx=10)
        self.employee_id = Entry(add_record_frame, width=40)
        self.employee_id.grid(row=0, column=2, pady=(10, 0), columnspan=2)

        # Getting the password
        Label(add_record_frame, text='PASSWORD: ', bg=BGCOLOR).grid(sticky='W',row=1, column=1, pady=(10, 0), padx=10)
        self.password = Entry(add_record_frame, width=40)
        self.password.grid(row=1, column=2, pady=(10, 0), columnspan=2)

        # Getting the First Name
        Label(add_record_frame, text='FIRST NAME: ', bg=BGCOLOR).grid(sticky='W',row=2, column=1, pady=(10, 0), padx=10)
        self.first_name = Entry(add_record_frame, width=40)
        self.first_name.grid(row=2, column=2, pady=(10, 0), columnspan=2)

        # Getting the Last Name
        Label(add_record_frame, text='LAST NAME: ', bg=BGCOLOR).grid(sticky='W',row=3, column=1, pady=(10, 0), padx=10)
        self.last_name = Entry(add_record_frame, width=40)
        self.last_name.grid(row=3, column=2, pady=(10, 0), columnspan=2)

        # Sex
        Label(add_record_frame, text='SEX: ', bg=BGCOLOR).grid(sticky='W',row=4, column=1, pady=(10, 0), padx=10)
        self.sex.set('MALE')
        option = OptionMenu(add_record_frame, self.sex, 'MALE', 'FEMALE')
        option.grid(sticky='W',row=4, column=2, pady=(10, 0), columnspan=2)

        # Schedule
        Label(add_record_frame, text='SCHEDULE', bg=BGCOLOR, width=10).grid(row=5, column=2, pady=20, columnspan=2)

        # IN
        Label(add_record_frame, text='IN:', bg=BGCOLOR).grid(sticky='W', row=6, column=1)
        self.schedule_in = Entry(add_record_frame, width=10)
        self.schedule_in.grid(row=6, column=2, sticky='W')
        morning.set('AM')
        option_morning = OptionMenu(add_record_frame, morning, 'AM', 'PM')
        option_morning.grid(sticky='W', row=6, column=3, pady=(10, 0))


        # Out
        Label(add_record_frame, text='OUT:', bg=BGCOLOR).grid(sticky='W', row=7, column=1)
        self.schedule_out = Entry(add_record_frame, width=10)
        self.schedule_out.grid(sticky='W', row=7, column=2)
        night.set('PM')
        option_night = OptionMenu(add_record_frame, night, 'AM', 'PM')
        option_night.grid(sticky='W', row=7, column=3, pady=(10, 0))


        # Cancel Button
        Button(add_record_frame, text='Cancel', width=10,  bg='#AAFE92', command=lambda: [add_record_page.destroy(), menu_page.deiconify()]).grid(row=8, column=2, pady=(20, 0))

        # Save Button
        Button(add_record_frame, text='Save', bg='#FE9292', width=10, command=lambda: [self.adding_record(add_record_page, menu_page)]).grid(row=8, column=3, pady=(20, 0))

        # check if user Exit the Window Manually
        add_record_page.protocol("WM_DELETE_WINDOW", lambda: [add_record_page.destroy(), menu_page.deiconify()])

        add_record_page.mainloop()

    def unique_id(self, id):
        self.c.execute(f'SELECT employee_id FROM employees WHERE employee_id = "{id.get()}"')
        result = self.c.fetchall()
        if len(result) <= 0 and id.get() != '':
            return True
        self.connection.commit()

    def adding_record(self, adding_page, menu):
        # adding records to the database

        #validation for time format, can't explain further XD

        if ':' in self.schedule_in.get():
            self.schedule_in = f"{self.schedule_in.get()} {morning.get()}"
        else:
            self.schedule_in = f"{self.schedule_in.get()}:00 {morning.get()}"

        if ':' in self.schedule_out.get():
            self.schedule_out = f"{self.schedule_out.get()} {night.get()}"
        else:
            self.schedule_out = f"{self.schedule_out.get()}:00 {night.get()}"

        if len(self.schedule_in) < 8:
            self.schedule_in = '0'+self.schedule_in

        if len(self.schedule_out) < 8:
            self.schedule_out = '0'+self.schedule_out
            
        if self.unique_id(self.employee_id):
            self.c.execute(f"""INSERT INTO employees VALUES(
            '{self.employee_id.get()}',
            '{self.password.get()}',
            '{self.first_name.get()}',
            '{self.last_name.get()}',
            '{self.sex.get()}',
            '{self.schedule_in}',
            '{self.schedule_out}'
            )""")
            # Apply Changes to the Database
            self.connection.commit()
            adding_page.destroy()
            menu.deiconify()
        else:
            messagebox.showerror('Error', 'Student Id Already Exist or Invalid Input')

    def update_query(self,edit_page,update_id):
        response = messagebox.askyesno('UPDATE RECORD',f'ARE YOU SURE TO UPDATE RECORD FOR {update_id} ?')
        if(response):
            self.c.execute('''UPDATE employees SET
                employee_id = :employee_id,
                password = :password,
                first_name = :first_name,
                last_name = :last_name,
                sex = :sex,
                schedule_in = :schedule_in,
                schedule_out = :schedule_out

                 WHERE employee_id = :update_id''',
                {
                    'employee_id': employee_id_edit.get(),
                    'password': password_edit.get(),
                    'first_name': first_name_edit.get(),
                    'last_name': last_name_edit.get(),
                    'sex': sex_edit.get(),
                    'schedule_in': schedule_in_edit.get(),
                    'schedule_out': schedule_out_edit.get(),

                    'update_id': update_id
                })
            self.c.execute("UPDATE employee_attendance SET employee_id = ? WHERE employee_id = ?", (employee_id_edit.get(), update_id))

            selected = self.tree.focus()
            self.tree.item(selected,text='',values=(employee_id_edit.get(),first_name_edit.get(),
                                                    last_name_edit.get(),sex_edit.get(),
                                                    schedule_in_edit.get(),schedule_out_edit.get()))

            self.connection.commit()
            print('success')
            edit_page.destroy()

    def edit_record(self,page):
        try:
            record_tree = self.tree.selection()[0]
        except:
            messagebox.showinfo('Invalid', 'Please Select a Row in the Table First')
        
        record = self.tree.item(record_tree)
        id = record['values'][0]
        cell_size = 35
        table_col=3
        win_size='400x300'
        
        global employee_id_edit,password_edit,first_name_edit,last_name_edit,sex_edit,schedule_in_edit,schedule_out_edit

        edit_record_page = Tk()
        edit_record_page.title('EDIT EMPLOYEE RECORD')
        edit_record_page.geometry(win_size)
        edit_record_page.config(bg=BGCOLOR)

        Label(edit_record_page,text="EMPLOYEE ID:",bg=BGCOLOR).grid(row=2,column=table_col-1,padx=10,pady=(40,0 ))
        employee_id_edit=Entry(edit_record_page, width=cell_size)
        employee_id_edit.grid(row=2, column=table_col, pady=(40, 0))

        Label(edit_record_page,text="PASSWORD:",bg=BGCOLOR).grid(row=3,column=table_col-1)
        password_edit=Entry(edit_record_page, width=cell_size)
        password_edit.grid(row=3, column=table_col)
        
        Label(edit_record_page,text="FIRST NAME:",bg=BGCOLOR).grid(row=4,column=table_col-1)
        first_name_edit=Entry(edit_record_page, width=cell_size)
        first_name_edit.grid(row=4, column=table_col)

        Label(edit_record_page,text="LAST NAME:",bg=BGCOLOR).grid(row=5,column=table_col-1)
        last_name_edit=Entry(edit_record_page,width=cell_size)
        last_name_edit.grid(row=5,column=table_col)

        Label(edit_record_page,text="SEX:",bg=BGCOLOR).grid(row=6,column=table_col-1)
        sex_edit=Entry(edit_record_page, width=cell_size)
        sex_edit.grid(row=6, column=table_col)

        Label(edit_record_page,text="SCHEDULE IN:",bg=BGCOLOR).grid(row=7,column=table_col-1)
        schedule_in_edit=Entry(edit_record_page, width=cell_size)
        schedule_in_edit.grid(row=7, column=table_col)

        Label(edit_record_page, text="SCHEDULE OUT:",bg=BGCOLOR).grid(row=8, column=table_col - 1)
        schedule_out_edit = Entry(edit_record_page, width=cell_size)
        schedule_out_edit.grid(row=8, column=table_col)



        self.c.execute(f"SELECT * FROM employees WHERE employee_id = '{id}'")
        records=self.c.fetchall()
        
        for record in records:
            employee_id_edit.insert(0, record[0])
            password_edit.insert(0, record[1])
            first_name_edit.insert(0, record[2])
            last_name_edit.insert(0,record[3])
            sex_edit.insert(0, record[4])
            schedule_in_edit.insert(0, record[5])
            schedule_out_edit.insert(0, record[6])

        
        Button(edit_record_page,text="SAVE",width=15,command=lambda:self.update_query(edit_record_page,id),bg='#AAFE92').grid(row=9,column=table_col,pady=20)
        Button(edit_record_page,text="CANCEL",width=15,command=lambda:edit_record_page.destroy(),bg='#FE9292').grid(row=9,column=table_col-1,pady=20,padx=(35,0))
        edit_record_page.mainloop()

    def delete_query(self):
        try:
            record_tree = self.tree.selection()[0]
        except:
            messagebox.showinfo('Invalid', 'Please Select a Row in the Table First')

        record = self.tree.item(record_tree)
        id = record['values'][0]
        response = messagebox.askyesno('DELETE RECORD',f'Delete Record for [{id}] ?')
        if(response):
            print()
            self.tree.delete(record_tree)
            self.c.execute(f"DELETE FROM employees WHERE employee_id = '{id}'")
            self.connection.commit()
            self.c.execute(f"DELETE FROM employee_attendance WHERE employee_id = '{id}'")
            self.connection.commit()

    def show_records(self, root_page):
        cell_size = 165
        mid_cell_size = 25
        win_size='1100x620'
        th_font ='Arial 12 bold'
        show_record_page = Toplevel()
        show_record_page.title('SHOW RECORDS')
        show_record_page.geometry(win_size)
        show_record_page.config(bg=BGCOLOR)
        show_record_frame=Frame(show_record_page,bg=BGCOLOR)
        show_record_frame.pack()
        Label(show_record_frame, height=3, width=600, bg=HEADER_COLOR, text='EMPLOYEE RECORDS', font=FONT).pack(pady=(0, 10))
        #for table's scrollbar
        scrollbary = Scrollbar(show_record_frame, orient=VERTICAL)

        self.tree = ttk.Treeview(show_record_frame,selectmode=BROWSE,yscrollcommand=scrollbary.set,height=20)
        scrollbary.config(command=self.tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        self.tree['columns'] = ('EMPLOYEE ID', 'FIRST NAME', 'LAST NAME', 'SEX', 'SCHEDULE IN','SCHEDULE OUT')
        self.tree.column('#0',width=0,stretch=NO)
        self.tree.column('EMPLOYEE ID',width=cell_size,minwidth=mid_cell_size,anchor=CENTER)
        self.tree.column('FIRST NAME',width=cell_size,minwidth=mid_cell_size,anchor=W)
        self.tree.column('LAST NAME',width=cell_size,minwidth=mid_cell_size,anchor=W)
        self.tree.column('SEX',width=cell_size,minwidth=mid_cell_size,anchor=CENTER)
        self.tree.column('SCHEDULE IN',width=cell_size,minwidth=mid_cell_size,anchor=CENTER)
        self.tree.column('SCHEDULE OUT',width=cell_size,minwidth=mid_cell_size,anchor=CENTER)

        self.tree.heading('#0',text='')
        self.tree.heading('EMPLOYEE ID',text='EMPLOYEE ID',anchor=CENTER)
        self.tree.heading('FIRST NAME',text='FIRST NAME',anchor=CENTER)
        self.tree.heading('LAST NAME',text='LAST NAME',anchor=CENTER)
        self.tree.heading('SEX',text='SEX',anchor=CENTER)
        self.tree.heading('SCHEDULE IN',text='SCHEDULE IN',anchor=CENTER)
        self.tree.heading('SCHEDULE OUT',text='SCHEDULE OUT',anchor=CENTER)

       
        #select all employees except for the admin
        self.c.execute("SELECT * FROM employees WHERE employee_id  != 'admin'")
        records = self.c.fetchall()        
        #insert data
        count=0
        for record in records:
            self.tree.insert(parent='',index='end',iid=count,text='',
            values=(record[0],record[2],record[3],record[4],record[5],record[6]))
            count+=1

        self.tree.pack()

        edit_btn = Button(show_record_page,text="EDIT",command=lambda: self.edit_record(show_record_page),bg='#AAFE92')
        edit_btn.place(x=935,y=525)
        delete_btn=Button(show_record_page,text="DELETE",command=lambda: self.delete_query(),bg='#FE9292')
        delete_btn.place(x=980,y=525)
        back_btn=Button(show_record_page, text='Go Back', bg='#ff79cd', width=10, command=lambda: [show_record_page.destroy(), root_page.deiconify()])
        back_btn.place(x=50,y=525)

        # check if user Exit the Window Manually
        show_record_page.protocol("WM_DELETE_WINDOW", lambda: [show_record_page.destroy(), root_page.deiconify()])

        show_record_page.mainloop()

    def current_time(self, time_label):
        date_time_now = datetime.now()
        date_time_now = date_time_now.strftime('%A %I:%M %p  %B %d, %Y')
        time_label.config(text=date_time_now)
        time_label.after(200, self.current_time, time_label)

    def attendance(self, root_page, date):
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
        Button(attendance_header, text='SET ATTENDANCE DATE', bg='#1eae98', command=lambda: [self.choose_date(attendance_page,root_page)]).grid(row=1, column=1)

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
            self.c.execute(f'''SELECT A.employee_id, first_name, last_name, attendance_date, time_in, status, time_out
                        FROM employee_attendance A, employees B
                        where A.employee_id = B.employee_id''')
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
        Button(attendance_page, text='Cancel', bg='#ff79cd', width=10, command=lambda: [attendance_page.destroy(), root_page.deiconify()]).pack()

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
        Button(date_frame, text='Confirm', bg='#3edbf0', command=lambda : [root.destroy(), self.attendance(root_root, f'{choice.get()}-{day.get()}-{year.get()}'), date_page.destroy()]).grid(row=2, column=2, pady=10)

        # Cancel Button
        Button(date_frame, text='Cancel', bg='#ff79cd', command=date_page.destroy).grid(row=2, column=1, pady=10)

        date_page.mainloop()

        
if __name__ == '__main__':
    main = Main()

