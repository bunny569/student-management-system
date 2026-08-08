from django.contrib import admin
from django.urls import path
from . import views

urlpatterns=[
    path('',views.landing,name="landing"),
    path('login/',views.loginview,name="login"),
    path('index',views.index,name="index"),
    path('addstudent/',views.addstudent,name="addstudent"),
    path('addteacher/',views.addteacher,name="addteacher"),
    path('studentlist/',views.student_list,name="studentlist"),
    path('teacherlist/',views.teacher_list,name="teacherlist"),
    path('editstudent/<int:pk>/',views.edit_student,name="editstudent"),
    path('editteacher/<int:pk>/',views.edit_teacher,name="editteacher"),
    path('deletestudent/<int:pk>/',views.delete_student,name="deletestudent"),
    path('deleteteacher/<int:pk>/',views.delete_teacher,name="deleteteacher"),
    path('dashboard/',views.studentdashboard,name="studentdashboard"),
    path('teacherdashboard/',views.teacherdashboard,name="teacherdashboard"),
    path('changepassword/',views.changepassword,name="changepassword"),
    path('attendence/',views.Attendence,name="attendence"),
    path('notice/',views.Notice,name="notice"),
    path('shownotice/',views.shownotice,name="shownotice"),
    path('course/',views.course,name="course"),
    path('deletecourse/<int:pk>/',views.delete_course,name="deletecourse"),
    path('logout/',views.logout_view,name="logout")




]