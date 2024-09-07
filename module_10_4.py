import queue
from threading import Thread
from time import sleep
from random import randint

'''Цель: Применить очереди в работе с потоками, используя класс Queue.'''

class Table:
    '''
    Задача "Потоки гостей в кафе":
    Необходимо имитировать ситуацию с посещением гостями кафе.
    Создайте 3 класса: Table, Guest и Cafe.
    Класс Table:
    Объекты этого класса должны создаваться следующим способом - Table(1)
    Обладать атрибутами number - номер стола и guest - гость, который сидит за этим столом (по умолчанию None)'''
    def __init__(self, number: int):
        self.number = number
        self.guest = None

    def __bool__(self):
        if self.guest == None:
            return False
        return True

class Guest(Thread):
    '''
    Класс Guest:
    Должен наследоваться от класса Thread (быть потоком).
    Объекты этого класса должны создаваться следующим способом - Guest('Vasya').
    Обладать атрибутом name - имя гостя.
    Обладать методом run, где происходит ожидание случайным образом от 3 до 10 секунд.
    '''
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        tau = randint(3, 10)
        sleep(tau)

    def __str__(self):
        return self.name

class Cafe:
    def __init__(self, *tables: Table):
        self.queue = queue.Queue()
        self.tables = {table.number: table for table in tables}

    def _find_free_table(self):
        for n, table in self.tables.items():
            if not table:
                return n


    def _all_tables_free(self):
        for n, table in self.tables.items():
            if table:
                return False
        return True

    def guest_arrival(self, *guests: Guest):
        for guest in guests:
            n = self._find_free_table()
            if n is None:
                self.queue.put(guest)
                print(f'{guest} ждет в очереди...')
            else:
                self.tables[n].guest = guest
                guest.start()
                print(f'{guest} сел(-а) за стол номер {n}.')


    def discuss_guests(self):
        while not (self._all_tables_free() and self.queue.empty()):
            for n, t in self.tables.items():
                if not t.guest is None:
                    if not t.guest.is_alive():
                        print(f'{t.guest} покушал(-а) и ушёл(ушла).\nСтол номер {n} свободен.')
                        if not self.queue.empty():
                            self.tables[n].guest = self.queue.get()
                            self.tables[n].guest.start()
                            print(f'{t.guest} вышел(-ла) из очереди и сел(-а) за стол номер {n}.')
                        else:
                            self.tables[n].guest = None

def main():
    # Создание столов
    tables = [Table(number) for number in range(1, 6)]
    # Имена гостей
    guests_names = ['Мария', 'Олег', 'Вахтанг', 'Сергей', 'Дарья', 'Арман', 'Виктория', 'Никита', 'Павел', 'Илья', 'Александр']
    # Создание гостей
    guests = [Guest(name) for name in guests_names]
    # Заполнение кафе столами
    cafe = Cafe(*tables)
    # Приём гостей
    cafe.guest_arrival(*guests)
    # Обслуживание гостей
    cafe.discuss_guests()

if __name__ == '__main__':
    main()
