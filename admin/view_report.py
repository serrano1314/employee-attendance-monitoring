from config_var import *

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import date, datetime
from calendar import monthrange
from PIL import ImageTk, Image

import matplotlib.pyplot as plt

#install numpy and matplotlib
figure_w = 400
figure_h = 300

def monthly_report_func(event, self):
    cur_month_str = self.month_combo.get()
    cur_year_str = self.year_combo.get()
    graph_type = self.gtype_combo.get()
    cur_month_num = datetime.strptime(cur_month_str,'%b').strftime('%B')
    dates_of_month = []
    x_dates_of_month = []
    y_atten_count = []
    
    # get the last date of the month
    last_day = monthrange(int(self.cur_year), month_option.index(cur_month_str)+1)[1]+1

    # loop for appending month and date
    for x in range(1,last_day):
        if x < 10: 
            # if single digit, will add a leading zero
            dates_of_month.append(f'{cur_month_str}-{str(x).zfill(2)}-{cur_year_str}')
            x_dates_of_month.append(str(x).zfill(2))
        else:
            dates_of_month.append(f'{cur_month_str}-{str(x)}-{cur_year_str}')
            x_dates_of_month.append(str(x))

    for date in dates_of_month:
        self.c.execute(f"""SELECT COUNT(status) FROM employee_attendance
                WHERE (status = 'LATE' OR status='PRESENT') AND attendance_date LIKE '%{date}%'
        """)
        y_atten_count.append(self.c.fetchone()[0])
    
    self.c.execute("SELECT * FROM employees WHERE employee_id  != 'admin'")
    num_of_emp = len(self.c.fetchall())

    fig = plt.figure()
    fig.patch.set_facecolor(BGCOLOR)

    if graph_type == 'bar':
        plt.bar(x_dates_of_month,y_atten_count)
    if graph_type == 'plot':
        plt.plot(x_dates_of_month,y_atten_count,'.-')

    plt.ylim(top=num_of_emp)
    plt.xticks(rotation=65)
    plt.margins(0.01)
    # plt.title('Monthly Attendance Report')
    plt.ylabel('NUMBER OF ATTENDANCE')
    plt.xlabel(f'DATE OF MONTH FOR {cur_month_num.upper()} {cur_year_str.upper()}',labelpad=5)
    plt.savefig('report_fig/monthly_report.png')
    plt.close()

    dates_of_month.clear()
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
    graph = plt.pie(gender_num,labels=gender,autopct='%1.2f%%')
    # graph[0].set_color('#2940d3')
    # graph[1].set_color('#ff96ad')
    plt.title('Gender Distribution')
    # plt.xlabel('Gender')
    # plt.ylabel('Number of Employees')
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

    x_months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    y_per_month_count = []
    for month in x_months:
        self.c.execute(f"SELECT * from employee_attendance WHERE attendance_date like '%{month}%' AND (status = 'LATE' OR status ='PRESENT')")
        y_per_month_count.append(len(self.c.fetchall()))

    plt.bar(x_months,y_per_month_count)
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

    Label(view_report_page, height=2, width=app_w, bg=HEADER_COLOR, text='DASHBOARD', font=FONT).pack()

    clock_date = Label(view_report_page, bg=HEADER_COLOR, width=app_w)
    clock_date.pack()

    view_report_frame = Frame(view_report_page,bg=BGCOLOR)
    view_report_frame.pack(pady=0, fill=BOTH, expand=1)
    
    self.current_time(clock_date)
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
    years_list = [str(x) for x in range(2010, 2050+1)]
    month_option = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    g_type = ['bar','plot']
    cur_month = date.today().strftime('%b')
    self.cur_year = date.today().strftime('%Y')
    
    monthly_report_frame=LabelFrame(new_frame,text="MONTHLY ATTENDACE REPORT",bg=BGCOLOR,pady=frame_h,padx=frame_w)
    self.month_combo = ttk.Combobox(monthly_report_frame, value=month_option, width=5,state="readonly")
    self.month_combo.current(month_option.index(cur_month))
    
    self.year_combo = ttk.Combobox(monthly_report_frame, value=years_list, width=5,state="readonly")
    self.year_combo.current(years_list.index(self.cur_year))

    self.gtype_combo = ttk.Combobox(monthly_report_frame, value=g_type, width=5,state="readonly")
    self.gtype_combo.current(0)

    self.month_label = Label(monthly_report_frame)

    #call function to display graph immediatley, imidyetli, emidiatley, agad nalang
    monthly_report_func(self,self)

    self.month_combo.bind('<<ComboboxSelected>>',lambda event, s=self:monthly_report_func(event,s))
    self.year_combo.bind('<<ComboboxSelected>>',lambda event, s=self:monthly_report_func(event,s))
    self.gtype_combo.bind('<<ComboboxSelected>>',lambda event, s=self:monthly_report_func(event,s))

    self.month_label.grid(row=0,column=0,columnspan=3)
    self.month_combo.grid(row=1,column=1,padx=5)
    self.year_combo.grid(row=1,column=1,sticky=E,padx=5)
    Label(monthly_report_frame,text="Graph Type: ",bg=BGCOLOR).grid(row=1,column=2)
    self.gtype_combo.grid(row=1,column=2,sticky=E,padx=5)
    monthly_report_frame.grid(row=1,column=1,columnspan=2)
    
    ttk.Separator(new_frame,orient='horizontal').grid(row=2,column=1,columnspan=3,sticky=EW,pady=30)
    Label(new_frame,text=" OTHER REPORT ",bg=BGCOLOR,font='Verdana, 12').grid(row=2,column=1,columnspan=3)

    #frame from active and inactive report, edit the active_report_func function for the content
    fig = plt.figure()
    fig.patch.set_facecolor(BGCOLOR)
    active_report_frame=LabelFrame(new_frame,text='ACTIVE AND INACTIVE REPORT',bg=BGCOLOR,pady=frame_w,padx=frame_h)
    active_report_func(self,active_report_frame)
    active_report_frame.grid(row=3,column=1, padx=10)

    fig = plt.figure()
    fig.patch.set_facecolor(BGCOLOR)
    #frame attendace graph, edit the hearbeat_report_func function for the content
    hearbeat_report_frame=LabelFrame(new_frame,text='CURRENT YEAR ATTENDANCE REPORT',bg=BGCOLOR,pady=frame_h,padx=frame_w)
    hearbeat_report_func(self,hearbeat_report_frame)
    hearbeat_report_frame.grid(row=3,column=2, padx=10)

    fig = plt.figure()
    fig.patch.set_facecolor(BGCOLOR)
    #frame from gender report, edit the gender_report_func function for the content
    gender_report_frame=LabelFrame(new_frame,text="GENDER REPORT",bg=BGCOLOR,pady=frame_h,padx=frame_w)
    gender_report_func(self,gender_report_frame)
    gender_report_frame.grid(row=4,column=1,columnspan=2)

    back_btn=Button(view_report_frame, image=self.back_img, bd=0, bg=BGCOLOR,command=lambda: [view_report_page.destroy(), menu_page.deiconify()])
    back_btn.place(x=900,y=450)
    view_report_page.protocol("WM_DELETE_WINDOW", lambda: [view_report_page.destroy(), menu_page.deiconify()])


def mouse_scroll(event, canvas):
    try:
        canvas.yview_scroll(-1*int(event.delta/120), "units")
    except:
        pass