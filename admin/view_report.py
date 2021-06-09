from config_var import *

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import date
from calendar import monthrange,month_name
from PIL import ImageTk, Image

import matplotlib.pyplot as plt

#install numpy and matplotlib
figure_w = 400
figure_h = 300

def monthly_report_func(event, self):
    cur_month_str = self.month_combo.get()
    dates_of_month = []
    x_dates_of_month = []
    y_atten_count = []
    last_day = monthrange(self.cur_year, month_option.index(cur_month_str)+1)[1]+1
    for x in range(1,last_day):
        if x < 10:
            dates_of_month.append(f'{cur_month_str}-{str(x).zfill(2)}')
            x_dates_of_month.append(str(x).zfill(2))
        else:
            dates_of_month.append(f'{cur_month_str}-{str(x)}')
            x_dates_of_month.append(str(x))

    for date in dates_of_month:
        self.c.execute(f"""SELECT COUNT(status) FROM employee_attendance
                WHERE (status = 'LATE' OR status='PRESENT') AND attendance_date LIKE '%{date}%'
        """)
        y_atten_count.append(self.c.fetchone()[0])
    
    fig = plt.figure()
    fig.patch.set_facecolor(BGCOLOR)
    plt.bar(x_dates_of_month,y_atten_count)
    # plt.ylim(top=num_of_emp)
    plt.xticks(rotation=65)
    # plt.title('Monthly Attendance Report')
    plt.ylabel('NUMBER OF ATTENDANCE')
    plt.xlabel(f'DATE OF MONTH FOR {cur_month_str.upper()}',labelpad=5)
    plt.savefig('report_fig/monthly_report.png')
    plt.close()

    y_atten_count.clear()
    x_dates_of_month.clear()
    self.monthly_fig = ImageTk.PhotoImage(Image.open('report_fig/monthly_report.png').resize((600, 430), Image.ANTIALIAS))
    self.month_label.config(image=self.monthly_fig)

def gender_report_func(self,frame):
    gender_num = []
    self.c.execute("SELECT * FROM employees WHERE sex = 'MALE'")
    gender = ['MALE', 'FEMALE']
    gender_num.append(len(self.c.fetchall()))
    self.c.execute("SELECT * FROM employees WHERE sex = 'FEMALE'")
    gender_num.append(len(self.c.fetchall()))
    graph = plt.bar(gender, gender_num)
    graph[0].set_color('#2940d3')
    graph[1].set_color('#ff96ad')
    # plt.title('Gender Distribution')
    plt.xlabel('Gender')
    plt.ylabel('Number of Employees')
    plt.savefig("report_fig/gender_graph.png")
    plt.close()

    self.gender_report_img = ImageTk.PhotoImage(Image.open('report_fig/gender_graph.png').resize((figure_w, figure_h), Image.ANTIALIAS))
    Label(frame,image=self.gender_report_img,bg=BGCOLOR).pack()
    

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
    
    # plt.title('ACTIVE AND INACTIVE EMPLOYEES')
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
        self.c.execute(f"SELECT * from employee_attendance WHERE attendance_date like '%{month}%' AND (status = 'LATE' OR status ='PRESENT')")
        y_per_month_count.append(len(self.c.fetchall()))

    plt.bar(x_months,y_per_month_count)
    # plt.ylim(top=num_of_emp)
    # plt.title('Current Year Attendance Report')
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

    Label(view_report_page, height=2, width=600, bg=HEADER_COLOR, text='DASHBOARD', font=FONT).pack()
    view_report_frame = Frame(view_report_page,bg=BGCOLOR)
    view_report_frame.pack(pady=0, fill=BOTH, expand=1)

    canvas = Canvas(view_report_frame, bg=BGCOLOR, highlightthickness=0)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)

    scroll = Scrollbar(view_report_frame, orient=VERTICAL, command=canvas.yview)
    scroll.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=scroll.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    new_frame = Frame(canvas, bg=BGCOLOR,padx=60)
    canvas.create_window((0,0),window=new_frame, anchor='nw')
    canvas.bind_all("<MouseWheel>", lambda e: mouse_scroll(e, canvas))

    frame_w = 5
    frame_h = 5
    # I use LabelFrame just to see the division of contents, maybe change into Frame later

    global month_option
    month_option = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    cur_month = int(date.today().strftime('%m'))-1
    self.cur_year = int(date.today().strftime('%Y'))
    
    monthly_report_frame=LabelFrame(new_frame,text="MONTHLY ATTENDACE REPORT",bg=BGCOLOR,pady=frame_h,padx=frame_w)
    self.month_combo = ttk.Combobox(monthly_report_frame, value=month_option, width=5,state="readonly")
    self.month_combo.current(cur_month)
    self.month_label = Label(monthly_report_frame,text='hello')
    monthly_report_func(self,self)
    self.month_combo.bind('<<ComboboxSelected>>',lambda event, s=self:monthly_report_func(event,s))
    self.month_label.pack()
    self.month_combo.pack()
    monthly_report_frame.grid(row=1,column=1,columnspan=2)
    
    fig = plt.figure()
    fig.patch.set_facecolor(BGCOLOR)
    #frame from active and inactive report, edit the active_report_func function for the content
    active_report_frame=LabelFrame(new_frame,text='ACTIVE AND INACTIVE REPORT',bg=BGCOLOR,pady=frame_w,padx=frame_h)
    active_report_func(self,active_report_frame)
    active_report_frame.grid(row=2,column=1, padx=10)

    fig = plt.figure()
    fig.patch.set_facecolor(BGCOLOR)
    #frame attendace graph, edit the hearbeat_report_func function for the content
    hearbeat_report_frame=LabelFrame(new_frame,text='CURRENT YEAR ATTENDANCE REPORT',bg=BGCOLOR,pady=frame_h,padx=frame_w)
    hearbeat_report_func(self,hearbeat_report_frame)
    hearbeat_report_frame.grid(row=2,column=2, padx=10)

    fig = plt.figure()
    fig.patch.set_facecolor(BGCOLOR)
    #frame from gender report, edit the gender_report_func function for the content
    gender_report_frame=LabelFrame(new_frame,text="GENDER REPORT",bg=BGCOLOR,pady=frame_h,padx=frame_w)
    gender_report_func(self,gender_report_frame)
    gender_report_frame.grid(row=3,column=1,columnspan=2)

    back_btn=Button(view_report_frame, image=self.back_img, bd=0, bg=BGCOLOR,command=lambda: [view_report_page.destroy(), menu_page.deiconify()])
    back_btn.place(x=900,y=480)
    view_report_page.protocol("WM_DELETE_WINDOW", lambda: [view_report_page.destroy(), menu_page.deiconify()])


def mouse_scroll(event, canvas):
    try:
        canvas.yview_scroll(-1*int(event.delta/120), "units")
    except:
        pass