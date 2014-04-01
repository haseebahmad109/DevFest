from Tkinter import *
import tkFont
from AutoScrollBar import AutoScrollbar
import tkMessageBox


root = Tk()
root.title("Outreach Application")
root.wm_iconbitmap("icon.ico")



screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.state('zoomed')
root.geometry("%sx%s+%s+%s" % (int(screen_width * 0.99),
                               int(screen_height * 0.9),
                               (screen_width - int(screen_width*0.7))/2,
                               0))

vscrollbar = AutoScrollbar(root)
vscrollbar.grid(row=0, column=1, sticky=N+S)


canvas = Canvas(root,
                yscrollcommand=vscrollbar.set,
               )
canvas.grid(row=0, column=0, sticky=N+S+E+W)

vscrollbar.config(command=canvas.yview)

# make the canvas expandable
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

#
# create canvas contents

frame = Frame(canvas)
frame.rowconfigure(1, weight=1)
frame.columnconfigure(1, weight=1)

CoursePoints = {"BIS": 0, "CS": 0, "VC": 0, "HP": 0, "SF": 0, "SE": 0}

Page = Frame(frame, width=700, bg="#ffffff", highlightthickness=1, highlightbackground="#111")
Page.grid(row=0, column=0, padx=(screen_width - 700)/2)



inner_page = Frame(Page, width=700, bg="#ffffff", highlightthickness=0, highlightbackground="#ffffff")
inner_page.pack(pady=20, padx=20)

top_text_font = tkFont.Font(family="san-serif", size=12, weight="bold", slant="italic")

top_text = "Outreach Application"

label = Label(inner_page,  bg="#ffffff", anchor=W, fg="#c0c0c0", justify=LEFT, text=top_text, font=top_text_font)
label.pack()

#
def scale_first(val):
    if val >= 5:
        CoursePoints["BIS"] += 5

question1 = LabelFrame(inner_page, width=700, height=110, bg="#ffffff", text="1", padx=5, pady=5)
question1.pack(padx=10, pady=10)
question1.pack_propagate(False)

question1_text = "On a scale of 1 to 10 (1 being not interested, 10 being very interested),\n " \
                 "would you say are interested in the business aspects of computing? "
label1 = Label(question1, bg="#ffffff", anchor=W, fg="#000000", justify=LEFT, text=question1_text)
label1.pack()
scale_1 = Scale(question1, from_=1, to=10, orient=HORIZONTAL, command=scale_first)
scale_1.pack()
#


#
def yes_2nd():
    CoursePoints["SF"] += 5
    CoursePoints["CS"] += 5

question2 = LabelFrame(inner_page, width=700, height=110, bg="#ffffff", text="2", padx=5, pady=5)
question2.pack(padx=10, pady=10)
question2.pack_propagate(False)

question2_text = "Would you consider yourself a logical thinker/ do you enjoy logical puzzles?"
label2 = Label(question2, pady=10, bg="#ffffff", anchor=W, fg="#000000", justify=LEFT, text=question2_text)
label2.pack()
yes_2 = Button(question2, text="Yes", command=yes_2nd)
yes_2.pack(in_=question2, side=LEFT, expand=True)
no_2 = Button(question2, text="No")
no_2.pack(in_=question2, side=LEFT, expand=True)
#

#

def selection_3rd():
    if var_3.get() == 2 or var_3.get() == 3:
        CoursePoints["CS"] += 3
    elif var_3.get() == 4:
        CoursePoints["HP"] += 3

question3 = LabelFrame(inner_page, width=700, height=110, bg="#ffffff", text="3", padx=5, pady=5)
question3.pack(padx=10, pady=10)
question3.pack_propagate(False)

question3_text = "What's the highest qualifications do you have in maths?"
label3 = Label(question3, pady=10, bg="#ffffff", anchor=W, fg="#000000", justify=LEFT, text=question3_text)
label3.pack()
var_3 = IntVar()
r1_3 = Radiobutton(question3, text="GCSE", variable=var_3, value=1, command=selection_3rd)
r1_3.pack(anchor=CENTER, side=LEFT, expand=True)

r2_3 = Radiobutton(question3, text="AS", variable=var_3, value=2, command=selection_3rd)
r2_3.pack(anchor=CENTER, side=LEFT, expand=True)

r3_3 = Radiobutton(question3, text="A2", variable=var_3, value=3, command=selection_3rd)
r3_3.pack(anchor=CENTER, side=LEFT, expand=True)

r4_3 = Radiobutton(question3, text="AS/A2 Further", variable=var_3, value=4, command=selection_3rd)
r4_3.pack(anchor=CENTER, side=LEFT, expand=True)

#

#
question4 = LabelFrame(inner_page, width=700, height=110, bg="#ffffff", text="4", padx=5, pady=5)
question4.pack(padx=10, pady=10)
question4.pack_propagate(False)


def scale_4th(val):
    if val >= 5:
        CoursePoints["VC"] += 5


question4_text = "On a scale of 1 to 10 (1 being not interested, 10 being very interested),\n" \
                 " would you say are interested in 3D modelling/visual representation?"
label4 = Label(question4, bg="#ffffff", anchor=W, fg="#000000", justify=LEFT, text=question4_text)
label4.pack()
scale_4 = Scale(question4, from_=1, to=10, orient=HORIZONTAL)
scale_4.pack()
#

#
def selection_5():
    if var_5.get() == 1:
        CoursePoints["VC"] += 3
    elif var_5.get() == 2:
        CoursePoints["SF"] += 3
        CoursePoints["HP"] += 2

question5 = LabelFrame(inner_page, width=700, height=110, bg="#ffffff", text="5", padx=5, pady=5)
question5.pack(padx=10, pady=10)
question5.pack_propagate(False)

question5_text = "Do you prefer to create a system or improve it?"
label5 = Label(question5, bg="#ffffff", anchor=W, fg="#000000", justify=LEFT, text=question5_text)
label5.pack()
var_5 = IntVar()
r1_5 = Radiobutton(question5, text="Create", variable=var_5, value=1, command=selection_5)
r1_5.pack(anchor=CENTER, side=LEFT, expand=True)

r2_5 = Radiobutton(question5, text="Improve", variable=var_5, value=2, command=selection_5)
r2_5.pack(anchor=CENTER, side=LEFT, expand=True)
#

#

def selection_6():
    if var_6.get() == 1:
        CoursePoints["SE"] += 5
        CoursePoints["BIS"] += 3

question6 = LabelFrame(inner_page, width=700, height=110, bg="#ffffff", text="6", padx=5, pady=5)
question6.pack(padx=10, pady=10)
question6.pack_propagate(False)

question6_text = "Do you like working in a team or managing it?"
label6 = Label(question6, bg="#ffffff", anchor=W, fg="#000000", justify=LEFT, text=question6_text)
label6.pack()
var_6 = IntVar()
r1_6 = Radiobutton(question6, text="Team Member", variable=var_6, value=1, command=selection_6)
r1_6.pack(anchor=CENTER, side=LEFT, expand=True)

r2_6 = Radiobutton(question6, text="Manager", variable=var_6, value=2, command=selection_6)
r2_6.pack(anchor=CENTER, side=LEFT, expand=True)
#

#

def selection_7():
    if var_7.get() == 1:
        CoursePoints["HP"] += 3
    elif var_7.get() == 2:
        CoursePoints["SE"] += 3
question7 = LabelFrame(inner_page, width=700, height=110, bg="#ffffff", text="7", padx=5, pady=5)
question7.pack(padx=10, pady=10)
question7.pack_propagate(False)

question7_text = "Does working as part of a large team interest you as oppose to small team / on your own?"
label7 = Label(question7, bg="#ffffff", anchor=W, fg="#000000", justify=LEFT, text=question7_text)
label7.pack()
var_7 = IntVar()
r1_7 = Radiobutton(question7, text="Small Team", variable=var_7, value=1, command=selection_7)
r1_7.pack(anchor=CENTER, side=LEFT, expand=True)

r2_7 = Radiobutton(question7, text="Large Team", variable=var_7, value=2, command=selection_7)
r2_7.pack(anchor=CENTER, side=LEFT, expand=True)
#


#

def yes_8th():
    CoursePoints["CS"] += 2

def no_8th():
    CoursePoints["BIS"] += 2

def maybe_8th():
    CoursePoints["SE"] += 2

question8 = LabelFrame(inner_page, width=700, height=110, bg="#ffffff", text="8", padx=5, pady=5)
question8.pack(padx=10, pady=10)
question8.pack_propagate(False)

question8_text = "Would you be interested in a career as a programmer?"
label8 = Label(question8, bg="#ffffff", anchor=W, fg="#000000", justify=LEFT, text=question8_text)
label8.pack()
yes_8 = Button(question8, text="Yes", command=yes_8th)
yes_8.pack(in_=question8, side=LEFT, expand=True)
no_8 = Button(question8, text="No", command=no_8th)
no_8.pack(in_=question8, side=LEFT, expand=True)
maybe_8 = Button(question8, text="Maybe", command=maybe_8th)
maybe_8.pack(in_=question8, side=LEFT, expand=True)
#


#
def selection_9th():
    if var_9.get() == 1:
        CoursePoints["SF"] += 2
    elif var_9.get() == 2:
        CoursePoints["VC"] += 2

question9 = LabelFrame(inner_page, width=700, height=110, bg="#ffffff", text="9", padx=5, pady=5)
question9.pack(padx=10, pady=10)
question9.pack_propagate(False)

question9_text = "Are you interested in more hardware or software?"
label9 = Label(question9, bg="#ffffff", anchor=W, fg="#000000", justify=LEFT, text=question8_text)
label9.pack()
var_9 = IntVar()
r1_9 = Radiobutton(question9, text="Hardware", variable=var_9, value=1, command=selection_9th)
r1_9.pack(anchor=CENTER, side=LEFT, expand=True)

r2_9 = Radiobutton(question9, text="Software", variable=var_9, value=2, command=selection_9th)
r2_9.pack(anchor=CENTER, side=LEFT, expand=True)

r3_9 = Radiobutton(question9, text="No preference", variable=var_9, value=3, command=selection_9th)
r3_9.pack(anchor=CENTER, side=LEFT, expand=True)
#

#
question10 = LabelFrame(inner_page, width=700, height=110, bg="#ffffff", text="10", padx=5, pady=5)
question10.pack(padx=10, pady=10)
question10.pack_propagate(False)

def yes_10th():
    CoursePoints["HP"] += 2

question10_text = "Would you like to work on a large scale project?"
label10 = Label(question10, bg="#ffffff", anchor=W, fg="#000000", justify=LEFT, text=question8_text)
label10.pack()
yes_10 = Button(question10, text="Yes", command=yes_10th)
yes_10.pack(in_=question10, side=LEFT, expand=True)
no_10 = Button(question10, text="No")
no_10.pack(in_=question10, side=LEFT, expand=True)
#


#
import operator

def check():
    sorted_list = sorted(CoursePoints.iteritems(), key=operator.itemgetter(1))
    if sorted_list[5][0] == "VC":
        tkMessageBox.showinfo("Course", "Computer Science with Visual Computing")
    elif sorted_list[5][0] == "BIS":
        tkMessageBox.showinfo("Course", "Business Information Systems")
    elif sorted_list[5][0] == "CS":
        tkMessageBox.showinfo("Course", "Computer Science")
    elif sorted_list[5][0] == "HP":
        tkMessageBox.showinfo("Course", "Computer Science with High Performance Computing ")
    elif sorted_list[5][0] == "SF":
        tkMessageBox.showinfo("Course", "Computer Science with Security and Forensics")

    print sorted_list
    return True

submit = Button(inner_page, text="Submit", command=check)
submit.pack(expand=True)



canvas.create_window(0, 0, anchor=NW, window=frame)

frame.update_idletasks()

canvas.config(scrollregion=canvas.bbox("all"))

root.mainloop()