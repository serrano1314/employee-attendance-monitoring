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
BGCOLOR='#EFEFEF'
HEADER_COLOR='#7EE5FF'

class Main:
    def __init__(self):
        # Root window creation
        root = Tk()
        root.title('Student Attendance Monitoring System')
        root.geometry(WINDOW_SIZE)
        root.config(bg='#FAF1E6')

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
        login_img = PhotoImage(file='bts_biot/login_btn.png')
        exit_img = PhotoImage(file='bts_biot/exit_btn.png')

        main_frame = Frame(root, bg='#FAF1E6')
        main_frame.pack()

        # Application Logo
        Label(main_frame, image=self.app_logo, bg='#FAF1E6').grid(row=0, column=1)

        # User name Entry
        Label(main_frame, text='Username/ID', bg='#FAF1E6').grid(row=1, column=1, pady=(20, 10), padx=(50, 180))
        username = Entry(main_frame, width=30, bd=1)
        username.grid(row=2, column=1)

        # Password Entry
        Label(main_frame, text='Password', bg='#FAF1E6').grid(row=3, column=1,pady=(20, 10), padx=(50, 180))
        password = Entry(main_frame, width=30, show="*")
        password.grid(row=4, column=1)

        # Log in Button
        login_button = Button(main_frame, image=login_img, border=0, bg='#FAF1E6', command=lambda: [self.menu(root)])
        login_button.grid(row=5, column=1, pady=(20, 10))

        # Exit Button
        exit_button = Button(main_frame, image=exit_img, border=0,  bg='#FAF1E6', command=lambda: [root.destroy(), self.connection.close()])
        exit_button.grid(row=6, column=1, pady=(10, 20))
        root.mainloop()

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
                menu_page.config(bg='#FAF1E6')
                menu_page.geometry(WINDOW_SIZE)

                # CREATING FRAME TO CENTER WIDGETS
                menu_frame = Frame(menu_page, bg='#FAF1E6')
                menu_frame.pack()

                # Current Time Label
                time_label = Label(menu_frame, bg='#FAF1E6',font=FONT)
                time_label.grid(row=0, column=3, padx=(0, 30), pady=20)
                self.current_time(time_label)

                button_h=4
                button_w=15

                # Logo
                Label(menu_frame, image=self.app_logo, bg='#FAF1E6').grid(row=1, column=3, rowspan=2, pady=20, padx=20)

                # Add Button
                Button(menu_frame, text='Add Record', bg='#FFC9C9', font=FONT, width=button_w, height=button_h, command=lambda: [menu_page.withdraw(), self.add_record(menu_page)]).grid(row=1, column=1, pady=20, padx=20)

                # View Report Button
                Button(menu_frame, text='View Report', bg='#FFFB78', font=FONT, width=button_w, height=button_h).grid(row=1, column=2, pady=20, padx=20)

                # View Record Button
                Button(menu_frame, text='View Record', bg='#8BFFBD', font=FONT, width=button_w, height=button_h, command=lambda: [menu_page.withdraw(), self.show_records(menu_page)]).grid(row=2, column=1, pady=20, padx=20)

                # Attendance
                Button(menu_frame, text='Attendance', bg='#FF82E6', font=FONT, width=button_w, height=button_h, command=lambda: [self.attendance(menu_page), menu_page.withdraw()]).grid(row=2, column=2, pady=20, padx=20)

                # Cancel Button
                Button(menu_frame, text='Log Out', bg='#E4EFE7',command=lambda: [menu_page.destroy(), root.deiconify()]).grid(row=3, column=0, pady=20, padx=20)

                # check if the Exit th Window Manually
                menu_page.protocol("WM_DELETE_WINDOW", lambda: [menu_page.destroy(), self.starting()])

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
        date_time_now = datetime.now()
        date_now = date_time_now.strftime('%b-%d-%Y')
        time_now = date_time_now.strftime('%I:%M %p')
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
            '{attendance_status}'
            )""")
        self.connection.commit()
        messagebox.showinfo('INFORMATION', f'You are {attendance_status} for today.')


    def employee_page(self, root, id):
        # Fetch employee profile
        self.c.execute(f"SELECT * FROM employees WHERE employee_id = '{id}'")
        content = self.c.fetchone()

        # Create Employee  Window
        employee_menu_page = Toplevel()
        employee_menu_page.title('Student Attendance Monitoring System')
        employee_menu_page.config(bg='#FAF1E6')
        employee_menu_page.geometry('500x400')

        button_h = 4
        button_w = 15

        Label(employee_menu_page, height=3, width=400, bg=HEADER_COLOR, text='EMPLOYEE', font=FONT).pack(pady=(0, 10))

        employee_menu_frame = Frame(employee_menu_page, bg='#FAF1E6')
        employee_menu_frame.pack()

        # Header
        Label(employee_menu_frame, text='WELCOME,', bg='#FAF1E6', font=FONT).grid(sticky='W', row=0, column=0,
                                                                                  columnspan=2)
        Label(employee_menu_frame, text=content[2], bg='#FAF1E6', font=FONT).grid(sticky='W', row=1, column=0, padx=5)
        Label(employee_menu_frame, text=content[3], bg='#FAF1E6', font=FONT).grid(sticky='W', row=1, column=1, padx=5,
                                                                                  columnspan=2)
        Label(employee_menu_frame, text=f'YOUR SCHEDULE: {content[5]} to {content[6]}', bg='#FAF1E6',).grid(sticky='W', row=1, column=2, padx=5,
                                                                                  columnspan=2)

        # time and date today
        emp = Label(employee_menu_frame, bg='#FAF1E6', font=('Verdana', 10), width=40)
        emp.grid(row=2, column=1, columnspan=2)
        self.current_time(emp)

        # time in button
        Button(employee_menu_frame, text='TIME IN', width=button_w, height=button_h, bg='#a5e1ad',
               font=('Verdana', 10),command=lambda: self.time_in_query(id)).grid(sticky='W', row=3, column=1, pady=10, padx=20)

        # time out button
        Button(employee_menu_frame, text='TIME OUT', width=button_w, height=button_h, bg='#f29191',
               font=('Verdana', 10)).grid(sticky='W', row=4, column=1, pady=10, rowspan=2, padx=20)

        # View Records Button
        Button(employee_menu_frame, text='VIEW RECORDS', bg='#c0fefc', width=20).grid(sticky='S', row=3, column=2,
                                                                                      pady=10, padx=20)

        # Edit Profile Button
        Button(employee_menu_frame, text='EDIT PROFILE', bg='#c0fefc', width=20,
               command=lambda: [employee_menu_page.destroy(), self.edit_profile(content[0], root)]).grid(sticky='N', row=4, column=2,
                                                                                         pady=10, padx=20)

        # Edit Password Button
        Button(employee_menu_frame, text='CHANGE PASSWORD', bg='#c0fefc', width=20, command=lambda: self.edit_password(id)).grid(sticky='N', row=5, column=2,
                                                                                         pady=10, padx=20)
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
            self.c.execute(f"UPDATE employees SET password = {new.get()} WHERE employee_id = {id}")
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

        Button(edit, text='SAVE',bg='#AAFE92', command=lambda :[self.edit_profile_query((new_fname.get(), new_lname.get(), new_sex.get(), id)), edit_profile.destroy(), self.employee_page(root, id)]).grid(row=3, column=1)

        Button(edit, text='CANCEL',bg='#FE9292', command=lambda :[edit_profile.destroy(), self.employee_page(root, id)]).grid(row=3, column=2)

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
        add_record_page.geometry(WINDOW_SIZE)
        add_record_page.config(bg='#FAF1E6')
        morning = StringVar()
        night = StringVar()
        Label(add_record_page, height=3, width=400, bg=HEADER_COLOR, text='Add Record', font=FONT).pack(pady=(0, 10))

        add_record_frame = Frame(add_record_page, bg='#FAF1E6')
        add_record_frame.pack()

        # Getting the Employee Id
        Label(add_record_frame, text='EMPLOYEE ID:', bg='#FAF1E6').grid(sticky='W', row=0, column=1, pady=(10, 0), padx=10)
        self.employee_id = Entry(add_record_frame, width=40)
        self.employee_id.grid(row=0, column=2, pady=(10, 0), columnspan=2)

        # Getting the password
        Label(add_record_frame, text='PASSWORD: ', bg='#FAF1E6').grid(sticky='W',row=1, column=1, pady=(10, 0), padx=10)
        self.password = Entry(add_record_frame, width=40)
        self.password.grid(row=1, column=2, pady=(10, 0), columnspan=2)

        # Getting the First Name
        Label(add_record_frame, text='FIRST NAME: ', bg='#FAF1E6').grid(sticky='W',row=2, column=1, pady=(10, 0), padx=10)
        self.first_name = Entry(add_record_frame, width=40)
        self.first_name.grid(row=2, column=2, pady=(10, 0), columnspan=2)

        # Getting the Last Name
        Label(add_record_frame, text='LAST NAME: ', bg='#FAF1E6').grid(sticky='W',row=3, column=1, pady=(10, 0), padx=10)
        self.last_name = Entry(add_record_frame, width=40)
        self.last_name.grid(row=3, column=2, pady=(10, 0), columnspan=2)

        # Sex
        Label(add_record_frame, text='SEX: ', bg='#FAF1E6').grid(sticky='W',row=4, column=1, pady=(10, 0), padx=10)
        self.sex.set('MALE')
        option = OptionMenu(add_record_frame, self.sex, 'MALE', 'FEMALE')
        option.grid(sticky='W',row=4, column=2, pady=(10, 0), columnspan=2)

        # Schedule
        Label(add_record_frame, text='SCHEDULE', bg='#FAF1E6', width=10).grid(row=5, column=2, pady=20, columnspan=2)

        # IN
        Label(add_record_frame, text='IN:', bg='#FAF1E6').grid(sticky='W', row=6, column=1)
        self.schedule_in = Entry(add_record_frame, width=10)
        self.schedule_in.grid(row=6, column=2, sticky='W')
        morning.set('AM')
        option_morning = OptionMenu(add_record_frame, morning, 'AM', 'PM')
        option_morning.grid(sticky='W', row=6, column=3, pady=(10, 0))


        # Out
        Label(add_record_frame, text='OUT:', bg='#FAF1E6').grid(sticky='W', row=7, column=1)
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

            selected = self.tree.focus()
            self.tree.item(selected,text='',values=(employee_id_edit.get(),first_name_edit.get(),
                                                    last_name_edit.get(),sex_edit.get(),
                                                    schedule_in_edit.get(),schedule_out_edit.get()))

            self.connection.commit()
            print('success')
            edit_page.destroy()


    def edit_record(self,page):
        cell_size = 35
        table_col=3
        win_size='400x300'
        
        global employee_id_edit,password_edit,first_name_edit,last_name_edit,sex_edit,schedule_in_edit,schedule_out_edit

        edit_record_page = Tk()
        edit_record_page.title('EDIT EMPLOYEE RECORD')
        edit_record_page.geometry(win_size)
        edit_record_page.config(bg=BGCOLOR)

        Label(edit_record_page,text="EMPLOYEE ID:").grid(row=2,column=table_col-1,padx=10,pady=(40,0 ))
        employee_id_edit=Entry(edit_record_page, width=cell_size)
        employee_id_edit.grid(row=2, column=table_col, pady=(40, 0))

        Label(edit_record_page,text="PASSWORD:").grid(row=3,column=table_col-1)
        password_edit=Entry(edit_record_page, width=cell_size)
        password_edit.grid(row=3, column=table_col)
        
        Label(edit_record_page,text="FIRST NAME:").grid(row=4,column=table_col-1)
        first_name_edit=Entry(edit_record_page, width=cell_size)
        first_name_edit.grid(row=4, column=table_col)

        Label(edit_record_page,text="LAST NAME:").grid(row=5,column=table_col-1)
        last_name_edit=Entry(edit_record_page,width=cell_size)
        last_name_edit.grid(row=5,column=table_col)

        Label(edit_record_page,text="SEX:").grid(row=6,column=table_col-1)
        sex_edit=Entry(edit_record_page, width=cell_size)
        sex_edit.grid(row=6, column=table_col)

        Label(edit_record_page,text="SCHEDULE IN:").grid(row=7,column=table_col-1)
        schedule_in_edit=Entry(edit_record_page, width=cell_size)
        schedule_in_edit.grid(row=7, column=table_col)

        Label(edit_record_page, text="SCHEDULE OUT:").grid(row=8, column=table_col - 1)
        schedule_out_edit = Entry(edit_record_page, width=cell_size)
        schedule_out_edit.grid(row=8, column=table_col)

        record_tree = self.tree.selection()[0]
        record = self.tree.item(record_tree)
        id = record['values'][0]

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

    def delete_query(self,page, root):

        record_tree = self.tree.selection()[0]
        record = self.tree.item(record_tree)
        id = record['values'][0]
        response = messagebox.askyesno('DELETE RECORD',f'Delete Record for [{id}] ?')
        if(response):
            print()
            self.tree.delete(record_tree)
            self.c.execute(f"DELETE FROM employees WHERE employee_id = '{id}'")
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
        show_record_frame=Frame(show_record_page)
        show_record_frame.pack()
        Label(show_record_frame, height=3, width=600, bg=HEADER_COLOR, text='EMPLOYEE RECORDS', font=FONT).pack(pady=(0, 10))
        #for table's scrollbar
        scrollbary = Scrollbar(show_record_frame, orient=VERTICAL)

        self.tree = ttk.Treeview(show_record_frame,selectmode=BROWSE,yscrollcommand=scrollbary.set,height=20)
        scrollbary.config(command=self.tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        self.tree['columns'] = ('EMPLOYEE ID', 'FIRST NAME', 'LAST NAME', 'SEX', 'SCHEDULE IN','SCHEDULE OUT')
        self.tree.column('#0',width=0,stretch=NO)
        self.tree.column('EMPLOYEE ID',width=cell_size,minwidth=mid_cell_size,anchor=W)
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
        delete_btn=Button(show_record_page,text="DELETE",command=lambda: self.delete_query(show_record_page, root_page),bg='#FE9292')
        delete_btn.place(x=980,y=525)
        back_btn=Button(show_record_page, text='Go Back', width=10, command=lambda: [show_record_page.destroy(), root_page.deiconify()])
        back_btn.place(x=50,y=525)

        # check if user Exit the Window Manually
        show_record_page.protocol("WM_DELETE_WINDOW", lambda: [show_record_page.destroy(), root_page.deiconify()])

        show_record_page.mainloop()

    def current_time(self, time_label):
        date_time_now = datetime.now()
        date_time_now = date_time_now.strftime('%A %I:%M %p  %B %d, %Y')
        time_label.config(text=date_time_now)
        time_label.after(200, self.current_time, time_label)

    def attendance(self, root_page):
        # Making attendance window
        attendance_page = Toplevel()
        attendance_page.title('Attendance')
        attendance_page.geometry('1100x600')
        attendance_page.config(bg='#FAF1E6')
        th_font = 'Arial 12 bold'

        # Attendance Header
        Label(attendance_page, width=400, height=3, text='ATTENDANCE', bg=HEADER_COLOR, font=FONT).pack()

        # Attendance Frame
        attendance_header = Frame(attendance_page, bg='#FAF1E6')
        attendance_header.pack()

        # Date now
        Label(attendance_header, text='Attendance Date for:', bg='#FAF1E6').grid(row=1, column=3, padx=(30, 0))

        # Date and time now
        current_date = Label(attendance_header, bg='#FAF1E6')
        current_date.grid(row=1, column=4, padx=(0, 70))

        # Picked attendance date
        Button(attendance_header, text='SET ATTENDANCE DATE', bg='#1eae98', command=lambda: self.choose_date(current_date)).grid(row=1, column=1)

        # day and time today
        dates = Label(attendance_header, bg='#FAF1E6', font=FONT)
        dates.grid(row=0, column=5, pady=10, columnspan=3)
        self.current_time(dates)

        # Field data
        Label(attendance_header, bg='#FAF1E6', text="EMPLOYEE ID ID", font=th_font, pady=10, padx=40).grid(row=2, column=1)
        Label(attendance_header, bg='#FAF1E6', text="FIRST NAME", font=th_font, pady=10, padx=40).grid(row=2, column=2)
        Label(attendance_header, bg='#FAF1E6', text="LAST NAME", font=th_font, pady=10, padx=40).grid(row=2, column=3)
        Label(attendance_header, bg='#FAF1E6', text="STATUS", font=th_font, pady=10, padx=40).grid(row=2, column=4)

        # Query for getting the data with status
        self.c.execute('SELECT employee_id, first_name, last_name FROM employees')
        data_row = 3
        status_label_list = []
        result = self.c.fetchall()
        for item in result:
            Label(attendance_header, text=item[0], pady=1, padx=40, width=10, bg='white').grid(row=data_row, column=1)
            Label(attendance_header, text=item[1], padx=40, bg='white', width=10).grid(row=data_row, column=2)
            Label(attendance_header, text=item[2], padx=40, bg='white', width=10).grid(row=data_row, column=3)


            Button(attendance_header, text='Present', bg='#4aa96c').grid(row=data_row, column=5)
            Button(attendance_header, text='Absent', bg='#fb3640').grid(row=data_row, column=6)
            Button(attendance_header, text='Late', bg='#fea82f').grid(row=data_row, column=7)
            data_row += 1

        self.connection.commit()

        # Save Button
        Button(attendance_header, text='Save', bg='#3edbf0', width=10, command=lambda: [attendance_page.destroy(), root_page.deiconify()]).grid(row=data_row + 1, column=4, pady=10)

        # Cancel Button
        Button(attendance_header, text='Cancel', bg='#ff79cd', width=10, command=lambda: [attendance_page.destroy(), root_page.deiconify()]).grid(row= data_row+1, column=3, pady=10)

        # Check if the User Manually Exit Window
        attendance_page.protocol("WM_DELETE_WINDOW", lambda: root_page.deiconify())

    # def attendance_save(self, list_status):
    #     # Get all the student id
    #     self.c.execute("SELECT student_id FROM students;")
    #     result = self.c.fetchall()
    #     index = 0
    #     for n in result:
    #         # Assign the Status of the students
    #         self.c.execute(f"UPDATE students SET student_status = '{list_status[index].cget('text')}' WHERE student_id = '{n[0]}'")
    #         index += 1
    #     self.connection.commit()
    #     messagebox.showinfo('Attendance Saved', 'Successfully Saved')

    # def attendance_accept(self, id, status, list_status):
    #     index = 0
    #     # Will change the status of the students in the table
    #     self.c.execute(f'SELECT * FROM students')
    #     result = self.c.fetchall()
    #     for i in result:
    #         if id == i[0]:
    #             break
    #         index += 1
    #     list_status[index].config(text=status)
    #     self.connection.commit()

    def choose_date(self, today_date):
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
        choice.set(current_month.upper())
        option = OptionMenu(date_frame, choice, "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
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
        Button(date_frame, text='Confirm', bg='#3edbf0', command=lambda: [today_date.config(text=f'{choice.get()} {day.get()}, {year.get()}'), date_page.destroy()]).grid(row=2, column=2, pady=10)

        # Cancel Button
        Button(date_frame, text='Cancel', bg='#ff79cd', command=date_page.destroy).grid(row=2, column=1, pady=10)

        date_page.mainloop()

        

main = Main()

