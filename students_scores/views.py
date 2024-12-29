from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
import numpy as np
from .models import Student
from typing import List
from abc import ABC, abstractmethod


# Паттерн Strategy (start)
class StatsCalculator:
    def calculate_stats(self, scores: List[int]) -> List[float]:
        stud_count = len(scores)
        # Вычисляем максимальную, минимальную и среднюю оценку по дисциплинам
        max_score = np.max(scores)
        min_score = np.min(scores)
        avg_score = np.mean(scores)
        # Вычисляем стандартное отклонение баллов
        std_dev = np.std(scores)
        # Вычисляем дисперсию баллов
        variance = np.var(scores)
        return [stud_count, max_score, min_score, avg_score, std_dev, variance]


class StudentStats:
    def __init__(self, name: str, stats_calculator: StatsCalculator):
        self.name = name
        self.stats_calculator = stats_calculator

    def calculate_student_stats(self) -> List[float]:
        # Извлекаем оценки из QuerySet
        student_info = Student.objects.filter(name=self.name).values()
        scores = [entry['score'] for entry in student_info]
        return self.stats_calculator.calculate_stats(scores)


class DisciplineStats:
    def __init__(self, discipline_name: str, stats_calculator: StatsCalculator):
        self.discipline_name = discipline_name
        self.stats_calculator = stats_calculator

    def calculate_discipline_stats(self) -> List[float]:
        # Извлекаем оценки из QuerySet
        discipline_info = Student.objects.filter(discipline=self.discipline_name).values()
        scores = [entry['score'] for entry in discipline_info]
        return self.stats_calculator.calculate_stats(scores)

# Паттерн Strategy (end)


# class StudentStats:
#     def __init__(self, name):
#         self.name = name
#
#     def calculate_student_stats(self):
#         # Извлекаем оценки из QuerySet
#         student_info = Student.objects.filter(name=self.name).values()
#         scores = [entry['score'] for entry in student_info]
#
#         stud_count = len(scores)
#         # Вычисляем максимальную, минимальную и среднюю оценку по дисциплинам
#         max_score = np.max(scores)
#         min_score = np.min(scores)
#         avg_score = np.mean(scores)
#         # Вычисляем стандартное отклонение баллов
#         std_dev = np.std(scores)
#         # Вычисляем дисперсию баллов
#         variance = np.var(scores)
#
#         return [stud_count, max_score, min_score, avg_score, std_dev, variance]
#
#
# class DisciplineStats:
#     def __init__(self, discipline_name):
#         self.discipline_name = discipline_name
#
#     def calculate_discipline_stats(self):
#         # Извлекаем оценки из QuerySet
#         discipline_info = Student.objects.filter(discipline=self.discipline_name).values()
#         scores = [entry['score'] for entry in discipline_info]
#
#         disc_count = len(scores)
#         # Вычисляем максимальную, минимальную и среднюю оценку студентов по данной дисциплине
#         max_score = np.max(scores)
#         min_score = np.min(scores)
#         avg_score = np.mean(scores)
#         # Вычисляем стандартное отклонение баллов
#         std_dev = np.std(scores)
#         # Вычисляем дисперсию баллов
#         variance = np.var(scores)
#
#         return [disc_count, max_score, min_score, avg_score, std_dev, variance]


# Паттерн Factory Method (start)
class RequestHandler(ABC):
    @abstractmethod
    def handle_request(self, request):
        pass

    def get_input(self, request, field_name):
        if request.method == 'POST':
            return str(request.POST.get(field_name))
        return "not a POST request"

    def render_template(self, request, template, context):
        return render(request, template, context)

    def render_error(self, request, message, link):
        return HttpResponse(f'<h3>{message}</h3><br><a href="{link}">Вернуться назад</a>')


class StudentInfoHandler(RequestHandler):
    def handle_request(self, request):
        student_name = self.get_input(request, "student")

        if Student.objects.filter(name=student_name).exists():
            student_info = Student.objects.filter(name=student_name)

            stats_calculator = StatsCalculator()
            student = StudentStats(student_name, stats_calculator=stats_calculator)
            stud_stats = student.calculate_student_stats()

            context = {'student_info': student_info, 'student_name': student_name, 'stud_stats': stud_stats}
            return self.render_template(request, 'students_scores/student_form.html', context)
        else:
            link = reverse('get_info')
            return self.render_error(request, f'{student_name} - такого студента нет!', link)


class DisciplineInfoHandler(RequestHandler):
    def handle_request(self, request):
        discipline_name = self.get_input(request, "discipline")

        if Student.objects.filter(discipline=discipline_name).exists():
            discipline_info = Student.objects.filter(discipline=discipline_name)

            stats_calculator = StatsCalculator()
            discipline = DisciplineStats(discipline_name, stats_calculator=stats_calculator)
            disc_stats = discipline.calculate_discipline_stats()

            context = {'discipline_info': discipline_info, 'discipline_name': discipline_name, 'disc_stats': disc_stats}
            return self.render_template(request, 'students_scores/discipline_form.html', context)
        else:
            link = reverse('get_info')
            return self.render_error(request, f'{discipline_name} - такой дисциплины нет!', link)


class RequestHandlerFactory:
    @staticmethod
    def create_handler(request_type):
        if request_type == 'student':
            return StudentInfoHandler()
        elif request_type == 'discipline':
            return DisciplineInfoHandler()
        else:
            raise ValueError("Unknown request type")


def student_info_page(request):
    handler = RequestHandlerFactory.create_handler('student')
    return handler.handle_request(request)


def discipline_info_page(request):
    handler = RequestHandlerFactory.create_handler('discipline')
    return handler.handle_request(request)

# Паттерн Factory Method (end)


# def student_info_page(request):
#     # Получаем имя студента из поля ввода
#     if request.method == 'POST':
#         student_name = str(request.POST.get("student"))
#     else:
#         student_name = "not a POST request"
#
#     # Проверка на то, существует ли такой студент в БД
#     if Student.objects.filter(name=student_name).exists():
#         # Получаем список дисциплин и оценок студента
#         student_info = Student.objects.filter(name=student_name)
#
#         # Вычисляем статистику студента по дисциплинам
#         stats_calculator = StatsCalculator()
#         student = StudentStats(student_name, stats_calculator=stats_calculator)
#         stud_stats = student.calculate_student_stats()
#
#         context = {'student_info': student_info, 'student_name': student_name, 'stud_stats': stud_stats}
#         return render(request, 'students_scores/student_form.html', context)
#     else:
#         link = reverse('get_info')
#         return HttpResponse(f'<h3>{student_name} - такого студента нет!</h3>'
#                             f'<br><a href="{link}">Вернуться назад</a>')
#
#
# def discipline_info_page(request):
#     # Получаем название дисциплины
#     if request.method == 'POST':
#         discipline_name = str(request.POST.get("discipline"))
#     else:
#         discipline_name = "not a POST request"
#
#     # Проверка на то, что такая дисциплина существует
#     if Student.objects.filter(discipline=discipline_name).exists():
#         # Получаем список студентов и их даллов по этой дисциплине
#         discipline_info = Student.objects.filter(discipline=discipline_name)
#
#         # Вычисляем статистику по дисциплине
#         stats_calculator = StatsCalculator()
#         discipline = DisciplineStats(discipline_name, stats_calculator=stats_calculator)
#         disc_stats = discipline.calculate_discipline_stats()
#
#         context = {'discipline_info': discipline_info, 'discipline_name': discipline_name, 'disc_stats': disc_stats}
#         return render(request, 'students_scores/discipline_form.html', context)
#     else:
#         link = reverse('get_info')
#         return HttpResponse(f'<h3>{discipline_name} - такой дисциплины нет!</h3>'
#                             f'<br><a href="{link}">Вернуться назад</a>')


def index(request):
    students = Student.objects.all()
    context = {'students': students}
    return render(request, 'students_scores/index.html', context)


def get_info_page(request):
    return render(request, 'students_scores/get_info.html')


def get_students_with_academic_debts():
    # Получаем студентов с оценкой ниже 61
    students_with_debts = Student.objects.filter(score__lt=61)
    return students_with_debts


def list_students_with_debts(request):
    students = get_students_with_academic_debts()
    return render(request, 'students_scores/students_with_debts.html', {'students': students})
