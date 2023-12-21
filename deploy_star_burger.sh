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

echo "Регистрация deploy в сервисе Rollbar"
commit_hash=$(git rev-parse HEAD)
source .env
export ROLLBAR_TOKEN

curl --http1.1 -X POST \
  https://api.rollbar.com/api/1/deploy \
  -H "X-Rollbar-Access-Token: $ROLLBAR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"environment": "production", "revision": "'"$commit_hash"'", "local_username": "'"$USER"'", "comment": "Deployed new version", "status": "succeeded"}'

echo "Деплой завершен"
