from django import forms
from application.models import User, course
from django.utils.safestring import mark_safe
from application.models import teacher, student
from django.core.validators import EmailValidator



class UserCreationForm(forms.ModelForm):
    error_messages = {
        'duplicate_email': 'The email address, you have entered , is already registered. Already on LinkedIn? <a href="/sign-in/">Sign In</a>',
    }
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password")

    def clean_email(self):
        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(mark_safe(self.error_messages['duplicate_email']))

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user




class UserCreationForm2(forms.Form):
    country = forms.ChoiceField(choices=User.county_choices, widget=forms.Select())
    postal_code = forms.IntegerField(required=False)
    user_type = forms.ChoiceField(choices=User.user_type_choices, widget=forms.RadioSelect(), initial=User.user_type_choices[0][0])
    job_title = forms.CharField(max_length=1000, required=False)
    most_recent_job_title = forms.CharField(max_length=1000, required=False)
    subjects = forms.ChoiceField(choices=teacher.major_subjects, widget=forms.Select(), required=False)
    institution = forms.CharField(max_length=2000, required=False)

    def clean_institution(self):
        user_type = self.cleaned_data['user_type']
        if user_type == "Student":
            institution = self.cleaned_data['institution']
            if institution == "":
                raise forms.ValidationError("This is required field")
            else:
                return institution


    def clean_job_title(self):
        user_type = self.cleaned_data['user_type']
        if user_type == "Employed":
            job_title = self.cleaned_data['job_title']
            if job_title == "":
                raise forms.ValidationError("This is required field")
            else:
                return job_title


    def clean_most_recent_job_title(self):
        user_type = self.cleaned_data['user_type']
        if user_type == "Teacher":
            most_recent_job_title = self.cleaned_data['most_recent_job_title']
            if most_recent_job_title == "":
                raise forms.ValidationError("This is required field")
            else:
                return most_recent_job_title

    def save(self, User):
        User.country = self.cleaned_data['country']
        User.postal_code = self.cleaned_data['postal_code']
        User.user_type = self.cleaned_data['user_type']
        User.save()

        if User.user_type == "Teacher":
            teacher_instance = teacher()
            teacher_instance.most_recent_job_title = self.cleaned_data['most_recent_job_title']
            teacher_instance.subjects = self.cleaned_data['subjects']
            teacher_instance.user_id = User
            teacher_instance.save()

        elif User.user_type == "Student":
            student_instance = student()
            student_instance.user_id = User
            student_instance.School_University = self.cleaned_data['institution']
            student_instance.save()


class LoginForm(forms.Form):
    username = forms.EmailField(max_length=150, validators=[EmailValidator])
    password = forms.CharField(min_length=6, widget=forms.PasswordInput())


class add_course(forms.Form):
    error_messages = {
        'duplicate_code': 'Code is already taken try another one'
    }
    name = forms.CharField(max_length=1000)
    code = forms.CharField(max_length=15)
    description = forms.CharField(widget=forms.Textarea)
    coursepic = forms.ImageField(required=False)

    def clean_code(self):
        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        code = self.cleaned_data["code"]
        try:
            course._default_manager.get(code=code)
        except course.DoesNotExist:
            return code
        raise forms.ValidationError(mark_safe(self.error_messages['duplicate_code']))


class add_assignment(forms.Form):
    title = forms.CharField(max_length=1000)
    description = forms.CharField(widget=forms.Textarea)
    weightage = forms.IntegerField(required=True)
    file = forms.FileField(required=False)
