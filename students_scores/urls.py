from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_info/', views.get_info_page, name='get_info'),
    path('student_info/', views.student_info_page, name='student_info'),
    path('discipline_info/', views.discipline_info_page, name='discipline_info'),
    path('students_with_debts/', views.list_students_with_debts, name='students_with_debts'),
]
