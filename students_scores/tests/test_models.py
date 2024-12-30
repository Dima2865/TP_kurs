from django.test import TestCase
from students_scores.models import Student, StudentWithDebts
from django.db import IntegrityError
from unittest.mock import patch, MagicMock


class StudentModelTest(TestCase):
    # Проверка на корректность создания новой записи
    def test_create_student(self):
        student = Student.objects.create(
            name="Бочкин Иван",
            discipline="Высшая математика",
            score=95
        )
        self.assertEqual(student.name, "Бочкин Иван")
        self.assertEqual(student.discipline, "Высшая математика")
        self.assertEqual(student.score, 95)

    # Проверяет то, что метод save был вызван с использованием unittest.mock.patch
    @patch('django.db.models.Model.save', MagicMock(name='save'))
    def test_save_method_called(self):
        student = Student(
            name="Бочкин Иван",
            discipline="Высшая математика",
            score=95
        )
        student.save()
        self.assertTrue(student.save.called)


class StudentWithDebtsModelTest(TestCase):
    # Проверка на корректность создания новой записи
    def test_create_student_with_debts(self):
        student_with_debts = StudentWithDebts.objects.create(
            name="Сидоров Сергей",
            discipline="Физика",
            score=50
        )
        self.assertEqual(student_with_debts.name, "Сидоров Сергей")
        self.assertEqual(student_with_debts.discipline, "Физика")
        self.assertEqual(student_with_debts.score, 50)

    # Проверка на то, что ограничение unique_together работает правильно и выдает IntegrityError,
    # если попытаться создать объект с повторяющимися значениями полей name и discipline.
    def test_unique_together_constraint(self):
        StudentWithDebts.objects.create(
            name="Сидоров Сергей",
            discipline="Физика",
            score=50
        )
        with self.assertRaises(IntegrityError):
            StudentWithDebts.objects.create(
                name="Сидоров Сергей",
                discipline="Физика",
                score=45
            )

    # Проверяет то, что метод save был вызван с использованием unittest.mock.patch
    @patch('django.db.models.Model.save', MagicMock(name='save'))
    def test_save_method_called(self):
        student_with_debts = StudentWithDebts(
            name="Сидоров Сергей",
            discipline="Физика",
            score=50
        )
        student_with_debts.save()
        self.assertTrue(student_with_debts.save.called)
