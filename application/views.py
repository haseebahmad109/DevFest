from django.shortcuts import render_to_response, render
from application.forms import UserCreationForm, UserCreationForm2, LoginForm, add_course, add_assignment
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from application.models import User, course, assignment, \
    course_assignment, assignment_submission, course_student, teacher, questionsession, questionsmessages, message, notes, MCQ, quizz, marked_quiz
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from itertools import izip
import random


def home(request):
    a = course.objects.all()[:3]
    args = {}
    args['courses_1'] = a[0]
    args['courses_2'] = a[1]
    args['courses_3'] = a[2]
    return render(request, 'home.html', args)


def dashboard(request):
    if request.user.user_type == "Student":
        courseStudent = course_student.objects.filter(student_id=request.user.id)
        allCourses = []
        for c in courseStudent:
            allCourses.append(course.objects.filter(id=c.course_id.id)[0])

        assignmentofthisuser = assignment_submission.objects.filter(student_id = request.user)
        marks = {}

        for k in allCourses:
            total_marks=0
            obtained_marks=0
            weightage=0
            course_assignment1 = course_assignment.objects.filter(course_id = k.id)
            for j in course_assignment1:
                for g in assignmentofthisuser:
                    if g.assignment_id == j.assignment_id:
                        if j is not None and g and g.marks:
                            obtained_marks = int(obtained_marks) + int(g.marks)
                            total_marks = total_marks + 10
                            weightage = weightage + j.assignment_id.weightage

            marks[k.id] = ((obtained_marks/total_marks)*weightage)

        args = {}
        args['all_courses'] = allCourses
        args['all_marks'] = marks
    else:
        allCourses = course.objects.filter(taughtby=request.user)
        args = {}
        args['all_courses'] = allCourses
    return render(request, 'dashboard.html', args)


def sign_in(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard')
    else:
        args = {}
        args.update(csrf(request))
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(username=request.POST["username"], password=request.POST["password"])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect('/dashboard')
                    else:
                        args['myErrors'] = "User Not Activated."
                else:
                    args['myErrors'] = "Username or passwords Don't match."
        else:
            form = LoginForm()

        args['form'] = form
        return render_to_response('signin.html', args, RequestContext(request))


def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard')
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if request.POST['password'] != request.POST['confirm_password']:
                args = {}
                args.update(csrf(request))
                args['password_error'] = 'Passwords donot match'
                args['form'] = form
                return render_to_response('signup.html', args, RequestContext(request))
            if form.is_valid():
                form.save()
                user = authenticate(username=request.POST['email'], password=request.POST['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        request.user.save()
                    else:
                        return "not activated"
                else:
                    return HttpResponse("<h1>User Cannot be authenticated</h1>")
                args = {}
                args.update(csrf(request))
                args['form'] = UserCreationForm2()

                return HttpResponseRedirect("/signup2", args)
        else:
            form = UserCreationForm()

        args = {}
        args.update(csrf(request))
        args['form'] = form
        return render_to_response('signup.html', args)


@login_required()
def signup2(request):
    if request.method == 'POST':
        form = UserCreationForm2(request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect('/dashboard')
    else:
        form = UserCreationForm2()

    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render_to_response('signup2.html', args, RequestContext(request))


@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/', RequestContext(request))



@login_required()
def add_course_view(request):

    args = {}
    args.update(csrf(request))


    if request.user.is_authenticated():
        if request.user.user_type == 'Teacher':
            if request.method =='POST':
                form = add_course(request.POST, request.FILES)
                if form.is_valid():
                    currentcourse = course()
                    currentcourse.name = request.POST['name']
                    currentcourse.code = request.POST['code']
                    currentcourse.description = request.POST['description']
                    currentcourse.coursepic= request.FILES['coursepic']

                    currentcourse.taughtby = request.user

                    currentcourse.save()
                    return HttpResponseRedirect('/dashboard')
                else:
                    args['form'] = form
                    return render_to_response('addcourse.html', args, RequestContext(request))
            else:
                form = add_course()
                args['form'] = form
                return render_to_response('addcourse.html', args, RequestContext(request))

        else:
            return HttpResponse("You are not allowed to access this Page <a href="/">Go Back</a>")
    else:
        return HttpResponseRedirect('/home',RequestContext(request))


def courses(request):
    all_courses = course.objects.all()
    args = {}
    args['courses'] = all_courses
    return render(request, 'courses.html', args)


def _course(request, id=None):
    corse = course.objects.filter(id=id)
    if corse:
        args = {}
        args['course'] = corse[0]
        assignments_c = course_assignment.objects.filter(course_id=corse[0])
        assignments = []
        for a in assignments_c:
            assignments.append(a.assignment_id)
        args['assignments'] = assignments
        alreay_registered = False
        all_students = course_student.objects.all()
        for s in all_students:
            if s.student_id == request.user and s.course_id == corse[0]:
                alreay_registered = True
        allnotes = notes.objects.filter(which_course=corse[0])
        args['notes'] = allnotes

        args['alreay_registered'] = alreay_registered

        args['quizes'] = quizz.objects.filter(belongs_to=corse)
    else:
        return HttpResponseRedirect('/courses')

    return render_to_response('course.html', args, RequestContext(request))



def add_assignment_view(request):
    args = {}
    args.update(csrf(request))
    if request.user.is_authenticated():
        if request.user.user_type == 'Teacher':
            if request.method =='POST':
                form = add_assignment(request.POST, request.FILES)
                if form.is_valid():
                    currentassignment = assignment()
                    currentassignment.title = request.POST['title']
                    currentassignment.description = request.POST['description']
                    currentassignment.weightage = request.POST['weightage']
                    currentassignment.document = request.FILES['document']
                    c = course.objects.filter(id=request.POST['name'])
                    currentassignment.save()
                    ass = course_assignment()
                    ass.course_id = c[0]
                    ass.assignment_id = currentassignment
                    ass.save()

                    return HttpResponseRedirect('/courses')
                else:
                    args['form'] = form

                    return render_to_response('addassignment.html', args, RequestContext(request))
            else:
                form = add_assignment()
                args['form'] = form
                co = course.objects.filter(taughtby=request.user)
                if not co:
                    return HttpResponseRedirect('/dashboard')
                args['courses'] = co
                return render_to_response('addassignment.html', args, RequestContext(request))
        else:
            return HttpResponse("You are not allowed to access this Page <a href="/">Go Back</a>")
    else:
        return HttpResponseRedirect('/home',RequestContext(request))


def submit_assignment_view(request):
    if request.method == "POST":
        a_s = assignment_submission()
        ass = assignment.objects.filter(id=request.POST['assignment'])
        a_s.assignment_id = ass[0]
        a_s.student_id = request.user
        a_s.submission_file = request.FILES['submission_file']
        a_s.save()
        return HttpResponseRedirect('/dashboard')


def register_course_view(request):
    c = course_student()
    c.student_id = request.user
    c.course_id = course.objects.filter(id=request.POST['register'])[0]
    c.save()
    return HttpResponseRedirect('/dashboard')


def view_teachers(request):
    all_teachers = User.objects.filter(user_type="Teacher")
    args = {}
    args['all_teachers'] = all_teachers
    return render(request, 'teachers.html', args)



@login_required()
def ask_question_view(request):
    args = {}
    args.update(csrf(request))

    if request.user.user_type != 'Student':
        return HttpResponse("You are not allowed to access this Page <a href='/'>Go Back</a>")

    else:
        if request.method == 'POST':
            useraskedfrom = User.objects.filter(id=request.POST['sentid'])[0]
            if useraskedfrom.user_type == 'Student':
                return HttpResponse("You are not allowed to access this Page <a href='/'>Go Back</a>")
            else:

                messagetosend = request.POST['messagetext']

                newquestionsession = questionsession()
                newquestionsession.askedfrom =useraskedfrom
                newquestionsession.askedby = request.user
                newquestionsession.firstmessage = messagetosend
                newquestionsession.save()

                newmessage = message()
                newmessage.askedfrom = useraskedfrom
                newmessage.askedby = request.user
                newmessage.mess = messagetosend
                newmessage.save()

                newquestionsmessages  = questionsmessages()
                newquestionsmessages.question_id = newquestionsession
                newquestionsmessages.message_id = newmessage
                newquestionsmessages.save()


                return HttpResponseRedirect("/dashboard")

        elif request.method =='GET':
            sentuserid = request.GET['sentid']
            sentuserinstance = User.objects.filter(id=sentuserid)[0]
            args['sentid'] = sentuserid
            args['sentname'] = sentuserinstance.get_full_name()

            return render_to_response('askquestion.html', args, RequestContext(request))



@login_required()
def reply_question_view(request):
    args = {}
    args.update(csrf(request))

    if request.method == 'POST':
        useraskedfrom = User.objects.filter(id=request.POST['sentid'])[0]
        questionbelongsto = questionsession.objects.filter(id= request.POST['questid'])[0]
        messagetosend = request.POST['messagetext']
        newmessage = message()
        newmessage.askedfrom = useraskedfrom
        newmessage.askedby = request.user
        newmessage.mess = messagetosend
        questionbelongsto.firstmessage = messagetosend
        questionbelongsto.save()
        newmessage.save()

        newquestionsmessages  = questionsmessages()
        newquestionsmessages.question_id = questionbelongsto
        newquestionsmessages.message_id = newmessage
        newquestionsmessages.save()

        return HttpResponseRedirect("/dashboard")

    elif request.method =='GET':
        sentuserid = request.GET['sentid']
        sentquestionid = request.GET['questid']
        sentuserinstance = User.objects.filter(id=sentuserid)[0]
        args['sentid'] = sentuserid
        args['questid'] = sentquestionid
        args['sentname'] = sentuserinstance.get_full_name()
        return render_to_response('replyquestion.html', args, RequestContext(request))


def mail_box_view(request):
    all_messages = questionsession.objects.filter(askedby=request.user) | questionsession.objects.filter(askedfrom=request.user)
    args = {}
    args.update(csrf(request))
    args['all_messages'] = all_messages
    return render(request, 'mailbox.html', args)

@login_required()
def show_messageview (request):
    if request.method =='GET':
        questionidsent = request.GET['questid']
        myquestionmessages = questionsmessages.objects.filter(question_id=questionidsent)
        args = {}
        args['messageids'] = myquestionmessages
        args['first'] = myquestionmessages[0].question_id.id
        return render_to_response('messageview.html',args, RequestContext(request))


@login_required()
def rate_the_question (request):
   if request.method == 'POST':
       questionbelongsto = questionsession.objects.filter(id= request.POST['questid'])[0]
       idoftheraterer = request.POST['raterer']
       ratinggiven = request.POST['ratinggiven']
       userwhorated = User.objects.filter(id=idoftheraterer)[0]
       if userwhorated.user_type == 'Student':
           questionbelongsto.ratingofstudent=ratinggiven
       elif userwhorated.user_type =='Teacher':
           questionbelongsto.ratingofteacher=ratinggiven

       questionbelongsto.save()

       return HttpResponseRedirect('/dashboard')
   else:
       return HttpResponse('GET request not served on this page <a href="/">Go Back</a>')


def mark_assignment(request):
    if request.method == "GET":
        assign = assignment_submission.objects.filter(assignment_id=request.GET['assignmentid'])
        args = {}
        args['all_assignments'] = assign
        return render(request, 'marking_assignment.html', args)
    elif request.method == "POST":
        which_assignment = assignment_submission.objects.filter(id=request.POST['which_assignment'])[0]
        assign = assignment_submission.objects.filter(assignment_id=which_assignment.assignment_id)
        args = {}
        args['all_assignments'] = assign
        which_assignment.marks = request.POST['marks']
        which_assignment.save()
        return render(request, 'marking_assignment.html', args)


def courses_search_view(request):
    if request.method == "GET":
        searchterm = request.GET['searchterm']
        searchedCoueses = course.objects.filter(Q(name__icontains=searchterm) | Q(description__icontains=searchterm))
        args={}
        args['courses'] = searchedCoueses
        return render(request, 'courses.html', args)


def upload_notes(request):
    if request.method == "POST":
        if "note_file" not in request.FILES:
            return HttpResponse("You didnot uploaded the file <a href='/'> Go Back</a>")
        note = notes()
        note.which_course = course.objects.filter(id=request.POST['which_course'])[0]
        note.noteFile = request.FILES['note_file']
        note.save()
        return HttpResponseRedirect("/dashboard")

def search_teachers_view(request):
    if request.method == "GET":
        search_term = request.GET['searchterm']
        searchedTeachers = User.objects.filter((Q(first_name__icontains=search_term)| Q(last_name__icontains=search_term)
                                               | Q(teacher__most_recent_job_title__icontains=search_term) |
                                               Q(teacher__subjects__icontains=search_term) ) & Q(user_type__iexact="Teacher"))

        args = {}
        args['all_teachers'] = searchedTeachers
        return render(request, 'teachers.html', args )


@login_required()
def create_Quiz(request):
    args = {}
    args.update(csrf(request))
    if request.user.is_authenticated():
        if request.user.user_type == 'Teacher':
            if request.method =='POST':
                q = quizz()
                q.title = request.POST['title']
                q.weightage = request.POST['weightage']
                q.belongs_to = course.objects.filter(id=request.POST['name'])[0]

                q.save()

                ques1 = MCQ()
                ques2 = MCQ()
                ques3 = MCQ()
                ques4 = MCQ()

                ques1.question = request.POST['question1']
                ques1.option1 = request.POST['1q1']
                ques1.option2 = request.POST['2q1']
                ques1.option3 = request.POST['3q1']
                ques1.option4 = request.POST['4q1']
                ques1.correct_answer = request.POST['answer1']
                ques1.quizz_id = q
                ques1.save()

                ques2.question = request.POST['question2']
                ques2.option1 = request.POST['1q2']
                ques2.option2 = request.POST['2q2']
                ques2.option3 = request.POST['3q2']
                ques2.option4 = request.POST['4q2']
                ques2.correct_answer = request.POST['answer2']
                ques2.quizz_id = q
                ques2.save()

                ques3.question = request.POST['question3']
                ques3.option1 = request.POST['1q3']
                ques3.option2 = request.POST['2q3']
                ques3.option3 = request.POST['3q3']
                ques3.option4 = request.POST['4q3']
                ques3.correct_answer = request.POST['answer3']
                ques3.quizz_id = q
                ques3.save()

                ques4.question = request.POST['question4']
                ques4.option1 = request.POST['1q4']
                ques4.option2 = request.POST['2q4']
                ques4.option3 = request.POST['3q4']
                ques4.option4 = request.POST['4q4']
                ques4.correct_answer = request.POST['answer4']
                ques4.quizz_id = q
                ques4.save()
                return HttpResponseRedirect('/dashboard')

            else:
                co = course.objects.filter(taughtby=request.user)
                if not co:
                    return HttpResponseRedirect('/dashboard')
                args['courses'] = co
                return render_to_response('addquiz.html', args, RequestContext(request))
        else:
            return HttpResponse("You are not allowed to access this Page <a href="/">Go Back</a>")
    else:
        return HttpResponseRedirect('/home',RequestContext(request))


@login_required()
def take_quiz(request, id=None):
    if request.method == "GET":
        q = quizz.objects.filter(id=id)[0]
        mcq = MCQ.objects.filter(quizz_id=q)
        args = {}
        args['mcq'] = mcq
        args['quiz'] = q
        return render(request, 'take_quiz.html', args)
    if request.method == 'POST':
        x = random.randint(0, 4)
        y = marked_quiz()
        y.quizid = quizz.objects.filter(id=request.POST['quizid'])[0]
        y.marks = x
        y.of_whom = request.user
        y.save()
        return HttpResponseRedirect('/dashboard')
