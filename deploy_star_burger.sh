#!/bin/bash
set -e

echo "Обновление кода"
git pull
echo "Код репозитория обновлён!"

echo "Установка библиотек python"
./venv/bin/pip3 install -r requirements.txt
echo "Библиотеки python установлены"

echo "Установка библиотек node.js"
npm ci --dev
echo "Библиотеки Node.js установлены"

echo "Сборка JS"
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
echo "Сборка JS завершена"

echo "Сборка статики django"
./venv/bin/python3 manage.py collectstatic --noinput
echo  "Статика пересобрана"

echo "Миграции БД"
./venv/bin/python3 manage.py migrate --noinput
echo  "Миграции БД завершены"

echo "Перезапуск службы сайта"
sudo systemctl restart starburger.service
echo  "Служба сайта перезапущена"

echo "Перезапуск nginx"
sudo systemctl reload nginx.service
echo  "Nginx перезапущен"

echo "Деплой завершен"
