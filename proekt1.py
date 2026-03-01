import os
from dataclasses import dataclass

MAX_MAKER_LEN = 15
MAX_CHIP_LEN = 20
MAX_VIDEO_LEN = 20
counter = 4
warehouse = []

@dataclass
class GamingUnit:
    identifier: int
    maker: str
    chip: str
    video_chip: str
    memory: int
    storage: int
    mass: int
    cost: int
    amount: int

def locate_by_identifier(container, search_id):
    for position in range(len(container)):
        if container[position].identifier == search_id:
            return position
    return -1

def safe_number_input(message):
    while True:
        try:
            number = int(input(message))
            if number < 0:
                print("Число не может быть отрицательным!")
                continue
            return number
        except ValueError:
            print("Некорректный ввод, повторите попытку")

def safe_string_input(message, max_length):
    while True:
        value = input(message).strip()
        if not value:
            print("Ошибка! Строка не может быть пустой.")
        elif len(value) > max_length:
            print(f"Ошибка! Максимальная длина {max_length} символов.")
        else:
            return value

def display_collection(items, title="КАТАЛОГ"):
    if not items:
        print("\nКоллекция пуста.")
        return
    
    print("\n" + "="*110)
    print(f"{title:^110}")
    print("="*110)
    print(f"{'ID':<5} {'Бренд':<15} {'Процессор':<20} {'Видео':<15} "
          f"{'RAM':<6} {'SSD':<6} {'Вес':<6} {'Цена':<10} {'Кол-во':<8}")
    print("-"*110)
    
    for unit in items:
        print(f"{unit.identifier:<5} {unit.maker:<15} {unit.chip:<20} "
              f"{unit.video_chip:<15} {unit.memory:<6} {unit.storage:<6} "
              f"{unit.mass:<6} {unit.cost:<10} {unit.amount:<8}")
    print("="*110)

def add_new_unit():
    global counter, warehouse
    
    print("\n--- ДОБАВЛЕНИЕ НОВОЙ ЕДИНИЦЫ ---")
    
    maker = safe_string_input("Производитель: ", MAX_MAKER_LEN)
    chip = safe_string_input("Процессор: ", MAX_CHIP_LEN)
    video_chip = safe_string_input("Видеокарта: ", MAX_VIDEO_LEN)
    memory = safe_number_input("ОЗУ (ГБ): ")
    storage = safe_number_input("SSD (ГБ): ")
    mass = safe_number_input("Вес (граммы): ")
    cost = safe_number_input("Цена (руб): ")
    amount = safe_number_input("Количество на складе: ")
    
    counter += 1
    new_unit = GamingUnit(counter, maker, chip, video_chip, memory, storage, mass, cost, amount)
    warehouse.append(new_unit)
    
    print(f"\nЕдиница с ID {counter} успешно добавлена!")

def search_units():
    print("\n--- ПОИСК ЕДИНИЦ ---")
    print("(оставьте пустым, если критерий не важен)")
    
    min_memory_str = input("Минимальный объём ОЗУ (ГБ): ")
    max_cost_str = input("Максимальная цена (руб): ")
    
    results = warehouse.copy()
    
    if min_memory_str:
        try:
            min_memory = int(min_memory_str)
            results = [unit for unit in results if unit.memory >= min_memory]
        except ValueError:
            print("Ошибка! ОЗУ должно быть числом.")
    
    if max_cost_str:
        try:
            max_cost = int(max_cost_str)
            results = [unit for unit in results if unit.cost <= max_cost]
        except ValueError:
            print("Ошибка! Цена должна быть числом.")
    
    print(f"\nНайдено единиц: {len(results)}")
    display_collection(results, "РЕЗУЛЬТАТЫ ПОИСКА")

def sort_by_cost():
    if not warehouse:
        print("Коллекция пуста.")
        return
    sorted_list = sorted(warehouse, key=lambda unit: unit.cost)
    display_collection(sorted_list, "СОРТИРОВКА ПО ЦЕНЕ")

def sort_by_memory_storage():
    if not warehouse:
        print("Коллекция пуста.")
        return
    sorted_list = sorted(warehouse, key=lambda unit: unit.memory + unit.storage, reverse=True)
    display_collection(sorted_list, "СОРТИРОВКА ПО СУММЕ ОЗУ+SSD")
def remove_by_identifier():
    if not warehouse:
        print("Коллекция пуста.")
        return
    
    target = safe_number_input("Введите ID для удаления: ")
    position = locate_by_identifier(warehouse, target)
    
    if position != -1:
        removed = warehouse.pop(position)
        print(f"Единица {removed.maker} с ID {target} удалена.")
    else:
        print(f"Единица с ID {target} не найдена.")

def remove_by_position():
    if not warehouse:
        print("Коллекция пуста.")
        return
    
    print("\nТекущая коллекция:")
    for i, unit in enumerate(warehouse, 1):
        print(f"{i}. ID: {unit.identifier} | {unit.maker} | {unit.chip} | {unit.cost} руб.")
    
    pos = safe_number_input(f"Введите номер в списке (1-{len(warehouse)}): ")
    
    if 1 <= pos <= len(warehouse):
        removed = warehouse.pop(pos - 1)
        print(f"Единица {removed.maker} с ID {removed.identifier} удалена.")
    else:
        print("Неверный номер.")

def increase_memory():
    if not warehouse:
        print("Коллекция пуста.")
        return
    
    target = safe_number_input("Введите ID единицы: ")
    position = locate_by_identifier(warehouse, target)
    
    if position != -1:
        print(f"Текущий объём ОЗУ: {warehouse[position].memory} ГБ")
        additional = safe_number_input("На сколько ГБ увеличить: ")
        if additional > 0:
            warehouse[position].memory += additional
            print(f"Новый объём ОЗУ: {warehouse[position].memory} ГБ")
        else:
            print("Значение должно быть положительным!")
    else:
        print(f"Единица с ID {target} не найдена.")

def apply_sale():
    if not warehouse:
        print("Коллекция пуста.")
        return
    
    target = safe_number_input("Введите ID единицы: ")
    position = locate_by_identifier(warehouse, target)
    
    if position != -1:
        old_cost = warehouse[position].cost
        warehouse[position].cost = int(warehouse[position].cost * 0.9)
        print(f"Старая цена: {old_cost} руб.")
        print(f"Новая цена: {warehouse[position].cost} руб. (скидка 10%)")
    else:
        print(f"Единица с ID {target} не найдена.")

def show_cost_extremes():
    if not warehouse:
        print("Коллекция пуста.")
        return
    
    most_expensive = max(warehouse, key=lambda unit: unit.cost)
    cheapest = min(warehouse, key=lambda unit: unit.cost)
    
    print("\n--- САМАЯ ДОРОГАЯ ЕДИНИЦА ---")
    print(f"ID: {most_expensive.identifier}")
    print(f"Производитель: {most_expensive.maker}")
    print(f"Процессор: {most_expensive.chip}")
    print(f"Видеокарта: {most_expensive.video_chip}")
    print(f"ОЗУ: {most_expensive.memory} ГБ")
    print(f"SSD: {most_expensive.storage} ГБ")
    print(f"Цена: {most_expensive.cost} руб.")
    
    print("\n--- САМАЯ ДЕШЁВАЯ ЕДИНИЦА ---")
    print(f"ID: {cheapest.identifier}")
    print(f"Производитель: {cheapest.maker}")
    print(f"Процессор: {cheapest.chip}")
    print(f"Видеокарта: {cheapest.video_chip}")
    print(f"ОЗУ: {cheapest.memory} ГБ")
    print(f"SSD: {cheapest.storage} ГБ")
    print(f"Цена: {cheapest.cost} руб.")

def filter_by_video():
    if not warehouse:
        print("Коллекция пуста.")
        return
    
    search_term = input("Введите модель видеокарты для поиска: ").strip()
    
    if not search_term:
        print("Введите модель видеокарты!")
        return
    
    results = []
    for unit in warehouse:
        if search_term.lower() in unit.video_chip.lower():
            results.append(unit)
    
    print(f"\nНайдено единиц: {len(results)}")
    display_collection(results, "РЕЗУЛЬТАТЫ ПОИСКА ПО ВИДЕОКАРТЕ")

def show_menu():
    print("\n" + "="*60)
    print("ГЛАВНОЕ МЕНЮ УПРАВЛЕНИЯ КОЛЛЕКЦИЕЙ")
    print("="*60)
    print(f"Всего единиц в базе: {len(warehouse)}")
    print("-"*60)
    print("1. Показать все единицы")
    print("2. Добавить единицу")
    print("3. Поиск единиц")
    print("4. Сортировка по цене")
    print("5. Сортировка по сумме (ОЗУ + SSD)")
    print("6. Удалить по ID")
    print("7. Удалить по номеру в списке")
    print("8. Увеличить ОЗУ")
    print("9. Распродажа (-10%)")
    print("10. Самая дорогая и самая дешёвая")
    print("11. Поиск по видеокарте")
    print("-"*60)
    print("0. Выход")
    print("="*60)

warehouse.append(GamingUnit(1, "ASUS", "Intel i7-13700K", "RTX 4070", 32, 1000, 2500, 120000, 5))
warehouse.append(GamingUnit(2, "MSI", "AMD Ryzen 9 7950X", "RTX 4080", 64, 2000, 3000, 200000, 3))
warehouse.append(GamingUnit(3, "Gigabyte", "Intel i5-13600K", "RTX 4060 Ti", 16, 512, 2200, 85000, 8))
warehouse.append(GamingUnit(4, "Lenovo", "AMD Ryzen 7 7800X", "RTX 3060", 16, 512, 2100, 75000, 12))

counter = max((unit.identifier for unit in warehouse), default=4)

program_active = True

while program_active:
    show_menu()
    user_choice = input("\nВыберите действие: ")
    
    os.system("cls" if os.name == "nt" else "clear")
    
    if user_choice == "1":
        display_collection(warehouse)
    
    elif user_choice == "2":
        add_new_unit()
    
    elif user_choice == "3":
        search_units()
    
    elif user_choice == "4":
        sort_by_cost()
    
    elif user_choice == "5":
        sort_by_memory_storage()
    
    elif user_choice == "6":
        remove_by_identifier()
    
    elif user_choice == "7":
        remove_by_position()
    
    elif user_choice == "8":
        increase_memory()
    
    elif user_choice == "9":
        apply_sale()
    
    elif user_choice == "10":
        show_cost_extremes()
    
    elif user_choice == "11":
        filter_by_video()
    
    elif user_choice == "0":
        print("Программа завершена.")
        program_active = False
    
    else:
        print("Неверный выбор. Попробуйте снова.")
    
    if user_choice != "0":
        input("\nНажмите Enter, чтобы продолжить...")
        os.system("cls" if os.name == "nt" else "clear")
