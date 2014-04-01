from django.contrib import admin

from application.models import User,course, assignment, course_assignment, assignment_submission, teacher, questionsession,message,questionsmessages

admin.site.register(User)
admin.site.register(course)
admin.site.register(assignment)
admin.site.register(course_assignment)
admin.site.register(assignment_submission)
admin.site.register(teacher)

admin.site.register(questionsession)
admin.site.register(questionsmessages)
admin.site.register(message)