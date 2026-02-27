#!/usr/bin/env bash
# Қате шықса бірден тоқтату үшін
set -o errexit

# Библиотекаларды орнату
pip install -r requirements.txt

# Статикалық файлдарды жинау
python manage.py collectstatic --no-input

# Базаны жаңарту (Миграция)
python manage.py migrate
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
  python manage.py createsuperuser \
    --noinput \
    --username $DJANGO_SUPERUSER_USERNAME \
    --email $DJANGO_SUPERUSER_EMAIL || true
fi