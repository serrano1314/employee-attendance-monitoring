# Imports
from sqlite3.dbapi2 import Row
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from datetime import datetime, date
import sqlite3

WINDOW_SIZE = '1000x580'
FONT = ('Verdana', 15)
BGCOLOR='#EFEFEF'
HEADER_COLOR='#7EE5FF'

class Main:
    def __init__(self, main_page):
        # Student info initialization
        self.student_id = 0
        self.first_name = ''
        self.middle_name = ''
        self.last_name = ''
        self.course = ''
        self.section = ''

        # Creating database& Table & connecting
        self.connection = sqlite3.connect('database.db')

        # Creating Cursor to the Database
        self.c = self.connection.cursor()
        try:
            # Creating Table
            self.c.execute("""CREATE TABLE students(
                    student_id text,
                    first_name text,
                    middle_name text,
                    last_name text,
                    course text,
                    section text
            )""")
            # Apply Changes to the Database
            self.connection.commit()

        except sqlite3.OperationalError:
            print('Table already made')
        # Frame
        main_frame = Frame(main_page, bg='#FAF1E6')
        main_frame.pack()

        # Application Logo
        self.app_logo = ImageTk.PhotoImage(Image.open('system daw eh.png').resize((150, 150), Image.ANTIALIAS))
        Label(main_frame, image=self.app_logo, bg='#FAF1E6').grid(row=0, column=1)

        # User name Entry
        Label(main_frame, text='Username', bg='#FAF1E6').grid(row=1, column=1, pady=(20, 10), padx=(50, 180))
        self.username = Entry(main_frame, width=30, bd=1,show='Hemlo')
        self.username.grid(row=2, column=1)

        # Password Entry
        Label(main_frame, text='Password', bg='#FAF1E6').grid(row=3, column=1,pady=(20, 10), padx=(50, 180))
        self.password = Entry(main_frame, width=30)
        self.password.grid(row=4, column=1)

        # Log in Button
        login_button = Button(main_frame, text='Login', width=10, bg='#E4EFE7', command=lambda: self.menu(main_page, main_frame))
        login_button.grid(row=5, column=1, pady=(20, 10))

        # Exit Button
        exit_button = Button(main_frame, text='Exit ', width=10,  bg='#E4EFE7', command=lambda: [main_page.destroy(), self.connection.close()])
        exit_button.grid(row=6, column=1, pady=(10, 20))

    def menu(self, main_page, main_frame):
        if self.username.get() == '' and self.password.get() == '':
            # Hide Main Window
            main_page.withdraw()
            self.username.delete(0, END)
            self.password.delete(0, END)

            # Create Menu Window
            menu_page = Toplevel()
            menu_page.title('Student Attendance Monitoring System')
            menu_page.config(bg='#FAF1E6')
            menu_page.geometry(WINDOW_SIZE)

            menu_frame = Frame(menu_page, bg='#FAF1E6')
            menu_frame.pack()
            # Current Time Label
            time_label = Label(menu_frame, bg='#FAF1E6',font=FONT)
            time_label.grid(row=0, column=3, padx=(0, 30), pady=20)
            self.current_time(time_label)

            button_h=4
            button_w=15

            # Logo
            Label(menu_frame, image=self.app_logo, bg='#FAF1E6').grid(row=1, column=3, pady=20, padx=20)

            # Add Button
            Button(menu_frame, text='Add Record', bg='#FFC9C9', font=FONT, width=button_w, height=button_h, command=lambda: [menu_page.withdraw(), self.add_record(menu_page)]).grid(row=1, column=1, pady=20, padx=20)

            # View Report Button
            Button(menu_frame, text='View Report', bg='#FFFB78', font=FONT, width=button_w, height=button_h).grid(row=1, column=2, pady=20, padx=20)

            # View Record Button
            Button(menu_frame, text='View Record', bg='#8BFFBD', font=FONT, width=button_w, height=button_h, command=lambda: [menu_page.withdraw(), self.show_records(menu_page)]).grid(row=2, column=1, pady=20, padx=20)

            # Attendance
            Button(menu_frame, text='Attendance', bg='#FF82E6', font=FONT, width=button_w, height=button_h, command=lambda: [self.attendance(menu_page), menu_page.withdraw()]).grid(row=2, column=2, pady=20, padx=20)

            # Cancel Button
            Button(menu_frame, text='Log Out', bg='#E4EFE7',command=lambda: [menu_page.destroy(), main_page.deiconify()]).grid(row=3, column=0, pady=20, padx=20)

            # check if the Exit th Window Manually
            menu_page.protocol("WM_DELETE_WINDOW", lambda: [menu_page.destroy(), main_page.deiconify()])

            menu_page.mainloop()
        else:
            error = Label(main_frame, text='Invalid Username or Password', fg='white', bg='#da7f8f', relief=RAISED)
            error.grid(row=7, column=1)
            error.after(3000, error.destroy)

    def add_record(self, menu_page):
        # Create Window
        add_record_page = Toplevel()
        add_record_page.title('Add Record')
        add_record_page.geometry(WINDOW_SIZE)
        add_record_page.config(bg='#FAF1E6')

        Label(add_record_page, height=3, width=400, bg=HEADER_COLOR, text='Add Record', font=FONT).pack(pady=(0, 10))

        add_record_frame = Frame(add_record_page, bg='#FAF1E6')
        add_record_frame.pack()
        # Getting the Student Id
        Label(add_record_frame, text='STUDENT ID:', bg='#FAF1E6').grid(row=0, column=1, pady=(10, 0), padx=(50, 220))
        self.student_id = Entry(add_record_frame, width=40)
        self.student_id.grid(row=1, column=1, pady=(10, 0))

        # Getting the First Name
        Label(add_record_frame, text='FIRST NAME: ', bg='#FAF1E6').grid(row=2, column=1, pady=(10, 0), padx=(50, 220))
        self.first_name = Entry(add_record_frame, width=40)
        self.first_name.grid(row=3, column=1, pady=(10, 0))

        # Getting the Middle Name
        Label(add_record_frame, text='MIDDLE NAME: ', bg='#FAF1E6').grid(row=4, column=1, pady=(10, 0), padx=(50, 210))
        self.middle_name = Entry(add_record_frame, width=40)
        self.middle_name.grid(row=5, column=1, pady=(10, 0))

        # Getting the Last Name
        Label(add_record_frame, text='LAST NAME: ', bg='#FAF1E6').grid(row=6, column=1, pady=(10, 0), padx=(50, 220))
        self.last_name = Entry(add_record_frame, width=40)
        self.last_name.grid(row=7, column=1, pady=(10, 0))

        # Getting the Course
        Label(add_record_frame, text='COURSE: ', bg='#FAF1E6').grid(row=8, column=1, pady=(10, 0), padx=(50, 230))
        self.course = Entry(add_record_frame, width=40)
        self.course.grid(row=9, column=1, pady=(10, 0))

        # Getting the Section
        Label(add_record_frame, text='SECTION: ', bg='#FAF1E6').grid(row=10, column=1, pady=(10, 0), padx=(50, 230))
        self.section = Entry(add_record_frame, width=40)
        self.section.grid(row=11, column=1, pady=(10, 0))

        # Cancel Button
        Button(add_record_frame, text='Cancel', width=10, bg='#E4EFE7', command=lambda: [add_record_page.destroy(), menu_page.deiconify()]).grid(row=13, column=1, pady=(10, 0))

        # Save Button
        Button(add_record_frame, text='Save', bg='#E4EFE7', width=10, command=lambda: [self.adding_record(add_record_page, menu_page)]).grid(row=12, column=1, pady=(10, 0))

        # check if user Exit the Window Manually
        add_record_page.protocol("WM_DELETE_WINDOW", lambda: [add_record_page.destroy(), menu_page.deiconify()])

        add_record_page.mainloop()

    def unique_id(self, id):
        self.c.execute(f'SELECT student_id FROM students WHERE student_id = "{id.get()}"')
        result = self.c.fetchall()
        if len(result) <= 0 and id.get() != '':
            return True
        self.connection.commit()

    def adding_record(self, adding_page, menu):
        # adding records to the database
        if self.unique_id(self.student_id):
            self.c.execute(f"""INSERT INTO students VALUES(
            '{self.student_id.get()}',
            '{self.first_name.get()}',
            '{self.middle_name.get()}',
            '{self.last_name.get()}',
            '{self.course.get()}',
            '{self.section.get()}',
            'N/A'
            )""")
            # Apply Changes to the Database
            self.connection.commit()
            adding_page.destroy()
            menu.deiconify()
        else:
            messagebox.showerror('Error', 'Student Id Already Exist or Invalid Input')

    def update_query(self,page,edit_page,update_id):

        response = messagebox.askyesno('UPDATE RECORD',f'ARE YOU SURE TO UPDATE RECORD FOR {update_id} ?')
        if(response):
            self.c.execute('''UPDATE students SET
                student_id = :student_id,
                first_name = :first_name,
                middle_name = :middle_name,
                last_name = :last_name,
                course = :course,
                section = :section

                WHERE student_id = :update_id''',
                {
                    'student_id':stud_id_edit.get(),
                    'first_name':first_name_edit.get(),
                    'middle_name':middle_name_edit.get(),
                    'last_name':last_name_edit.get(),
                    'course':course_edit.get(),
                    'section':section_edit.get(),
                    'update_id':update_id

                })
                
            self.connection.commit()
            print('success')
            page.destroy()
            edit_page.destroy()
            self.show_records()


    def edit_record(self,page,record_id):
        cell_size = 35
        table_col=3
        win_size='400x300'
        
        global stud_id_edit,first_name_edit,middle_name_edit,last_name_edit,course_edit,section_edit

        edit_record_page = Tk()
        edit_record_page.title('EDIT STUDENT RECORD')
        edit_record_page.geometry(win_size)
        edit_record_page.config(bg=BGCOLOR)
        Label(edit_record_page,text="STUDENT ID:").grid(row=2,column=table_col-1,padx=10,pady=(40,0 ))
        stud_id_edit=Entry(edit_record_page,width=cell_size)
        stud_id_edit.grid(row=2,column=table_col,pady=(40,0 ))

        Label(edit_record_page,text="FIRST NAME:").grid(row=3,column=table_col-1)
        first_name_edit=Entry(edit_record_page,width=cell_size)
        first_name_edit.grid(row=3,column=table_col)
        
        Label(edit_record_page,text="MIDDLE NAME:").grid(row=4,column=table_col-1)
        middle_name_edit=Entry(edit_record_page,width=cell_size)
        middle_name_edit.grid(row=4,column=table_col)

        Label(edit_record_page,text="LAST NAME:").grid(row=5,column=table_col-1)
        last_name_edit=Entry(edit_record_page,width=cell_size)
        last_name_edit.grid(row=5,column=table_col)

        Label(edit_record_page,text="COURSE:").grid(row=6,column=table_col-1)
        course_edit=Entry(edit_record_page,width=cell_size)
        course_edit.grid(row=6,column=table_col)

        Label(edit_record_page,text="SECTION:").grid(row=7,column=table_col-1)
        section_edit=Entry(edit_record_page,width=cell_size)
        section_edit.grid(row=7,column=table_col)

        self.c.execute(f"SELECT * FROM students WHERE student_id = '{record_id}'")
        records=self.c.fetchall()
        
        for record in records:
            stud_id_edit.insert(0,record[0])
            first_name_edit.insert(0,record[1])
            middle_name_edit.insert(0,record[2])
            last_name_edit.insert(0,record[3])
            course_edit.insert(0,record[4])
            section_edit.insert(0,record[5])

        
        Button(edit_record_page,text="SAVE",width=15,command=lambda id=record_id:self.update_query(page,edit_record_page,id),bg='#AAFE92').grid(row=8,column=table_col,pady=20)
        Button(edit_record_page,text="CANCEL",width=15,command=lambda:edit_record_page.destroy(),bg='#FE9292').grid(row=8,column=table_col-1,pady=20,padx=(35,0))
        edit_record_page.mainloop()

    def delete_query(self,page,record_id):
        response = messagebox.askyesno('DELETE RECORD',f'ARE YOU SURE TO DELETE RECORD FOR {record_id} ?')
        if(response):
            self.c.execute(f"DELETE FROM students WHERE student_id = '{record_id}'")
            self.connection.commit()         
            page.destroy()
            self.show_records()

    def show_records(self, root_page):
        cell_size = 22
        th_font ='Arial 12 bold'
        win_size='1100x600'
        table_bg_color = '#ffffff'
        show_record_page = Toplevel()
        show_record_page.title('SHOW RECORDS')
        show_record_page.geometry(win_size)
        show_record_page.config(bg=BGCOLOR)
        
        self.c.execute("SELECT * FROM students")
        records = self.c.fetchall()

        Label(show_record_page,bg=HEADER_COLOR,padx=500,pady=25,text="SHOW RECORDS").grid(row=4,column=5,columnspan=8)
        table_row=5
        
        Label(show_record_page,bg=BGCOLOR,text="STUDENT ID",font=th_font,pady=10).grid(row=table_row,column=5)
        Label(show_record_page,bg=BGCOLOR,text="FIRST NAME ",font=th_font,pady=10).grid(row=table_row,column=6)
        Label(show_record_page,bg=BGCOLOR,text="MIDDLE NAME ",font=th_font,pady=10).grid(row=table_row,column=7)
        Label(show_record_page,bg=BGCOLOR,text="LAST NAME ",font=th_font,pady=10).grid(row=table_row,column=8)
        Label(show_record_page,bg=BGCOLOR,text="COURSE",font=th_font,pady=10).grid(row=table_row,column=9)
        Label(show_record_page,bg=BGCOLOR,text="SECTION",font=th_font,pady=10).grid(row=table_row,column=10)
        
        for record in records:
            stud_id=Label(show_record_page,text=record[0],width=cell_size,bg=table_bg_color,padx=0)
            stud_id.grid(row=table_row+1,column=5)

            first_name=Label(show_record_page,text=record[1],width=cell_size,bg=table_bg_color)
            first_name.grid(row=table_row+1,column=6)

            middle_name=Label(show_record_page,text=record[2],width=cell_size,bg=table_bg_color)
            middle_name.grid(row=table_row+1,column=7)

            last_name=Label(show_record_page,text=record[3],width=cell_size,bg=table_bg_color)
            last_name.grid(row=table_row+1,column=8)

            course=Label(show_record_page,text=record[4],width=cell_size,bg=table_bg_color)
            course.grid(row=table_row+1,column=9)

            section=Label(show_record_page,text=record[5],width=cell_size,bg=table_bg_color)
            section.grid(row=table_row+1,column=10)

            Button(show_record_page,text="EDIT",command=lambda edit_id=record[0]: self.edit_record(show_record_page,edit_id),bg='#AAFE92').grid(row=table_row+1,column=11)
            Button(show_record_page,text="DELETE",command=lambda del_id=record[0]: self.delete_query(show_record_page,del_id),bg='#FE9292').grid(row=table_row+1,column=12)

            table_row+=1

        self.connection.commit()

        Button(show_record_page, text='Cancel', width=10, command=lambda: [show_record_page.destroy(), root_page.deiconify()]).grid(row=table_row+1, column=5, pady=20)

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
        Label(attendance_header, bg='#FAF1E6', text="STUDENT ID", font=th_font, pady=10, padx=40).grid(row=2, column=1)
        Label(attendance_header, bg='#FAF1E6', text="FIRST NAME", font=th_font, pady=10, padx=40).grid(row=2, column=2)
        Label(attendance_header, bg='#FAF1E6', text="LAST NAME", font=th_font, pady=10, padx=40).grid(row=2, column=3)
        Label(attendance_header, bg='#FAF1E6', text="STATUS", font=th_font, pady=10, padx=40).grid(row=2, column=4)

        # Query for getting the data with status
        self.c.execute('SELECT student_id, first_name, last_name, student_status FROM students')
        data_row = 3
        status_label_list = []
        result = self.c.fetchall()
        for item in result:
            Label(attendance_header, text=item[0], pady=1, padx=40, width=10, bg='white').grid(row=data_row, column=1)
            Label(attendance_header, text=item[1], padx=40, bg='white', width=10).grid(row=data_row, column=2)
            Label(attendance_header, text=item[2], padx=40, bg='white', width=10).grid(row=data_row, column=3)
            ito = Label(attendance_header, text=item[3], padx=40, bg='white', width=10)
            ito.grid(row=data_row, column=4)
            status_label_list.append(ito)

            Button(attendance_header, text='Present', bg='#4aa96c', command= lambda id=item[0]: self.attendance_accept(id, 'Present', status_label_list)).grid(row=data_row, column=5)
            Button(attendance_header, text='Absent', bg='#fb3640', command= lambda id=item[0]: self.attendance_accept(id, 'Absent', status_label_list)).grid(row=data_row, column=6)
            Button(attendance_header, text='Late', bg='#fea82f', command= lambda id=item[0]: self.attendance_accept(id, 'Late', status_label_list)).grid(row=data_row, column=7)
            data_row += 1

        self.connection.commit()

        # Save Button
        Button(attendance_header, text='Save', bg='#3edbf0', width=10, command=lambda: [self.attendance_save(status_label_list), attendance_page.destroy(), root_page.deiconify()]).grid(row=data_row + 1, column=4, pady=10)

        # Cancel Button
        Button(attendance_header, text='Cancel', bg='#ff79cd', width=10, command=lambda: [attendance_page.destroy(), root_page.deiconify()]).grid(row= data_row+1, column=3, pady=10)

        # Check if the User Manually Exit Window
        attendance_page.protocol("WM_DELETE_WINDOW", lambda: root_page.deiconify())

    def attendance_save(self, list_status):
        # Get all the student id
        self.c.execute("SELECT student_id FROM students;")
        result = self.c.fetchall()
        index = 0
        for n in result:
            # Assign the Status of the students
            self.c.execute(f"UPDATE students SET student_status = '{list_status[index].cget('text')}' WHERE student_id = '{n[0]}'")
            index += 1
        self.connection.commit()
        messagebox.showinfo('Attendance Saved', 'Successfully Saved')

    def attendance_accept(self, id, status, list_status):
        index = 0
        # Will change the status of the students in the table
        self.c.execute(f'SELECT * FROM students')
        result = self.c.fetchall()
        for i in result:
            if id == i[0]:
                break
            index += 1
        list_status[index].config(text=status)
        self.connection.commit()

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

        
root = Tk()
root.title('Student Attendance Monitoring System')
root.geometry(WINDOW_SIZE)
root.config(bg='#FAF1E6')
main = Main(root)
root.mainloop()
