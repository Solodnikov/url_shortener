# UrlShortener

![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

### Описание проекта
Приложение для укорачивания ссылок. Позволяет ассоциировать длинную пользовательскую ссылку с короткой, которую предоставляет приложение или предлогает сам пользователь. Реализует переадресацию на исходный адрес при обращении к коротким ссылкам.

### Развертывание проекта

* клонируйте проект

   `https://github.com/Solodnikov/url_shortener.git`

* установите и запустите виртуальное окружение в папке проекта

    `python -m venv venv`

    `. venv/Scripts/activate`

* установите зависимости проекта

    `pip install -r requirements.txt`

### Запуск проекта

* создайте файл `.env` в корневой директории проекта:
    
    ```
    # .env example
    FLASK_APP=cut
    FLASK_ENV=development
    DATABASE_URI=sqlite:///db.sqlite3
    SECRET_KEY=1234test4321
    ```
* ввести комманду в корневой директории проекта

    `flask run`

* cервис будет доступен по адресу

    `http://127.0.0.1:5000/`
