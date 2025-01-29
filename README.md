## Описание проекта

Проект представляет собой веб-приложение для генерации случайных цитат на главной странице. Авторизованные пользователи могут не только просматривать цитаты, но и добавлять свои собственные. Для этого необходимо заполнить форму и отправить цитату на модерацию. Все предложенные цитаты получают статус "На рассмотрении", и после проверки модератором они могут быть либо отклонены, либо опубликованы.

Кроме того, пользователи могут сохранять понравившиеся им цитаты в своем профиле. Все сохраненные и предложенные цитаты отображаются в личном кабинете пользователя.

## Структура проекта

- `random_quote/` — папка с исходным кодом для генерации цитат.
- `requirements.txt` — файл с зависимостями проекта.
- `Dockerfile` — описание для контейнеризации проекта.
- `docker-compose.yaml` — файл для настройки контейнеров.
- `entrypoint.sh` — скрипт для запуска приложения.
- `.env_example` — пример конфигурационного файла для окружения.

## Установка


1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/ваш_пользователь/имя_репозитория.git
    cd имя_репозитория
    ```

2. Создайте и активируйте виртуальное окружение:

    ```bash
    python -m venv venv
    venv\Scripts\activate 
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

## Запуск

### Вариант 1: Запуск через Docker

Если у вас установлен Docker, вы можете запустить проект в контейнере:

1. Соберите Docker-образ:

    ```bash
    docker build -t random-quote-generator .
    ```

2. Запустите контейнер:

    ```bash
    docker-compose up
    ```

### Вариант 2: Запуск локально

Перейдите в папку random_quote и запустите приложение:

```bash
cd random_quote
python manage.py runserver