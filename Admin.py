from main import conn, cur


class Admin:
    def __init__(self, id):
        self.id = id
    def add_user(self):
        user_name = input("Введите имя нового пользователя")
        login = input("Введите логин нового пользователя: ")
        password = input("Введите пароль нового пользователя: ")
        cur.execute("SELECT * FROM posts")
        roles = cur.fetchall()
        print(*[f"{i[0]}. {i[1]}\n" for i in roles], sep='')
        role = int(input("Выберите роль: "))
        cur.execute(f"INSERT INTO users(login, pass, post_id, user_name) VALUES ('{login}', '{password}', {role}, '{user_name}')")
        conn.commit()
        print("Пользователь успешно добавлен")

    def add_room(self):
        room_number = int(input("Введите номер добавляемого номера: "))
        cur.execute("SELECT * FROM room_types")
        roles = cur.fetchall()
        print(*[f"{i[0]}. {i[1]}\n" for i in roles], sep='')
        type_id = int(input("Выберите тип комнаты: "))
        stat = "y"==input("Комната забронирована? [y/n]")
        if stat:
            cur.execute("SELECT users.id, user_name FROM users "
                        "WHERE post_id = 3")
            roles = cur.fetchall()
            print(*[f"{i[0]}. {i[1]}\n" for i in roles], sep='')
            user_name = input("Введите id владельца")
        else:
            user_name = 'NULL'
        cur.execute(f"SELECT room_number, type_id, booking_status, owner_id FROM rooms WHERE room_number = {room_number}")
        if len(cur.fetchall()) > 0:
            print('Такая комната уже существует')

        else:
            cur.execute(
                f"INSERT INTO rooms(room_number, type_id, booking_status, owner_id) "
                f"VALUES ('{room_number}', '{type_id}', {stat}, {user_name})")
            conn.commit()
            print("Комната успешно добавлена!")
    def add_service(self):
        print("Для какой комнаты вы хотите добавить услугу? ")
        cur.execute(f"SELECT room_number FROM rooms")
        roles = cur.fetchall()
        roles.sort()
        print(*[f"Комната {i[0]}\n" for i in roles], sep='')
        room = int(input("Введите номер комнаты: "))

        print("Выберите тип услуги")
        cur.execute(f"SELECT * FROM task_types")
        roles = cur.fetchall()
        print(*[f"{i[0]}. {i[1]}\n" for i in roles], sep='')
        task_type = int(input("Введите тип услуги: "))

        if task_type == 4:
            desc = input("Введите описание проблемы")
        else:
            desc = 'NULL'

        cur.execute(f'INSERT INTO tasks (type_id, room_number, description) '
                    f'VALUES ({task_type}, {room}, {desc})')
        conn.commit()
    def del_service(self):
        print("Для какой комнаты вы хотите удалить услугу? ")
        cur.execute(f"SELECT room_number FROM rooms")
        rooms = cur.fetchall()
        rooms.sort()
        print(*[f"Комната {i[0]}\n" for i in rooms], sep='')
        room = int(input("Введите номер комнаты: "))

        cur.execute(f"SELECT task_name FROM tasks "
                    f"JOIN task_types ON type_id = task_types.id "
                    f"WHERE room_number = {room}")
        servises = cur.fetchall()
        if len(servises) > 0:
            cl = 0
            for i in servises:
                cl += 1
                print(f"{cl}. {i[0]}")

            cl = int(input("Введите номер услуги, которая должна быть удалена"))
            t_name = str(servises[cl-1]).strip("'(),")

            cur.execute(f"DELETE FROM tasks "
                        f"WHERE type_id IN "
                        f"(SELECT id FROM task_types "
                        f"WHERE task_types.task_name = '{t_name}') "
                        f"AND room_number = {room}")
            conn.commit()
        else:
            print("У этой комнаты нет активных услуг")

    def del_user(self):
        cur.execute(f"SELECT users.id, user_name, post_name FROM users "
                    f"JOIN posts ON post_id = posts.id ")
        users = cur.fetchall()
        print(*[f"{i[0]}. {i[1]} {i[2]}\n" for i in users], sep='')
        u_id = int(input("Какого пользователя вы хотите удалить: "))
        if u_id == self.id:
            print("Админа можно  удалить только через СУБД (защита от дурачка)")
            return
        cur.execute(f"DELETE FROM users WHERE id = {u_id}")
        conn.commit()

    def del_room(self):
        cur.execute(f"SELECT room_number FROM rooms")
        rooms = cur.fetchall()
        rooms.sort()
        print(*[f"Комната {i[0]}\n" for i in rooms], sep='')

        r_num = int(input("Введите номер комнаты, которую хотите удалить: "))
        cur.execute(f"DELETE FROM rooms WHERE room_number = {r_num}")
        conn.commit()

    def update_user(self):
        cur.execute(f"SELECT users.id, user_name, post_name, post_id FROM users "
                    f"JOIN posts ON post_id = posts.id ")
        cl = 0
        users = cur.fetchall()
        for i in users:
            cl += 1
            print(f"{cl}. {i[1]} {i[2]}" )
        u_id = int(users[int(input("Какого пользователя вы хотите изменить: "))][3])
        if users[u_id][2] == 'Admin':
            print("Админа можно изменить только через СУБД (защита от дурачка)")
            return
        cur.execute(f"SELECT * FROM users WHERE id = {u_id}")
        print(cur.fetchall())
        cur.execute("SELECT ordinal_position, column_name FROM INFORMATION_SCHEMA.COLUMNS "
                    "WHERE TABLE_NAME = 'users'")
        columns = cur.fetchall()
        columns.sort()
        print(*[f"{i[0]}. {i[1]} \n" for i in columns], sep='')
        clm = int(input("Выберите столбец: "))
        an = input()

        cur.execute(f"UPDATE users SET {columns[clm-1][1]} = '{an}' WHERE id = {u_id}")
        conn.commit()
    def raslogin(self):
        print()
        return True
    def action(self):
        num = int(input("1. Добавить пользователя\n2. Добавить комнату\n3. Добавить услугу в номер\n"
                        "4. Удалить услугу\n5. Удалить полььзователя\n6. Удалить комнату\n7. Изменить данные пользователя\n8. Разлогиниться"))
        match num:
            case 1: self.add_user()
            case 2: self.add_room()
            case 3: self.add_service()
            case 4: self.del_service()
            case 5: self.del_user()
            case 6: self.del_room()
            case 7: self.update_user()
            case 8: self.raslogin()
