# salary_api_task

Описание задачи: Реализуйте REST-сервис просмотра текущей зарплаты и даты следующего
повышения. Из-за того, что такие данные очень важны и критичны, каждый
сотрудник может видеть только свою сумму. Для обеспечения безопасности, вам
потребуется реализовать метод где по логину и паролю сотрудника будет выдан
секретный токен, который действует в течение определенного времени. Запрос
данных о зарплате должен выдаваться только при предъявлении валидного токена.

Stack

- Python 3.11
- FastAPI 0.88.0
- PostgreSQL 15
- Docker


## Как запустить проект?

Для поднятия сервисов баз для локальной разработки нужно запустить команду:

```
make up
```

Для накатывания миграций, если файла alembic.ini ещё нет, нужно запустить в терминале команду:

```
alembic init migrations
```

После этого будет создана папка с миграциями и конфигурационный файл для алембика.

- В alembic.ini нужно задать адрес базы данных, в которую будем создавать миграции.
- Дальше необходимо зайти в папку с миграциями и открыть env.py, там вносим изменения в блок, где написано

```
from myapp import mymodel
```

- Дальше вводим: ```alembic revision --autogenerate -m "comment"``` - делается при любых изменениях моделей
- Будет создана миграция
- Дальше вводим: ```alembic upgrade heads```

Для того, чтобы во время тестов нормально генерировались миграции нужно:
- сначала попробовать запустить тесты обычным образом. с первого раза оно должно не сработать
- если после падения в папке tests создались алембиковские файлы, то нужно прописать туда данные по миграциям
- если они не создались, то зайти из консоли в папку test и вызвать вручную команды на миграции, чтобы файлы появились

Для запуска сервиса необходимо:
- Создать виртуальное окружение, выполнив команду python -m venv venv находясь внутри папки с файлами
- Активировать виртуальное окружение, выполнив команду ```venv\bin\activate```
- Установить зависимости, выполнив команду ```pip install -r requirements.py```
- Запустить файл main.py
- Перейти по адресу ```http://127.0.0.1:8003/docs```

## Содержание API

В рамках сервиса были реализованы две таблицы: users и salary_info.

Таблица users содержит поля:
- user_id
- login
- hashed_password
- name
- surname
- email
- is_active
- roles

Таблица salary_info содержит поля:
- salary_id
- user_id
- salary
- next_salary_increase


REST-сервис содержит в себе следующие функции:

- Создание пользователя
- Редактирование данных пользователя
- Удаление пользователя
- Получение пользователя по id
- Добавление пользователю роли Администратора
- Получение данных о текущей зарплате и дате следующего повышения
- Создание данных о текущей зарплате и дате следующего повышения
- Изменение данных о текущей зарплате и дате следующего повышения
- Удаление данных о текущей зарплате и дате следующего повышения
- Получение токена

Сервис содержит ролевую модель, которая включает в себя: пользователя, админа и суперпользователя.
Получить информацию о текущих зарплатных данных можно получить только при ввода валидного токена.
Функции создания, изменения и удаления данных о зарплате доступны только админу и суперпользователю.

Взаимодействия с сервисом осущестляется с помощью эндпоинтов:
- Авторизация
    - `/login`, принимает в теле запроса логин и пароль сотрудника, отдает jwt-токен
- Данные о сотруднике
    - `/user`, принимает id и токен, при валидности токена отдает информацию о пользователе
- Зарплатные данные
    - `/user/salary`, принимает токен, при валидности токена отдает данные текущего пользователя

## Некотрорые примеры работы API-сервиса

__Получение токена, используя логин и пароль__

<img width="1437" alt="image" src="https://gitlab.com/keyzoz/salary_api_task/raw/main/doc_images/auth.png">

__Получение зарплатных данных пользователя, при успешной аутентификации__

<img width="1437" alt="image" src="https://gitlab.com/keyzoz/salary_api_task/raw/main/doc_images/get_salary_info.png">

__Получение данных о пользователе по id при успешной авторизации__

<img width="1437" alt="image" src="https://gitlab.com/keyzoz/salary_api_task/raw/main/doc_images/get_user_info.png">


## Swagger documentation

<img width="1437" alt="image" src="https://gitlab.com/keyzoz/salary_api_task/raw/main/doc_images/swagger.png">


