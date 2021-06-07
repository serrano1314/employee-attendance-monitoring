from config_var import *

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image

import matplotlib.pyplot as plt

#install numpy and matplotlib
figure_w = 400
figure_h = 300

def gender_report_func(self,frame):
    Label(frame,text='data visualization here').pack(pady=100,padx=75)
    

def active_report_func(self,frame):

    self.c.execute("SELECT * FROM employees WHERE work_status = 'active'")
    active_emp = self.c.fetchall()

    self.c.execute("SELECT * FROM employees WHERE work_status = 'inactive'")
    inactive_emp = self.c.fetchall()

    x = ['ACTIVE','INACTIVE'] #values in the x axis 
    y = [len(active_emp), len(inactive_emp)] #values in the y axis 

    barlist=plt.bar(x,y)
    barlist[0].set_color('#00ff5e')   
    barlist[1].set_color('#fd085b')
    
    plt.title('ACTIVE AND INACTIVE EMPLOYEES')
    plt.ylabel('NUMBER OF EMPLOYEES')
    plt.xlabel('WORK STATUS OF EMPLOYEE')
    plt.savefig('report_fig/active_report.png')
    plt.close()

    self.report_fig = ImageTk.PhotoImage(Image.open('report_fig/active_report.png').resize((figure_w, figure_h), Image.ANTIALIAS))
    Label(frame,image=self.report_fig,bg=BGCOLOR).pack()
    

def hearbeat_report_func(self,frame):

    self.c.execute("SELECT * FROM employees WHERE employee_id  != 'admin'")
    num_of_emp = len(self.c.fetchall())*30

    x_months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    y_per_month_count = []
    for month in x_months:
        self.c.execute(f"SELECT * from employee_attendance WHERE attendance_date LIKE '%{month}%' AND (status = 'LATE' OR status ='PRESENT')")
        y_per_month_count.append(len(self.c.fetchall()))

    plt.bar(x_months,y_per_month_count)
    # plt.ylim(top=num_of_emp)
    plt.title('Current Year Attendance Report')
    plt.ylabel('NUMBER OF EMPLOYEES')
    plt.xlabel('Month')
    plt.savefig('report_fig/hearbeat_report.png')
    plt.close()

    self.hearbeat_fig = ImageTk.PhotoImage(Image.open('report_fig/hearbeat_report.png').resize((figure_w, figure_h), Image.ANTIALIAS))
    Label(frame,image=self.hearbeat_fig,bg=BGCOLOR).pack()
    

def view_report(self,menu_page):
    view_report_page = Toplevel()
    view_report_page.title('Summary / Report')
    view_report_page.geometry(self.WINDOW_SIZE)
    view_report_page.config(bg=BGCOLOR)
    view_report_frame = Frame(view_report_page,bg=BGCOLOR)
    view_report_frame.pack(pady=10)

    frame_w = 5
    frame_h = 5
    # I use LabelFrame just to see the division of contents, maybe change into Frame later

    #frame from active and inactive report, edit the active_report_func function for the content
    active_report_frame=LabelFrame(view_report_frame,text='ACTIVE AND INACTIVE REPORT',bg=BGCOLOR,pady=frame_w,padx=frame_h)
    active_report_func(self,active_report_frame)
    active_report_frame.grid(row=1,column=1)

    #frame attendace graph, edit the hearbeat_report_func function for the content
    hearbeat_report_frame=LabelFrame(view_report_frame,text='ATTENDANCE HEARBEAT',bg=BGCOLOR,pady=frame_h,padx=frame_w)
    hearbeat_report_func(self,hearbeat_report_frame)
    hearbeat_report_frame.grid(row=1,column=2)

    #frame from gender report, edit the gender_report_func function for the content
    gender_report_frame=LabelFrame(view_report_frame,text="GENDER REPORT",bg=BGCOLOR,pady=frame_h,padx=frame_w)
    gender_report_func(self,gender_report_frame)
    gender_report_frame.grid(row=2,column=1)

    

    back_btn=Button(view_report_page, image=self.back_img, bd=0, command=lambda: [view_report_page.destroy(), menu_page.deiconify()])
    back_btn.place(x=900,y=525)
    view_report_page.protocol("WM_DELETE_WINDOW", lambda: [view_report_page.destroy(), menu_page.deiconify()])
