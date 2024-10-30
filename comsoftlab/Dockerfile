FROM python:3.9.20-slim

ENV PYTHONDONTWRITECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /django_app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /django_app/

CMD python manage.py makemigrations \
    && python manage.py migrate \
    && python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@admin.com', 'admin');"  \
    && python manage.py collectstatic --noinput \
    && python manage.py runserver 0.0.0.0:8000