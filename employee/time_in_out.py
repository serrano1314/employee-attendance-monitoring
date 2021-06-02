from datetime import datetime
from tkinter import *
from tkinter import messagebox

def time_in_query(self, id):
    date_time_now = datetime.now()
    date_now = date_time_now.strftime('%b-%d-%Y')
    time_now = date_time_now.time()

    # check if the user already time in today
    self.c.execute(f"SELECT time_in FROM employee_attendance WHERE employee_id = ? AND attendance_date = ?",
                   (id, date_now))
    result = self.c.fetchall()
    self.connection.commit()
    if len(result) <= 0:
        self.c.execute(f"SELECT schedule_in, schedule_out FROM employees WHERE employee_id = '{id}'")
        status = {
            'present': 'PRESENT',
            'late': 'LATE',
            'absent': 'ABSENT'
        }
        attendance_status = ''
        result = self.c.fetchone()
        sched_in = datetime.strptime(result[0],'%I:%M %p').time()
        sched_out = datetime.strptime(result[1],'%I:%M %p').time()

        time_in = time_now

        if time_in <= sched_in:
            attendance_status = status['present']
        if time_in > sched_in:
            attendance_status = status['late']
        if time_in > sched_out:
            attendance_status = status['absent']

        time_in_str = time_in.strftime('%I:%M %p')

        self.c.execute(f"""INSERT INTO employee_attendance VALUES(
               '{id}',
               '{date_now}',
               '{time_in_str}',
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
        self.c.execute(f"UPDATE employee_attendance SET time_out = ? WHERE employee_id = ? AND time_out = 'None'",
                       (time_now, id))
        self.connection.commit()
        messagebox.showinfo('INFORMATION', 'THANK YOU')
    else:
        messagebox.showinfo('INFORMATION', 'YOU ALREADY TIMED OUT OR NOT TIMED IN YET')
