from django.db import models
import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        now = datetime.datetime.now()
        if not email:
            raise ValueError('The given email address must be set')
        email = UserManager.normalize_email(email)
        user = self.model(email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.full_name = user.first_name + user.last_name
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=30)
    last_name = models.CharField('last name', max_length=30)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    is_email_verified = models.BooleanField('verified', default=False)
    county_choices = (
        ('Pakistan', 'Pakistan'),
        ('India', 'India'),
        ('Afghanistan', 'Afghanistan')
    )
    country = models.CharField(max_length=1000, choices=county_choices)
    postal_code = models.IntegerField(blank=True, null=True)
    user_type_choices = (

        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
    )
    user_type = models.CharField(max_length=50, choices=user_type_choices)
    USERNAME_FIELD = 'email'
    date_joined = models.DateTimeField(default=datetime.datetime.now())
    profile_pic = models.ImageField(upload_to="uploads", default="uploads/default_profile.jpg")


    objects = UserManager()

    def get_full_name(self):
        return u' '.join((self.first_name, self.last_name))

    def get_short_name(self):
        return u' '(self.first_name)


class student(models.Model):
    user_id = models.ForeignKey('User')
    School_University = models.CharField(max_length=300, blank=False, null=False)
    Age = models.CharField(max_length=10, default='18+')
    Date_of_Birth = models.CharField(max_length=50, blank=True, null=True)


class teacher(models.Model):
    user_id = models.ForeignKey('User')
    most_recent_job_title = models.CharField(max_length=1000)
    major_subjects = (
        ('', '-'),
        ('Accounting', 'Accounting'),
        ('Math', 'Math'),
    )

    subjects = models.CharField(choices=major_subjects, max_length=1000)


class course (models.Model):
    name = models.CharField(max_length=1000)
    code = models.CharField(max_length=15, unique=True)
    description = models.TextField(max_length=10000)
    taughtby = models.ForeignKey(User)
    coursepic = models.ImageField(upload_to="uploads", default="uploads/default_profile.jpg", null=True)


class assignment(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField()
    weightage = models.IntegerField(null=False)
    document = models.FileField(upload_to='uploads', null=True)


class course_assignment(models.Model):
    course_id = models.ForeignKey('course')
    assignment_id = models.ForeignKey('assignment')


class course_student(models.Model):
    course_id = models.ForeignKey('course')
    student_id = models.ForeignKey('User')


class assignment_submission(models.Model):
    assignment_id = models.ForeignKey('assignment')
    student_id = models.ForeignKey('User')
    submission_file = models.FileField(upload_to='uploads', null=False)
    marks = models.IntegerField(blank=True, null=True)


class questionsession (models.Model):
    askedby = models.ForeignKey('User',related_name='askedby')
    askedfrom = models.ForeignKey('User',related_name='askedfrom')
    ratingofstudent = models.IntegerField(blank=True, null=True)
    ratingofteacher = models.IntegerField(blank=True, null=True)
    firstmessage = models.TextField()

class message (models.Model):
    askedby = models.ForeignKey('User', related_name='askedby1')
    askedfrom = models.ForeignKey('User', related_name='askedfrom1')
    mess = models.TextField()

class questionsmessages (models.Model):
    question_id = models.ForeignKey('questionsession')
    message_id = models.ForeignKey('message')


class notes(models.Model):
    which_course = models.ForeignKey('course')
    noteFile = models.FileField(upload_to='uploads')


class quizz(models.Model):
    weightage = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=1000)
    belongs_to = models.ForeignKey('course')

class MCQ (models.Model):
    quizz_id = models.ForeignKey('quizz')
    question = models.CharField(max_length=1000)
    option1 = models.CharField(max_length=1000)
    option2 = models.CharField(max_length=1000)
    option3 = models.CharField(max_length=1000)
    option4 = models.CharField(max_length=1000)
    correct_answer = models.IntegerField(blank=True, null=True)
    user_answer = models.IntegerField(blank=True, null=True)


class marked_quiz(models.Model):
    marks = models.IntegerField(blank=True, null=True)
    of_whom = models.ForeignKey('User')
    quizid = models.ForeignKey('quizz')

