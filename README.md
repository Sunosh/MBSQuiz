# MBS

### [???./](https://???.com/) [![Website letsquiz.pythonanywhere.com](https://img.shields.io/website-up-down-green-red/http/letsquiz.pythonanywhere.com.svg)](http://letsquiz.pythonanywhere.com/)

Это онлайн платформа олимпиад, с помощью Python веб-фреймворка Django.<br>
For front-end designing I have used Twitter's front-end library Bootstrap4.

[![GitHub release](https://img.shields.io/github/release/akashgiricse/lets-quiz.svg)](https://img.shields.io/bower/vpre/bootstrap.svg)
[![GitHub forks](https://img.shields.io/github/forks/akashgiricse/lets-quiz.svg)](https://github.com/akashgiricse/lets-quiz/network)
[![GitHub stars](https://img.shields.io/github/stars/akashgiricse/lets-quiz.svg)](https://github.com/akashgiricse/lets-quiz/stargazers)
[![GitHub license](https://img.shields.io/github/license/akashgiricse/lets-quiz.svg)](https://github.com/akashgiricse/lets-quiz/blob/master/LICENSE)
[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

## Доступные сейчас функции:

### Функции доступа к сайту:

- Для доступа к сайту пользователь должен быть зарегистрирован.
- Для регистрации пользователь обязан предоставить свои: _НикНейм_, _Электронная почта_ и _Пароль_.
- For login the user will be required to enter _username_ and _password_ only.

### Функции платформы:

- Все вопросы выбираются рандомно.
- Каждый вопрос показывается единожды для каждого пользователя.
- Если пользователь случайно обновит страницу или перейдёт на предыдущюю страницу, то будет показан отдельный вопрос с новым условием в соответствии с туром.
- После отправки ответа сразу будет показано "Правильно/Неправильно".

### Функции Таблицы Лидеров:

- Таблица Лидеров- таблица, где пользователи сортируются по счёту.
- Если два пользователя имеют одинаковый счёт, то первее будет тот, кто зарегистрировался ранше другого.
- Таблица Лидеров открыта для всех. Доступен вход без логина.

### Функции администратора:

- Только админы могут добавлять вопросы.
- Админы могут редактировать вопросы до того как они будут помечены  _Опубликован?_
- Вопрос выкладывается единожды, он может быть доступен только единожды. Админы могут просматривать список вопросов.
- Админ может искать вопросы по условию или по вариантам ответов.
- Админ может фильтровать вопросы по категориия: Опубликовано, Не опубликовано.

## Начать разработку:

Dependencies:

- Python 3.6.x
- Django 1.11.x
- Ubuntu 17.04 или позже or Linux Mint 18.2 или позже

### 1. Скопируйте себе этот репозиторий

```bash
git clone https://github.com/akashgiricse/lets-quiz.git
cd lets_quiz
```

### 2. Установите [Pipenv](https://pipenv.pypa.io/en/latest/)

### 3. Создайте виртуальное пространство

```bash
## run following command from `lets_quiz` directory
pipenv shell
```

### 4. Установите модули Python

```bash
pip install -r requirements.txt
```

### 5. Установите базу данных

_TODO - Добавляйте инструкцию для этого когда я начинаю использовать базу данных MySQL._

### 6. Запустите миграции баз данных

```bash
cd lets_quiz
python manage.py migrate
```

### 7. Создайте аккаунт суперпользователя

```bash
python manage.py createsuperuser
```

### 8. Запустите сервер разработки

```bash
python manage.py runserver
```

## Разработка

- Исходный код: [Download zip: Release v1.0.1](https://github.com/MBSQuiz)

## Создатели

- [Lixer](https://github.com/lixerso2)

## Поддержка

- Если есть какие-то проблемы или вопросы, 
- Пожалуйста напишите мне на почту "standoffdidzej@gmail.com"

## License

MIT Лицензия

Авторское право (с) 2023 Lixer, Suno.
