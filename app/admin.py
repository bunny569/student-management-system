from django.contrib import admin
from .models import Course,Student,Teacher,attendence,notice

# Register your models here.
admin.site.register(Course)
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display=["name","roll_number","age","course"]
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display=["name","teacher_id","department"]
admin.site.register(attendence)
admin.site.register(notice)