from django.shortcuts import render,redirect
from .models import Student,Teacher,attendence,notice,Course
from .forms import Studentform,Teacherform,ChangePasswordform,attendenceform,noticeform,courseform
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User,Group
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,"index.html")
def student_list(request):
    students=Student.objects.all()
    return render(request,'student_list.html',{"students":students})
def teacher_list(request):
    teachers=Teacher.objects.all()
    return render(request,'teacher_list.html',{"teachers":teachers})
@login_required
def addstudent(request):
    if not request.user.is_superuser:
        return HttpResponse("you don't have permission")
    if request.method == "POST":
        form = Studentform(request.POST)
        if form.is_valid():
            student = form.save(commit=False)

            user = User.objects.create_user(
                username=student.roll_number,
                password="college123"
            )

            student.user = user
            student.save()

            student_group = Group.objects.get(name="Student")
            user.groups.add(student_group)
            messages.success(request, "Student added successfully.")
            return redirect("index")

    else:
        form = Studentform()


    return render(request, "addstudent.html", {"form": form})
@login_required
def addteacher(request):
    if request.method=="POST":
        form=Teacherform(request.POST)
        if form.is_valid():
            teacher=form.save(commit=False)
            user=User.objects.create_user(
                username=teacher.teacher_id,
                password="college123"
            )
            teacher.user=user
            teacher.save()
            teacher_group= Group.objects.get(name="Teacher")
            user.groups.add(teacher_group)
            messages.success(request, "Teacher added successfully.")
            return redirect("index")
    else:
        form= Teacherform()
    return render(request,'addteacher.html',{"form":form})
@login_required
def edit_student(request,pk):
    student=get_object_or_404(Student,pk=pk)
    if request.method == "POST":
            form = Studentform(request.POST, instance=student)
            if form.is_valid():
                form.save()
                messages.success(request, "Student updated successfully.")
                return redirect("index")
    else:
            form = Studentform(instance=student)
    
    return render(request, "addstudent.html", {"form": form})
@login_required
def edit_teacher(request,pk):
    teacher=get_object_or_404(Teacher,pk=pk)
    if request.method=="POST":
         form=Teacherform(request.POST, instance=teacher)
         if form.is_valid():
            form.save()
            messages.success(request, "Teacher updated successfully.")
            return redirect("teacherlist")
    else:
         form=Teacherform(instance=teacher)
    return render(request,"addteacher.html",{"form":form})
@login_required
def delete_student(request,pk):
    student=get_object_or_404(Student,pk=pk)
    if request.method=="POST":
        if student.user:
            student.user.delete()
        else:
         student.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect("studentlist")
    return render(request, "delete_student.html", {"student": student})
@login_required
def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    if request.method == "POST":
        teacher.user.delete()
        messages.success(request, "Teacher deleted successfully.")
        return redirect("teacherlist")

    return render(request, "deleteteacher.html", {
        "teacher": teacher
    })



def loginview(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect("index")
            elif user.groups.filter(name="Student").exists():
                return redirect("studentdashboard")
            elif user.groups.filter(name="Teacher").exists():
                return redirect("teacherdashboard")

            return redirect("index")
        else:
            messages.error(request, "Invalid username or password.")



    return render(request, "login.html")
def studentdashboard(request,):
    student=Student.objects.get(user=request.user)
    presentcount=attendence.objects.filter(student=student,status="Present").count()
    absentcount=attendence.objects.filter(student=student,status="Absent").count()
    total=presentcount+absentcount
    if total>0:
     percentage=(presentcount/(presentcount+absentcount))*100
    else:
        percentage=0
    return render(request,"studentdashboard.html",{"student":student,
     "presentcount":presentcount,
     "absentcount":absentcount,
     "percentage":percentage})

def teacherdashboard(request):
    teacher=Teacher.objects.get(user=request.user)
    studentcount=attendence.objects.filter(date=timezone.now().date(), status="Present").count()
    return render(request,"teacherdashboard.html",{"teacher":teacher,
    "studentcount":studentcount})
def logout_view(request):
    logout(request)
    return redirect("landing")
def changepassword(request):
    if request.method=="POST":
        form=ChangePasswordform(request.POST)
        if form.is_valid():
          password=form.cleaned_data["password"]
          conformpassword=form.cleaned_data["conformpassword"]
          if password == conformpassword:
            request.user.set_password(password)
            request.user.save()
            messages.success(request, "Password Changed Successfully.")
            return redirect("login")
          else:
              return HttpResponse("Password Missmathc")
    else:
        form=ChangePasswordform()        
    return render(request,"changepassword.html",{"form":form})
from django.utils import timezone
from django.contrib import messages

def Attendence(request):
    students = Student.objects.all()

    if request.method == "POST":
        for student in students:
            status = request.POST.get(f"attendance_{student.id}")

            if status:
                attendence.objects.update_or_create(
                    student=student,
                    date=timezone.localdate(),
                    defaults={
                        "course": student.course,
                        "status": status
                    }
                )

        messages.success(request, "Attendance submitted successfully.")
        return redirect("index")

    return render(request, "addtendence.html", {
        "students": students
    })

def landing(request):
    return render(request,"landing.html")
def Notice(request):
    notices = notice.objects.all().order_by("-date")

    if request.method == "POST":
        form = noticeform(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Notice added successfully.")
            return redirect("notice")
    else:
        form = noticeform()

    if request.user.is_superuser:
        template = "base.html"
    else:
        template = "base3.html"

    return render(request, "notice.html", {
        "form": form,
        "notices": notices,
        "base_template": template
    })
def shownotice(request):
    notices=notice.objects.all().order_by("-date")
    return render(request,"shownotice.html",{"notices":notices})
def course(request):
    form=courseform()
    courses=Course.objects.all()
    if request.method=="POST":
        form=courseform(request.POST)
        if form.is_valid():
           form.save()
           messages.success(request, "Course added successfully.")
           return redirect("course")
        
    return render(request,"course.html",{"form":form,
                                         "courses":courses})
def delete_course(request,pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        course.delete()
        messages.success(request, "Course deleted successfully.")
        return redirect("course")

    return render(request, "deletecourse.html", {"course": course})