![main](https://github.com/TwillightGolem/foodgram-project-react/actions/workflows/main.yml/badge.svg)
# Foodgram
## Описание:
На сайте "Foodgram" пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в «Избранное», а перед походом в магазин скачивать в виде pdf-файла сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд. На сайте доступна система регистрации и авторизации пользователей. Неавторизованным пользователям доступен просмотр рецептов на главной странице с фильтрацией по тегам, страниц отдельных рецептов и страниц других пользователей. Фронтенд и бекенд взаимодействуют через API.

### Использованные технологии:
- Python 3.9
- Django 2.2.19
- Django Rest Framework 3.12.4
- Djoser 2.1.0

### Локальный запуск приложения в контейнерах
Склонировать репозиторий на свой компьютер и перейти в корневую папку:

Создать в корневой папке файл .env с переменными окружения, необходимыми 
для работы приложения..

Пример содержимого файла:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

Перейти в папку /infra/ и запустить сборку контейнеров с помощью 
docker-compose: 
```
docker-compose up -d
```

Внутри контейнера web выполнить миграции, создать суперпользователя (для входа 
в админку), собрать статику и загрузить ингредиенты из recipes_ingredients.csv 
в базу данных:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```
После этого проект должен стать доступен по адресу http://127.0.0.1/.

Админ зона доступна по адресу http://127.0.0.1/admin/.

### Спецификация API в формате Redoc:

Чтобы посмотреть спецификацию API в формате Redoc, нужно локально запустить 
проект и перейти на страницу http://127.0.0.1/api/docs/

### Доступ к сайту для проверки:

Адрес сайта: https://foodingramm.hopto.org/

Администратор:
```
root              # Login
root              # Password
```

Пользователь 1:
```
user1@infra.com       # E-mail
12345678aA       # Password
```

Пользователь 2:
```
user2@infra.com       # E-mail
12345678aA       # Password
```

Пользователь 3:
```
user3@infra.com       # E-mail
12345678aA       # Password
```

Пользователь 4:
```
user4@infra.com       # E-mail
12345678aA       # Password
```

Пользователь 5:
```
user5@infra.com       # E-mail
12345678aA       # Password
```

Пользователь 6:
```
user6@infra.com       # E-mail
12345678aA       # Password
```

Пользователь 7:
```
user7@infra.com       # E-mail
12345678aA       # Password
```

#### Автор: 
**[Яковлев Александр](https://github.com/TwillightGolem)**

*truenoae8694yaa@yandex.ru*
