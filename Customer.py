from main import conn, cur
from Employeer import Employeer
from Admin import Admin

class Customer:
    room = []

    def __init__(self, id):

        self.id = id
        # try:

        cur.execute(f"SELECT room_number FROM rooms "
                        f"WHERE owner_id = {self.id}")

        l = cur.fetchall()
        self.room = [int(str(l[i]).strip("(),")) for i in range(len(l))]
        # except:
        self.room = []

    def booking(self):

        cur.execute(f"SELECT room_number, room_name FROM rooms JOIN room_types "
                    f"ON rooms.type_id=room_types.id WHERE booking_status = FALSE")

        l = cur.fetchall()
        print(" №   Тип")
        #Вывод свободных номеров
        if len(l) > 0:
            print(*[l[i] for i in range(len(l))], sep='\t\n')
            num = int(input("Выберите номер комнаты, которую хотите забронировать: "))
        else:
            print("Свободных номеров нет")
            return
        try:

            cur.execute(f'UPDATE rooms '
                        f'SET booking_status = TRUE, owner_id = {self.id} '
                        f'WHERE room_number = {num} AND owner_id IS NULL')

            self.room.append(int(num))
            conn.commit()
        except:
            print("Вы ввели некорректный номер комнаты")

    def service(self):
        if self.room == []:
            print("Вы не бронировали комнаты")
            return
        try:
            for i in self.room:
                print(f"Комната {i}")
            k = int(input(f"В какую из комнат вы хотите получить услугу?"))
            if k not in self.room:
                return
            num = int(input("1. Уборка\n2. Сантехника\n3. Электрика\n4. Другое\n"))
            if num == 4:
                desc = input("Введите описание проблемы")

                cur.execute(f'INSERT INTO tasks (type_id, room_number, description) '
                            f'VALUES ({num}, {k}, {desc})')
            else:

                cur.execute(f'INSERT INTO tasks (type_id, room_number, description) '
                            f'VALUES ({num}, {k}, NULL)')
            conn.commit()
        except:
            print("Услуга этого типа была добавлена ранее")

    def del_booking(self):
        if self.room == []:
            print("Вы не бронировали комнаты")
            return
        for i in self.room:
            print(f"Комната {i}")
        k = int(input(f"От какой комнаты вы хотите отказаться"))
        if k not in self.room:
            return
        self.room.remove(k)

        cur.execute(f"UPDATE rooms "
                    f"SET booking_status = FALSE, owner_id = NULL "
                    f"WHERE owner_id = {self.id} and room_number = {k}")

        conn.commit()


    def del_service(self):
        if self.room == []:
            print("Вы не бронировали комнаты")
            return
        l = []
        for i in self.room:
            print(f"Комната {i}")
        k = int(input(f"От услуг в какой комнате вы хотите отказаться? "))

        cur.execute(f"SELECT task_types.task_name FROM tasks "
                    f"JOIN task_types ON type_id = task_types.id "
                    f"WHERE room_number = {k}")

        l.append(cur.fetchall())
        cl = 0
        for j in l:
            if len(j) > 0:
                cl += 1
                print(f"{cl}. {str(j).strip('()[],')}")

        cl = int(input("Введите номер услуги, от которой хотите отказаться"))

        cur.execute(f"DELETE FROM tasks "
                    f"WHERE type_id IN "
                    f"(SELECT id FROM task_types "
                    f"WHERE task_types.task_name = {str(l[cl-1]).strip('()[],')}) "
                    f"AND room_number = {k}")

        conn.commit()


    def raslogin(self):
        print()
        return True
    def action(self):
        while True:
            print("1. Бронирование\n2. Заказ услуг\n3. Отказ от бронирования\n4. Отказ от услуг\n5. Разлогиниться")
            num = int(input())
            match num:
                case 1: self.booking()
                case 2: self.service()
                case 3: self.del_booking()
                case 4: self.del_service()
                case 5: self.raslogin()

#
# per = Customer(2)
# while True:
#     per.action()


