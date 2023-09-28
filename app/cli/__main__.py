import sys
import getpass
import hashlib
import sqlite3
import getpass
import json
import os

from app.serveces.user import User
from app.dao.user_dao import UserDao


def registration():
    login = input("Введите ваше имя: ")
    age = input("Введите ваш возраст: ")
    phone_number = input("Введите ваш номер телефона: ")
    email = input("Введите ваш email: ")
    while True:
        password = getpass.getpass("Введите ваш пароль: ")
        password_repet = getpass.getpass("Подтвердите пароль: ")
        if password == password_repet:
            break
        else:
            print("Попробуйте еще...")
            continue
    print("Пароль принят")
    hashpass = hashlib.sha256(password.encode("utf-8")).hexdigest()
    user = User(login, hashpass, age, phone_number, email)
    user_dao = UserDao()
    user_dao.create(user)


def login():
    while True:
        login = input("Введите ваш login: ")
        input_hashpass = getpass.getpass("Введите пароль: ")
        hashpass = hashlib.sha256(input_hashpass.encode("utf-8")).hexdigest()

        user_dao = UserDao()
        user = user_dao.find_by_login(login)

        if not user:
            print("Пользователь не найден!")
            continue
        if user.hashpass != hashpass:
            print("Неверный пароль!")
            continue
        print('Авторизация успешна. Добро пожаловать,', login)
        data = {
            "login": login,
            "hashpass": hashpass,
        }
        if not os.path.exists(".cache"):
            os.makedirs(".cache")
        with open(".cache/data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        break

def whoami():
    with open('.cache/data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    login = data['login']

    user_dao = UserDao()
    user = user_dao.all_information(login)

    if user:
        print(
            f"Добро пожаловать {user.login}! Ваш возраст: {user.age} лет. Ваш номер телефона: {user.phone_number}. Ваша почта: {user.email}"
            )
    else:
        print("Сначала авторизуйтесь!")
#НЕ РАБОТАЕТ БЛОК ELSE


def logout():

    with open('.cache/data.json', 'r') as file:
        data = json.load(file)
    if data == {}:
        print("вы не авторизованны!")
    else:
        data = {}
        with open('.cache/data.json', 'w') as file:
            json.dump(data, file)
            print("Вы вышли из системы!")


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    command = args[0]
    if command == 'registration':
        registration()
    elif command == 'login':
        login()
    elif command == 'whoami':
        whoami()
    elif command == 'logout':
        logout()
    else:
        print("БЛЯ РЕБЯТ ЧЕ ЕБАНУЛИСЬ СОВСЕМ?")
        return 1
    return 0



if __name__ == '__main__':
    main()