from django import forms
from .models import Student,Teacher,attendence,notice,Course
from django.contrib.auth.models import User

class Studentform(forms.ModelForm):
    class Meta:
      model=Student
      fields='__all__'
      exclude=["user"]
      widgets = {
            "date_of_birth": forms.DateInput(
                attrs={"type": "date"}
            ),
            "admissiom_date": forms.DateInput(
                attrs={"type": "date"}
            ),
        }

class Teacherform(forms.ModelForm):
   class Meta:
      model=Teacher
      fields='__all__'
      exclude=["user"]
      widgets = {
                  "date_of_joining": forms.DateInput(
                      attrs={"type": "date"}
                  ),
              }
      
class ChangePasswordform(forms.Form):
   password=forms.CharField(
      widget=forms.PasswordInput()
   )
   conformpassword=forms.CharField(
      widget=forms.PasswordInput()
   )

class attendenceform(forms.ModelForm):
   class Meta:
      model=attendence
      fields="__all__"

class noticeform(forms.ModelForm):
   class Meta:
      model=notice
      fields="__all__"
      exclude=["date"]
class courseform(forms.ModelForm):
   class Meta:
      model=Course
      fields=["course"]


   
