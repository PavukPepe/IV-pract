
from main import conn, cur

from Employeer import Employeer
from Admin import Admin
from Customer import Customer

EXECUTORS = {
    'Customer':Customer,
    'Employeer':Employeer,
    'Admin':Admin
}
class User:
    def autorization(self, login, password):
        # try:
            cur.execute(f"SELECT post_name, user_name FROM users JOIN posts ON users.post_id = posts.id WHERE users.login = '{login}' AND users.pass = '{password}'")
            status = cur.fetchall()[0]
            print(f'Вы вошли как: {status[0]} {status[1]}')
            cur.execute(f"SELECT users.id FROM users JOIN "
                        f"posts ON users.post_id = posts.id "
                        f"WHERE users.login = '{login}' AND users.pass = '{password}'")
            id = cur.fetchall()[0]
            executor = EXECUTORS.get(status[0],None)
            return executor(id[0])
        # except:
        #     print("Неверный логин или пароль")
    def registration(self, user_name, login, password):
        try:
            cur.execute(f"INSERT INTO users(login, pass, post_id, user_name) VALUES ('{login}', '{password}', 2, '{user_name}')")
            print("Вы успешно зарегистрировались!")
            conn.commit()
        except:
            print("Некорректный ввод данных")

    def action(self):
        while True:
            print("1. Авторизация\n2. Регистрация")
            num = int(input())
            match num:
                case 1:
                    exe=self.autorization(input("Введите логин: "), input("Введите пароль: "))
                    exe.action()
                case 2: self.registration(input("Введите имя пользователя: "), input("Введите логин: "), input("Введите пароль: "))


per = User()
while True:
    if(per.action()):
        per = User()

