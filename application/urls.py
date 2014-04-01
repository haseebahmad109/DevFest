from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'application.views.home'),
    url(r'^dashboard$', 'application.views.dashboard'),
    url(r'^signin$', 'application.views.sign_in'),
    url(r'^signup$', 'application.views.signup'),
    url(r'^signup2$', 'application.views.signup2'),
    url(r'^logout$', 'application.views.user_logout'),
    url(r'^addcourse$', 'application.views.add_course_view'),
    url(r'^courses$', 'application.views.courses'),
    url(r'^course/(?P<id>\d+)/$', 'application.views._course'),
    url(r'^add_assignment$', 'application.views.add_assignment_view'),
    url(r'^submit_assignment$', 'application.views.submit_assignment_view'),
    url(r'^register_course$', 'application.views.register_course_view'),
    url(r'^teachers$', 'application.views.view_teachers'),
    url(r'^askquestion$', 'application.views.ask_question_view'),
    url(r'^replyquestion$', 'application.views.reply_question_view'),
    url(r'^mail_box$','application.views.mail_box_view'),
    url(r'^messageview$', 'application.views.show_messageview'),
    url(r'^rate$', 'application.views.rate_the_question'),
    url(r'^markassignment$', 'application.views.mark_assignment'),
    url(r'^search_course$', 'application.views.courses_search_view'),
    url(r'^upload_notes$', 'application.views.upload_notes'),
    url(r'^search_teachers$', 'application.views.search_teachers_view'),
    url(r'^add_quiz', 'application.views.create_Quiz'),
    url(r'^quiz/(?P<id>\d+)/', 'application.views.take_quiz')
)

urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)