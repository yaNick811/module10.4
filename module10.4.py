import threading
import time
import random
from queue import Queue

class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None

class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        # Гость сидит за столом случайное время от 3 до 10 секунд
        time.sleep(random.randint(3, 10))

class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = list(tables)

    def guest_arrival(self, *guests):
        for guest in guests:
            # Ищем свободный стол
            free_table = None
            for table in self.tables:
                if table.guest is None:
                    free_table = table
                    break

            if free_table:
                # Сажаем гостя за свободный стол
                free_table.guest = guest
                guest.start()
                print(f"{guest.name} сел(-а) за стол номер {free_table.number}")
            else:
                # Если свободных столов нет, добавляем гостя в очередь
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest and not table.guest.is_alive():
                    # Гость закончил есть
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None

                    # Если есть гости в очереди, сажаем их за освободившийся стол
                    if not self.queue.empty():
                        new_guest = self.queue.get()
                        table.guest = new_guest
                        new_guest.start()
                        print(f"{new_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")

# Пример использования
if __name__ == "__main__":
    # Создаем столы
    table1 = Table(1)
    table2 = Table(2)
    table3 = Table(3)

    # Создаем кафе с этими столами
    cafe = Cafe(table1, table2, table3)

    # Создаем гостей
    guest1 = Guest('Vasya')
    guest2 = Guest('Petya')
    guest3 = Guest('Masha')
    guest4 = Guest('Dasha')
    guest5 = Guest('Sasha')

    # Гости приходят в кафе
    cafe.guest_arrival(guest1, guest2, guest3, guest4, guest5)

    # Обслуживаем гостей
    cafe.discuss_guests()