from main import conn, cur

class Employeer:
    def __init__(self, id):
        self.id = id

    l = []
    def del_service(self):
        print("Какой вид услуг вы хотите оказать, для просмотра всех нажмите Enter")
        num = input("1. Уборка\n2. Сантехника\n3. Электрика\n4. Другое\n")
        if num == '':
            cur.execute("SELECT room_number, task_name, description "
                        "FROM tasks JOIN task_types ON task_types.id = tasks.type_id ")
            l = cur.fetchall()
        else:
            try:
                cur.execute(f"SELECT room_number, task_name, description "
                            f"FROM tasks "
                            f"JOIN task_types ON task_types.id = tasks.type_id "
                            f"WHERE type_id = {num}")
                l = cur.fetchall()
                if len(l) == 0:
                    print("Услуги этого типа не были заказаны")
                    return
            except:
                print("Вы ввели некорректное значение")
        if len(l) > 0:
            cl = 0
            for i in l:
                cl += 1
                print(f"{cl}. В номере {i[0]} требуется {i[1]}  {i[2]}")
            num = int(input())
            cur.execute(f"DELETE FROM tasks "
                        f"WHERE type_id IN "
                        f"(SELECT id FROM task_types "
                        f"WHERE task_types.task_name = '{str(l[num - 1][1]).strip('()[],')}') "
                        f"AND room_number = {l[num-1][0]}")
            conn.commit()
        else:
            print("Услуги не требуются!!!")
            print()

    def raslogin(self):
        print()
        return True
    def action(self):
        while True:
            print("1. Выполнить услугу\n2. Разлогиниться")
            num = int(input())
            match num:
                case 1: self.del_service()
                case 2: self.raslogin()




