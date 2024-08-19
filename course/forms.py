from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Lesson, Course, User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=False, max_length=30)
    last_name = forms.CharField(required=False, max_length=30)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ("name", "description")


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ("title", "content")


class CourseSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by course name",
                "class": "form-control search-input",
            }
        )
    )
