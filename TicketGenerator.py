import json
from datetime import datetime
from Tickets import Ticket
#7-8
class TicketGenerator:
    def __init__(self, tickets_list):
        self.tickets = tickets_list
    def get_open_tickets(self):
        result = []
        for t in self.tickets:
            if t.status == "open":
                result.append(t)
        return result
    def get_tickets_by_priority(self, priority):
        result = []
        for t in self.tickets:
            if t.priority == priority:
                result.append(t)
        return result
    def export_to_json(self, filepath="tickets.json"):
        simple_list = []
        for t in self.tickets:
            dict_format = {
                "id": t.id,
                "title": t.title,
                "priority": t.priority,
                "status": t.status,
                "created_at": t.created_at,
            }
            simple_list.append(dict_format)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(simple_list, f, ensure_ascii=False, indent=4)
        print(f"Успешно сохранено {len(simple_list)} тикетов в файл {filepath}")
    def import_from_json(self, filepath="tickets.json"):
        with open(filepath, "r", encoding="utf-8") as f:
            file_data = json.load(f)
        loaded_tickets = []
        for item in file_data:
            t = Ticket(item["title"], item["priority"], item["status"])
            t.id = item["id"]
            t.created_at = item["created_at"]
            loaded_tickets.append(t)
        print(f"Успешно загружено {len(loaded_tickets)} тикетов из файла")
        return loaded_tickets