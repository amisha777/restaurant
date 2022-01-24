import psycopg2
import psycopg2.extras


class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def get_menu(self):
        self.__cursor.execute("SELECT name_dish, price_dish, picture FROM dish")
        menu = self.__cursor.fetchall()
        return menu

    # достаем данные из reserve в табличку на странице
    def get_podbron(self):
        self.__cursor.execute("SELECT people, date, time, fio_reserve, phone_reserve, vish_reserve, "
                              "id_reserve FROM reserve")
        podbron = self.__cursor.fetchall()
        return podbron

    # достаем данные из zakaz в табличку на странице
    def get_podzakaz(self):
        self.__cursor.execute("SELECT price_zakaz, data, address_dostavki, fio_zakaz, time, phone_zakaz, "
                              "people_zakaz, vish_zakaz, payment_zakaz, number_zakaz FROM zakaz")
        podzakaz = self.__cursor.fetchall()
        return podzakaz

    # после нажатия кнопки перемещаем данные в таблицу подтвержденного заказа
    def get_info_podzakaz(self, number_zakaz):
        self.__cursor.execute("SELECT price_zakaz, data, address_dostavki, id_user, fio_zakaz, "
                              "time, phone_zakaz, people_zakaz, vish_zakaz, payment_zakaz, "
                              "number_zakaz FROM zakaz WHERE number_zakaz=%s", (number_zakaz,))
        info_podzakaz = self.__cursor.fetchall()
        return info_podzakaz

    def add_podzakaz(self, price_zakaz, data, address_dostavki, id_user, fio_zakaz, time,
                     phone_zakaz, people_zakaz, vish_zakaz, payment_zakaz, id_sotrudnik, number_zakaz):
        self.__cursor.execute(f"""INSERT INTO zakaz_podtverzh (price_zakaz, data, address_dostavki, id_user, fio_zakaz, 
                              time, phone_zakaz, people_zakaz, vish_zakaz, payment_zakaz, id_sotrudnik, number_zakaz) 
                              VALUES ({price_zakaz},'{data}','{address_dostavki}',{id_user},'{fio_zakaz}','{time}',
                            '{phone_zakaz}',{people_zakaz},'{vish_zakaz}', '{payment_zakaz}', {id_sotrudnik},
                             {number_zakaz})""")
        self.__db.commit()

    def delete_info_podzakaz(self, number_zakaz):
        self.__cursor.execute("DELETE FROM zakaz WHERE number_zakaz=%s", (number_zakaz,))
        self.__db.commit()

    def get_info_podbron(self, id_reserve):
        self.__cursor.execute("SELECT people, date, time, fio_reserve, phone_reserve, vish_reserve, id_reserve "
                              "FROM reserve WHERE id_reserve=%s", (id_reserve,))
        info_podbron = self.__cursor.fetchall()
        return info_podbron

    # после нажатия кнопки перемещаем данные в таблицу подтвержденного резерва
    def add_podbron(self, people, date, time, fio, phone, vish, id_sotrudnik, id_reserve):
        self.__cursor.execute(f"""INSERT INTO reserve_podtverzh (people, date, time, fio_reserve, phone_reserve, 
        vish_reserve, id_sotrudnik, id_reserve) VALUES ('{people}', '{date}', '{time}', '{fio}', '{phone}', 
        '{vish}', {id_sotrudnik}, {id_reserve})""")
        self.__db.commit()

     # на странице удаляем данные из таблицы неподтвержденных резервов
    def delete_info_podbron(self, id_reserve):
        self.__cursor.execute("DELETE FROM reserve WHERE id_reserve=%s", (id_reserve,))
        self.__db.commit()

    def get_zakazpod(self):
        self.__cursor.execute("SELECT price_zakaz, data, address_dostavki, fio_zakaz, time, phone_zakaz, "
                              "people_zakaz, vish_zakaz, payment_zakaz, number_zakaz FROM zakaz_podtverzh")
        zakazpod = self.__cursor.fetchall()
        return zakazpod

    def get_bronpod(self):
        self.__cursor.execute("SELECT people, date, time, fio_reserve, phone_reserve, vish_reserve, "
                              "id_reserve FROM reserve_podtverzh")
        bronpod = self.__cursor.fetchall()
        return bronpod

    def get_dishes(self):
        self.__cursor.execute("SELECT name_dish FROM dish")
        dishes = self.__cursor.fetchall()
        return dishes

    def get_dish_for_id(self, id_dish):
        self.__cursor.execute(f"SELECT name_dish,price_dish FROM dish WHERE id_dish='{id_dish}'")
        dish_atr = self.__cursor.fetchall()
        return dish_atr

    def get_id_dish(self, name_dish):
        self.__cursor.execute(f"SELECT id_dish, kolich_dish FROM dish WHERE name_dish='{name_dish}'")
        id_dish = self.__cursor.fetchall()
        return id_dish

    def get_basket(self, id_user):
        self.__cursor.execute(f"SELECT id_dish, kolich_basket FROM position_basket WHERE id_user={id_user}")
        basket = self.__cursor.fetchall()
        return basket

    def add_basket(self, id_dish, id_user, kolich_basket):
        self.__cursor.execute("INSERT INTO position_basket (id_dish, id_user, kolich_basket) VALUES (%s,%s,%s)",
                              (id_dish, id_user, kolich_basket))
        self.__db.commit()

    def get_max_kolichdish(self):
        self.__cursor.execute("SELECT MAX(kolich_dish) FROM dish")
        kolich_dishes = self.__cursor.fetchall()
        return kolich_dishes

    def delete_basket(self, id_user):
        self.__cursor.execute(f"DELETE FROM position_basket WHERE id_user='{id_user}'")
        self.__db.commit()

    def get_account(self, login):
        self.__cursor.execute('SELECT * FROM users WHERE login = %s', (login,))
        account = self.__cursor.fetchall()
        return account

    def get_sotrudnik(self, phone):
        self.__cursor.execute('SELECT * FROM sotrudnik WHERE phone_sotrudnik = %s', (phone,))
        sotrudnik = self.__cursor.fetchone()
        return sotrudnik

    def add_account(self, login, password, fio, phone):
        self.__cursor.execute("INSERT INTO users (login, password, fio_user, phone_user) VALUES (%s,%s,%s,%s)",
                              (login, password, fio, phone))
        self.__db.commit()

    def get_user(self, phone):
        self.__cursor.execute('SELECT * FROM users WHERE phone_user = %s', (phone,))
        user = self.__cursor.fetchone()
        return user

    def add_reserve(self, people, date, time, fio, phone, vish):
        self.__cursor.execute(
            """INSERT INTO reserve (people, date, time, fio_reserve, phone_reserve, vish_reserve) VALUES 
            (%s,%s,%s,%s,%s,%s)""",
            (people, date, time, fio, phone, vish))
        self.__db.commit()

    def add_delivery(self, price_zakaz, date, address, id_user, fio, time, phone_zakaz, people, vish, payment):
        self.__cursor.execute(
            """INSERT INTO zakaz (price_zakaz, data, address_dostavki, id_user, fio_zakaz, time, 
            phone_zakaz, people_zakaz, vish_zakaz, payment_zakaz) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (price_zakaz, date, address, id_user, fio, time, phone_zakaz, people, vish, payment))
        self.__db.commit()

    def get_bron(self):
        # Ищу максимальное значение id в таблице reserve
        self.__cursor.execute("SELECT MAX(id_reserve) FROM reserve")
        max_id_reserve = self.__cursor.fetchall()
        print(max_id_reserve)
        if not max_id_reserve:
            max_id_reserve = 1
        self.__cursor.execute("SELECT * FROM reserve WHERE id_reserve = %s", (max_id_reserve,))
        bron = self.__cursor.fetchone()
        return bron
