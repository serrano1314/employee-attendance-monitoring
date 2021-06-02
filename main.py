# Imports
from admin.show_record import *
from admin.attendance_record import *
from admin.add_record import *

from sqlite3.dbapi2 import Row
from tkinter import *
from tkinter import messagebox, ttk
from PIL import ImageTk, Image
from datetime import datetime, date
import sqlite3
import re

from config_var import *

class Main:
    def __init__(self):
        # Root window creation
        root = Tk()
        root.title('Employee Attendance Monitoring System')
        root.geometry(WINDOW_SIZE)
        root.config(bg=BGCOLOR)
        root.resizable(False, False)

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
        self.app_logo = ImageTk.PhotoImage(Image.open('logo.png').resize((180, 180), Image.ANTIALIAS))

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
        password.pack(pady=(0,30))

        # Log in Button
        login_button = Button(root, image=login_img, border=0,bg='#FFFFFF', command=lambda: [self.menu(root)])
        login_button.pack(pady=5)

        # Exit Button
        exit_button = Button(root, image=exit_img, border=0,bg='#FFFFFF', command=lambda: [root.destroy(), self.connection.close()])
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
        e.widget['background'] = '#e1e5ea'

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
                menu_page.title('Employee Attendance Monitoring System')
                menu_page.config(bg=BGCOLOR)
                menu_page.geometry(WINDOW_SIZE)

                # CREATING FRAME TO CENTER WIDGETS
                menu_frame = Frame(menu_page, bg=BGCOLOR)
                menu_frame.pack()

                # Current Time Label
                time_label = Label(menu_frame, bg=BGCOLOR,font=FONT)
                time_label.grid(row=0, column=1, columnspan=3, pady=20)
                self.current_time(time_label)

                button_h=110
                button_w=250

                # Logo
                Label(menu_frame, image=self.app_logo, bg=BGCOLOR).grid(row=1, column=3, rowspan=2 ,padx=(50,0),pady=(50,0))

                # Add Button
                add_record_img = ImageTk.PhotoImage(Image.open("btn/add_record_btn.png").resize((button_w, button_h), Image.ANTIALIAS))
                add_button = Button(menu_frame, image=add_record_img, bg=BGCOLOR, border=0,command=lambda: [menu_page.withdraw(), add_record(self,menu_page)])
                add_button.grid(row=1, column=1, pady=(50,2))

                # View Report Button
                view_report_img = ImageTk.PhotoImage(Image.open('btn/view_report_btn.png').resize((button_w, button_h), Image.ANTIALIAS))
                view_report_button = Button(menu_frame, image=view_report_img, bg=BGCOLOR, border=0)
                view_report_button.grid(row=1, column=2, pady=(50,2))

                # View Record Button
                view_record_img = ImageTk.PhotoImage(Image.open('btn/view_record_btn.png').resize((button_w, button_h), Image.ANTIALIAS))
                view_button = Button(menu_frame, image=view_record_img, bg=BGCOLOR, border=0,command=lambda: [menu_page.withdraw(), show_records(self,menu_page)], relief=RAISED)
                view_button.grid(row=2, column=1, pady=2)

                # Attendance
                attendance_img = ImageTk.PhotoImage(Image.open('btn/attendance_btn.png').resize((button_w, button_h), Image.ANTIALIAS))
                attendance_button = Button(menu_frame, image=attendance_img, bg=BGCOLOR, border=0, command=lambda: [attendance_record(self,menu_page, ""), menu_page.withdraw()])
                attendance_button.grid(row=2, column=2, pady=2)

                # logout Button
                Button(menu_frame, text='Log Out', bg='#e4bad4',command=lambda: [menu_page.destroy(), root.deiconify()]).grid(row=2, column=3, padx=(50,0))

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
        employee_records_page.config(bg=BGCOLOR)

        Label(employee_records_page, width=400, height=2, bg=HEADER_COLOR, text='EMPLOYEE RECORDS').pack()
        employee_records_frame = Frame(employee_records_page,bg=BGCOLOR)
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
        employee_menu_page.title('Employee Attendance Monitoring System')
        employee_menu_page.config(bg=BGCOLOR)
        employee_menu_page.geometry('500x400')
        employee_menu_page.resizable(False,False)

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
                                                                            
        Button(employee_menu_frame, text='Log Out', bg='#e4bad4',command=lambda: [employee_menu_page.destroy(), root.deiconify()]).grid(row=6, column=2)
        # check if the Exit th Window Manually
        employee_menu_page.protocol("WM_DELETE_WINDOW", lambda: [employee_menu_page.destroy(), root.deiconify()])

        employee_menu_page.mainloop()

    def edit_password(self, id):
        # Edit password window
        edit_pass = Toplevel()
        edit_pass.geometry('400x300')
        edit_pass.resizable(False, False)
        edit_pass.title('EDIT PASSWORD')
        edit_pass.config(bg=BGCOLOR)

        # Label header
        Label(edit_pass, height=3, width=400, bg=HEADER_COLOR, text='EDIT PASSWORD', font=FONT).pack(pady=(0, 10))
        edit_pass_frame = Frame(edit_pass,bg=BGCOLOR)
        edit_pass_frame.pack(fill=BOTH)

        Label(edit_pass_frame, text='CURRENT PASSWORD:',bg=BGCOLOR).grid(sticky='W', row=0, column=0, padx=10, pady=10)
        current_password = Entry(edit_pass_frame, show='*')
        current_password.grid(row=0, column=1, columnspan=2)

        Label(edit_pass_frame, text='NEW PASSWORD:',bg=BGCOLOR).grid(sticky='W',row=1, column=0, padx=10, pady=10)
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
        edit_profile.config(bg=BGCOLOR)

        Label(edit_profile, height=3, width=400, bg=HEADER_COLOR, text='EDIT PROFILE', font=FONT).pack(pady=(0, 10))

        new_sex = StringVar()
        edit = Frame(edit_profile,bg=BGCOLOR)
        edit.pack()

        Label(edit, text='FIRST NAME: ',bg=BGCOLOR).grid(row=0, column=0, pady=10)
        new_fname = Entry(edit, width=20)
        new_fname.grid(row=0, column=1)
        new_fname.insert(0, result[0])

        Label(edit, text='LAST NAME: ',bg=BGCOLOR).grid(row=1, column=0, pady=10)
        new_lname = Entry(edit, width=20)
        new_lname.grid(row=1, column=1)
        new_lname.insert(0, result[1])

        Label(edit, text='SEX: ',bg=BGCOLOR).grid(row=2, column=0, pady=10)
        new_sex.set(result[2])
        option = OptionMenu(edit, new_sex, 'MALE', 'FEMALE')
        option.grid(sticky='W', row=2, column=1)

        Button(edit, text='SAVE',bg='#AAFE92', command=lambda :[self.edit_profile_query((new_fname.get(), new_lname.get(), new_sex.get(), id)), edit_profile.destroy(), self.employee_page(root, id)]).grid(row=3, column=2)

        Button(edit, text='CANCEL',bg='#e4bad4', command=lambda :[edit_profile.destroy(), self.employee_page(root, id)]).grid(row=3, column=1)

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


    def current_time(self, time_label):
        date_time_now = datetime.now()
        date_time_now = date_time_now.strftime('%A %I:%M %p  %B %d, %Y')
        time_label.config(text=date_time_now)
        time_label.after(200, self.current_time, time_label)

        
if __name__ == '__main__':
    main = Main()

