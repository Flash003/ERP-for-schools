from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from Darwin.models import *
from Darwin.forms import *
from django.contrib.auth.decorators import login_required
from datetime import datetime


#Views for all user types-------------------------------------------------------

def index_view(request):
    return render(request, 'Aims/index.html')

@login_required
def announcements_view(request):
    user = None
    if request.session['user_type'] == 'teacher':
        user = Teacher.objects.get(user = request.user)
    elif request.session['user_type'] == 'student':
        user = Student.objects.get(user = request.user)
    announcements_set = Announcement.objects.all().order_by('-date_and_time')[:10]
    return render(request, 'Aims/announcements.html', {'type' : request.session['user_type'] , 'USER' : user, 'announcements':announcements_set})

@login_required
def profile_view(request):
    user = None
    uname = str(request.user.username)

    is_teacher = False
    is_student = False

    try:
        teacher = Teacher.objects.get(user=request.user)
    except:
        teacher = None
    try:
        student = Student.objects.get(user=request.user)
    except:
        student = None

    #Decided uptill here whether the user is Student or Teacher
    request.session['first_name'] = request.user.first_name
    schedule = None
    count_total_attendance = -1
    count_present_attendance = -1
    schedule_set = None
    if(teacher):
        request.session['user_type'] = 'teacher'
        user = teacher
        count_total_attendance = len(TeacherAttendance.objects.filter(teacher=user))
        count_present_attendance = len(TeacherAttendance.objects.filter(teacher=user, status = 'present'))
        schedule_set = TeacherSchedule.objects.filter(teacher=teacher)
    elif (student):
        request.session['user_type'] = 'student'
        user = student
        count_total_attendance = len(StudentAttendance.objects.filter(student=user))
        count_present_attendance = len(StudentAttendance.objects.filter(student=user, status = 'present'))
        schedule_set = ClassSchedule.objects.filter(class_name=user.class_studying)
    else:
        request.session['user_type'] = 'admin'
        return HttpResponseRedirect('/admin/')


    return render(request, 'Aims/profile.html', {'type': request.session['user_type'], 'USER' : user, 'schedules' : schedule_set, 'total_attendance' : count_total_attendance, 'present_attendance' : count_present_attendance})

@login_required
def upcoming_events_view(request):
    user = None
    if request.session['user_type'] == 'teacher':
        user = Teacher.objects.get(user = request.user)
    elif request.session['user_type'] == 'student':
        user = Student.objects.get(user = request.user)
    events = Event.objects.all().order_by('-date')[:5]
    return render(request, 'Aims/upcoming_events.html', {'type' : request.session['user_type'] , 'USER' : user, 'events' : events})


@login_required
def athenium_view(request):
    return HttpResponse("Hello from Athenium Portal")

@login_required
def user_attendance_view(request):
    type = request.session['user_type']
    if type == 'student':
        user = Student.objects.get(user = request.user)
        attendance = StudentAttendance.objects.filter(student = user)
        return render(request, 'Aims/attendance_view.html',  {'type' : type, 'USER' : user, 'attendance' : attendance})
    elif type == 'teacher':
        user = Teacher.objects.get(user = request.user)
        attendance = TeacherAttendance.objects.filter(teacher = user)
        return render(request, 'Aims/attendance_view.html', {'type' : type, 'USER' : user, 'attendance' : attendance})
    else:
        return HttpResponse("You Must be Admin")


#Views only for Teachers--------------------------------------------------------
@login_required
def create_announcement_view(request):
    if request.session['user_type'] == 'student':
        HttpResponseRedirect('/profile/')
    text = ""
    user = Teacher.objects.get(user = request.user)
    if request.method == 'POST':
        heading = request.POST.get('heading')
        content = request.POST.get('content')
        announcement = Announcement()
        announcement.heading = heading
        announcement.content = content
        announcement.date_and_time = datetime.now()
        announcement.author = Teacher.objects.get(user=request.user)
        announcement.save()
        text="Announcement Created Successfully"
    return render(request, 'Aims/create_announcements.html', {'type' : request.session['user_type'] , 'USER' : user, 'text' : text})

@login_required
def leave_request_view(request):
    text = ""
    if request.session['user_type'] == 'teacher':
        teacher = Teacher.objects.get(user = request.user)
        if request.method == 'POST':
            d = request.POST.get('d')
            reason = request.POST.get('reason')
            lr = LeaveRequest()
            lr.date = d
            lr.reason = reason
            lr.user = teacher
            lr.save()
            text="Leave Request Generated Successfully"

        return render(request, 'Aims/leave_request.html', {'USER' : teacher, 'type' : 'teacher' , 'text' : text})
    else:
        HttpResponseRedirect('/')

@login_required
def marks_upload(request):
    text = ''
    if request.session['user_type'] == 'teacher':
        if request.method == 'POST':
            print(request.POST)
            teacher = Teacher.objects.get(user = request.user)
            student_set = Student.objects.filter(class_studying = teacher.class_teacher)
            for student in student_set:
                marks_obj = Marks()
                marks_obj.student = student
                subject = Subjects.objects.get(name=request.POST.get('student-subject'))
                marks_obj.subject = subject
                marks_obj.exam_name = request.POST.get('exam-name')
                marks_obj.exam_date = str(request.POST.get('exam-date'))
                marks_obj.marks_obtained = int(request.POST.get(student.user.username+'-obtained-marks'))
                marks_obj.total_marks = int(request.POST.get('maximum-marks'))
                marks_obj.uploaded_by = teacher
                marks_obj.uploaded_on = datetime.now()
                marks_obj.save()
            text='Submitted Successfully'


        #Normal case
        user = Teacher.objects.get(user = request.user)
        teacher_class = user.class_teacher
        students = Student.objects.filter(class_studying = teacher_class)
        subjects = Subjects.objects.all()
        return render(request, 'Aims/marks_upload.html', {'type' : request.session['user_type'] , 'USER' : user, 'students' : students, 'subjects' : subjects, 'text' : text})
    else:
        return HttpResponseRedirect('/')

@login_required
def publish_attendance(request):
    current_teacher = Teacher.objects.get(user = request.user)
    if request.method == 'POST':
        students = Student.objects.filter(class_studying = current_teacher.class_teacher)
        #print(request.POST)
        for s in students:
            sa = StudentAttendance()
            sa.student = s
            if request.POST.get(s.user.first_name + s.user.username) == 'present':
                sa.date = str(request.POST.get('date'))
                sa.status = "present"
                t = s.attendance_count
                t = t + 1
                s.attendance_count = t
                print("Increased")
            elif request.POST.get(s.user.first_name + s.user.username) == 'absent':
                sa.date = str(request.POST.get('date'))
                sa.status = "absent"
            tchr = Teacher.objects.get(user=request.user)
            sa.marked_by = tchr
            sa.save()
            t = s.total_attendance
            t += 1
            s.total_attendance = t
            s.save()
        return HttpResponse("Attendance Marked")
    else:
        if request.session['user_type'] == 'teacher':
            students = Student.objects.filter(class_studying = current_teacher.class_teacher)
            user = Teacher.objects.get(user = request.user)
            return render(request, 'Aims/publish_attendance.html', {'type' : request.session['user_type'] , 'USER' : user, 'students' : students})
        else:
            return HttpResponseRedirect('/')




#views only for students -------------------------------------------------------
@login_required
def analytics_view(request):
    if request.session['user_type'] == 'student':
        return HttpResponse("Hello from analytics")
    else:
        return HttpResponseRedirect('/')

@login_required
def marks_view(request):
    if request.session['user_type'] == 'student':
        user = Student.objects.get(user = request.user)
        current_student = Student.objects.get(user = request.user)
        subjects = Subjects.objects.filter(taught_in_class = current_student.class_studying)
        return render(request, 'Aims/marks_view.html', {'type' : request.session['user_type'] , 'USER' : user, 'subjects' : subjects})
    else:
        return HttpResponseRedirect('/')

@login_required
def today_topics_view(request):
    if(request.session['user_type'] == 'student'):
        return HttpResponse("Topics Views")
    else:
        return HttpResponseRedirect('/')

@login_required
def explain_marks_view(request):
    if request.method == 'GET':
        user = request.user
        subject_name = request.GET.get('subject')
        student = Student.objects.get(user = request.user)
        sub = Subjects.objects.get(name = subject_name)
        marks = Marks.objects.filter(subject=sub, student=student)
        l = len(marks)
    return render(request, 'Aims/explain_marks.html', {'type' : request.session['user_type'], 'USER' : student, 'marks' : marks, 'length' : l})

@login_required
def fee_status_view(request):
    if request.session['user_type'] == 'student':
        user = request.user
        student = Student.objects.get(user = request.user)
        return render(request, 'Aims/fee_status.html', {'type' : request.session['user_type'], 'USER' : student, })
    else:
        return HttpResponseRedirect('/')
