from django.test import TestCase, Client
from students_scores.views import StatsCalculator, StudentStats, DisciplineStats
from students_scores.views import RequestHandlerFactory, StudentInfoHandler, DisciplineInfoHandler
from unittest.mock import patch, MagicMock
import numpy as np
from students_scores.models import Student
from django.urls import reverse
from django.http import HttpResponse
from students_scores.views import get_students_with_academic_debts, StudentWithDebts, update_students_with_debts


class StatsCalculatorTest(TestCase):
    def setUp(self):
        self.scores = [50, 70, 80, 90, 100]
        self.stats_calculator = StatsCalculator()

    # Проверка метода calculate_stats класса StatsCalculator с использованием unittest.mock для
    # замены функций numpy на моки.
    # Проверка того, что метод возвращает правильные значения и что функции numpy вызываются с правильными аргументами.
    @patch('numpy.max')
    @patch('numpy.min')
    @patch('numpy.mean')
    @patch('numpy.std')
    @patch('numpy.var')
    def test_calculate_stats(self, mock_var, mock_std, mock_mean, mock_min, mock_max):
        mock_max.return_value = 100
        mock_min.return_value = 50
        mock_mean.return_value = 78.0
        mock_std.return_value = 15.811388300841896
        mock_var.return_value = 250.0

        result = self.stats_calculator.calculate_stats(self.scores)

        mock_max.assert_called_once_with(self.scores)
        mock_min.assert_called_once_with(self.scores)
        mock_mean.assert_called_once_with(self.scores)
        mock_std.assert_called_once_with(self.scores)
        mock_var.assert_called_once_with(self.scores)

        expected_result = [5, 100, 50, 78.0, 15.811388300841896, 250.0]
        self.assertEqual(result, expected_result)


class StudentStatsTest(TestCase):
    def setUp(self):
        self.student1 = Student.objects.create(name="Бочкин Иван", discipline="Высшая математика", score=85)
        self.student2 = Student.objects.create(name="Бочкин Иван", discipline="Информатика", score=90)
        self.student3 = Student.objects.create(name="Бочкин Иван", discipline="Физика", score=78)
        self.stats_calculator = StatsCalculator()
        self.student_stats = StudentStats(name="Бочкин Иван", stats_calculator=self.stats_calculator)

    # Проверка метода calculate_student_stats класса StudentStats.
    # Используются моки для функций numpy и проверяется то, что метод возвращает правильные значения и что
    # функции numpy вызываются с правильными аргументами.
    @patch('numpy.max')
    @patch('numpy.min')
    @patch('numpy.mean')
    @patch('numpy.std')
    @patch('numpy.var')
    def test_calculate_student_stats(self, mock_var, mock_std, mock_mean, mock_min, mock_max):
        mock_max.return_value = 90
        mock_min.return_value = 78
        mock_mean.return_value = 84.33333333333333
        mock_std.return_value = 5.163977794943222
        mock_var.return_value = 26.666666666666668

        stats = self.student_stats.calculate_student_stats()

        self.assertEqual(stats, [3, 90, 78, 84.33333333333333, 5.163977794943222, 26.666666666666668])
        mock_max.assert_called_once_with([85, 90, 78])
        mock_min.assert_called_once_with([85, 90, 78])
        mock_mean.assert_called_once_with([85, 90, 78])
        mock_std.assert_called_once_with([85, 90, 78])
        mock_var.assert_called_once_with([85, 90, 78])


class DisciplineStatsTest(TestCase):
    def setUp(self):
        self.student1 = Student.objects.create(name="Бочкин Иван", discipline="Высшая математика", score=85)
        self.student2 = Student.objects.create(name="Сидоров Сергей", discipline="Высшая математика", score=90)
        self.student3 = Student.objects.create(name="Петров Иван", discipline="Высшая математика", score=78)
        self.stats_calculator = StatsCalculator()
        self.discipline_stats = DisciplineStats(discipline_name="Высшая математика",
                                                stats_calculator=self.stats_calculator)

    # Проверка метода calculate_discipline_stats класса DisciplineStats.
    # Используются моки для функций numpy и проверяется то, что метод возвращает правильные значения и что
    # функции numpy вызываются с правильными аргументами.
    @patch('numpy.max')
    @patch('numpy.min')
    @patch('numpy.mean')
    @patch('numpy.std')
    @patch('numpy.var')
    def test_calculate_discipline_stats(self, mock_var, mock_std, mock_mean, mock_min, mock_max):
        mock_max.return_value = 90
        mock_min.return_value = 78
        mock_mean.return_value = 84.33333333333333
        mock_std.return_value = 5.163977794943222
        mock_var.return_value = 26.666666666666668

        stats = self.discipline_stats.calculate_discipline_stats()

        self.assertEqual(stats, [3, 90, 78, 84.33333333333333, 5.163977794943222, 26.666666666666668])
        mock_max.assert_called_once_with([85, 90, 78])
        mock_min.assert_called_once_with([85, 90, 78])
        mock_mean.assert_called_once_with([85, 90, 78])
        mock_std.assert_called_once_with([85, 90, 78])
        mock_var.assert_called_once_with([85, 90, 78])


# --------------------------------------------------------


class RequestHandlerTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_student_info_page(self):
        response = self.client.post(reverse('student_info'), {'student': 'Петров Иван'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Петров Иван')

    def test_discipline_info_page(self):
        response = self.client.post(reverse('discipline_info'), {'discipline': 'Высшая математика'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Высшая математика')


class StudentInfoHandlerTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(name='Петров Андрей', discipline='Высшая математика', score=85)

    def test_handle_request_student_exists(self):
        response = self.client.post(reverse('student_info'), {'student': 'Петров Андрей'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Петров Андрей')
        self.assertTemplateUsed(response, 'students_scores/student_form.html')

    def test_handle_request_student_not_exists(self):
        response = self.client.post(reverse('student_info'), {'student': 'Не существующий'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Не существующий - такого студента нет!')


class DisciplineInfoHandlerTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(name='Петров Иван', discipline='Информатика', score=85)

    def test_handle_request_discipline_exists(self):
        response = self.client.post(reverse('discipline_info'), {'discipline': 'Информатика'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Информатика')
        self.assertTemplateUsed(response, 'students_scores/discipline_form.html')

    def test_handle_request_discipline_not_exists(self):
        response = self.client.post(reverse('discipline_info'), {'discipline': 'Не существующая'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Не существующая - такой дисциплины нет!')


# --------------------------------------------------------


class StudentViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Создаем тестовые объекты модели Student
        self.student1 = Student.objects.create(name='Сусарев Евгений', discipline='Тестирование и оценка кач-ва ПО', score=85)
        self.student2 = Student.objects.create(name='Федотова Елена', discipline='Теория вероятности', score=58)
        self.student3 = Student.objects.create(name='Королёв Егор', discipline='Методы оптимизации', score=72)
        self.student4 = Student.objects.create(name='Кузьминов Михаил', discipline='Параллельные и распределенные вычисления', score=55)

    def test_index_view(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Сусарев Евгений')
        self.assertContains(response, 'Федотова Елена')
        self.assertContains(response, 'Королёв Егор')
        self.assertContains(response, 'Кузьминов Михаил')
        self.assertTemplateUsed(response, 'students_scores/index.html')

    def test_get_info_page_view(self):
        response = self.client.get(reverse('get_info'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students_scores/get_info.html')

    def test_list_students_with_debts_view(self):
        # Обновляем список студентов с долгами перед тестом
        response = self.client.get(reverse('students_with_debts'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Федотова Елена')
        self.assertContains(response, 'Кузьминов Михаил')
        self.assertNotContains(response, 'Сусарев Евгений')
        self.assertNotContains(response, 'Королёв Егор')
        self.assertTemplateUsed(response, 'students_scores/students_with_debts.html')

        # Проверяем, что студенты добавлены в модель StudentWithDebts
        students_with_debts = StudentWithDebts.objects.all()
        self.assertEqual(students_with_debts.count(), 2)
        self.assertIn('Федотова Елена', [student.name for student in students_with_debts])
        self.assertIn('Кузьминов Михаил', [student.name for student in students_with_debts])

    def test_update_students_with_debts(self):
        # Вызываем функцию для обновления студентов с долгами
        update_students_with_debts()

        # Проверяем, что студенты добавлены в модель StudentWithDebts
        students_with_debts = StudentWithDebts.objects.all()
        self.assertEqual(students_with_debts.count(), 2)
        self.assertIn('Федотова Елена', [student.name for student in students_with_debts])
        self.assertIn('Кузьминов Михаил', [student.name for student in students_with_debts])

    def test_get_students_with_academic_debts(self):
        # Вызываем функцию для получения студентов с долгами
        students_with_debts = get_students_with_academic_debts()

        self.assertEqual(students_with_debts.count(), 2)
        self.assertIn('Федотова Елена', [student.name for student in students_with_debts])
        self.assertIn('Кузьминов Михаил', [student.name for student in students_with_debts])
