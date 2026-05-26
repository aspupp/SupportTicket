import random
import pandas as pd
from datetime import datetime, timedelta

from Tickets import Ticket
from SupportDesk import SupportDesk
from TicketGenerator import TicketGenerator
from TicketAnalyzer import TicketAnalyzer
from SlaChart import SLAChart, SupportDeskAPI


# задача 1

print("задача 1: Создание тикетов и валидация")
t1 = Ticket("Сервер не отвечает", "critical")
t2 = Ticket("Принтер не печатает", "low", "in_progress")
t1.show()
t2.show()
print("\nСмена статусов")
t1.change_status("in_progress")
t1.change_status("closed")
t1.show_history()
print("\n--- Проверка валидации ---")
for title, priority, status, desc in [
    ("", "high", "open", "Пустое название"),
    ("Тест", "urgent", "open", "Неверный приоритет"),
    ("Тест", "low", "pending", "Неверный статус"),
]:
    try:
        Ticket(title, priority, status)
    except ValueError as e:
        print(f"[{desc}] Ошибка: {e}")
print("\nНедопустимые переходы")
t3 = Ticket("VPN не работает", "high")
try:
    t3.change_status("closed")
except ValueError as e:
    print(f"Ошибка: {e}")

#задача 2

print("задача 2: SupportDesk")
desk = SupportDesk()
desk.add_ticket("Сервер недоступен", "critical")
desk.add_ticket("Ошибка VPN", "high")
desk.add_ticket("Медленный Wi-Fi", "low")
desk.add_ticket("Нет звука на ПК", "medium", "in_progress")
desk.add_ticket("Обновление драйверов", "low", "closed")
desk.add_ticket("Критическая утечка данных", "critical")
desk.add_ticket("Сброс пароля", "medium")
desk.print_summary()
desk.print_list(desk.filter_by_status("open"), "Открытые тикеты")
desk.print_list(desk.filter_by_priority("critical"), "Критические тикеты")
desk.print_list(desk.get_sorted(by="priority"), "Сортировка по приоритету")
first_id = desk.tickets[0].id
desk.update_status(first_id, "in_progress")
desk.remove_ticket(desk.tickets[-1].id)

# задача 3
def main():
    print("ШАГ 1: Создание тестовых тикетов")
    ticket1 = Ticket(title="Сломалась оплата картой на сайте", priority="critical")
    ticket2 = Ticket(title="Добавить кнопку 'Выход' в меню", priority="low")
    ticket3 = Ticket(title="Долго грузится личный кабинет", priority="high")
    ticket1.change_status("in_progress")
    my_tickets = [ticket1, ticket2, ticket3]
    print(f"Создано тикетов: {len(my_tickets)}")
    for t in my_tickets:
        print(f"  {t}")
    print("\nШАГ 2: Фильтрация данных через TicketManager")
    manager = TicketGenerator(my_tickets)
    open_only = manager.get_open_tickets()
    print(f"Только открытые тикеты ({len(open_only)}):")
    for t in open_only:
        print(f"  {t}")
    print("\nШАГ 3: Экспорт данных в JSON-файл")
    manager.export_to_json("backup_tickets.json")
    print("\nШАГ 4: Импорт данных из JSON-файла")
    new_manager = TicketGenerator([])
    restored_tickets = new_manager.import_from_json("backup_tickets.json")
    print("\nШАГ 5: Проверка восстановленных данных")
    print("Список тикетов, прочитанных с жесткого диска:")
    for t in restored_tickets:
        print(f"  Восстановлен: {t}")
    print("задача 4: Pandas — groupby и время решения")
    print("\nАнализ данных с помощью Pandas")
    analyzer = TicketAnalyzer(my_tickets)
    print("\n1. Подсчет тикетов по приоритетам:")
    print(analyzer.group_by_priority())
    print("\n2. Сводная таблица (Приоритет х Статус):")
    print(analyzer.pivot_summary())
    print("\n3. Среднее время решения задач по приоритетам:")
    print(analyzer.avg_resolution_by_priority())
if __name__ == "__main__":
    main()

# задача 5

print("\nЗадача 5: График и FastAPI")

chart = SLAChart(desk.tickets)
chart.plot("sla_chart.png")

api = SupportDeskAPI(desk.tickets)
print("FastAPI приложение создано.")
print("Запуск: uvicorn main:api.app --reload")
print("Документация: http://127.0.0.1:8000/docs")

for route in api.app.routes:
    if hasattr(route, "methods"):
        print(f"  {list(route.methods)[0]:<6} {route.path}")