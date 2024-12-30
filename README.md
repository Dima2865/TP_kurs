# Курсовая работа по дисциплине "Технологии программирования"

$env:PYTHONPATH = "ps_password"
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata students_scores.yaml
python manage.py runserver

python manage.py test students_scores/tests/

create database django_kurs_db owner postgres;