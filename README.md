# CreditAppAPI

### Описание:
   Решение задания тестового [задания]( https://drive.google.com/file/d/1-EjUNBoZ2C1To-ktfDTp8mXzejQtrLbD/view?usp=sharing).
   API реализовано с помощью Django и Django REST framework.
   Для реализации более красивой и удобной админки использовал django-suit==0.2.26.
   При разработке использовал Python 3.6
   Для простоты проверки работы в качестве БД использовал Sqlite3.
    
### Развертывание:
    # Клонировать репозиторий
    >>> git clone https://github.com/DanilXO/CreditAppAPI.git
    >>> cd CreditAppAPI
    # Создать и активировать виртуальное окружение (Windows | Unix)
    >>> python -m venv venv
    >>> venv\Scripts\activate.bat | source tutorial-env/bin/activate
    # Установить зависимости
    >>> pip install -r requirements.txt
    # Выполнить миграции
    >>> python manage.py migrate
    # Запустить
    >>> set DJANGO_SETTINGS_MODULE=mysite.settings | export DJANGO_SETTINGS_MODULE=mysite.settings
    >>> python manage.py runserver
    
### Демонстрация работы:
![Screenshot1](http://dl4.joxi.net/drive/2019/11/17/0038/4064/2539488/88/3ae98bfb03.png)
![Screenshot2](http://dl3.joxi.net/drive/2019/11/17/0038/4064/2539488/88/59c690e340.png)
![Screenshot3](http://dl3.joxi.net/drive/2019/11/17/0038/4064/2539488/88/f6747d3e02.png)

            
