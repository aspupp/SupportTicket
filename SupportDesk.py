from Tickets import Ticket
#4-6
class SupportDesk:
    def __init__(self):
        self.tickets = []
    def add_ticket(self, title, priority, status="open"):
        ticket = Ticket(title, priority, status)
        self.tickets.append(ticket)
        return ticket
    def get_ticket(self, ticket_id):
        for ticket in self.tickets:
            if ticket.id == ticket_id:
                return ticket
        return None
    def update_status(self, ticket_id, new_status):
        ticket = self.get_ticket(ticket_id)
        if ticket is None:
            print(f"Тикет #{ticket_id} не найден.")
            return
        ticket.change_status(new_status)
    def remove_ticket(self, ticket_id):
        for i, t in enumerate(self.tickets):
            if t.id == ticket_id:
                return self.tickets.pop(i)
        return None
    def filter_by_status(self, status):
        return [t for t in self.tickets if t.status == status]
    def filter_by_priority(self, priority):
        return [t for t in self.tickets if t.priority == priority]
    def search_by_title(self, keyword):
        return [t for t in self.tickets if keyword.lower() in t.title.lower()]
    def get_sorted(self, by="priority"):
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        if by == "priority":
            return sorted(self.tickets, key=lambda t: priority_order.get(t.priority, 9))
        elif by == "status":
            return sorted(self.tickets, key=lambda t: t.status)
        return self.tickets
    def count_by_status(self):
        counts = {s: 0 for s in Ticket.VALID_STATUSES}
        for t in self.tickets:
            counts[t.status] += 1
        return counts
    def count_by_priority(self):
        counts = {p: 0 for p in Ticket.VALID_PRIORITIES}
        for t in self.tickets:
            counts[t.priority] += 1
        return counts
    def print_summary(self):
        print("СВОДКА ТЕХПОДДЕРЖКИ")
        print(f"Всего тикетов: {len(self.tickets)}")
        print("\nПо статусам:")
        for status, count in self.count_by_status().items():
            print(f"  {status:<14}: {count}")
        print("\nПо приоритетам:")
        for priority, count in self.count_by_priority().items():
            print(f"  {priority:<10}: {count}  {'#' * count}")
    def print_list(self, tickets=None, label="Тикеты"):
        items = tickets if tickets is not None else self.tickets
        print(f"\n{label} ({len(items)})")
        if not items:
            print("  Пусто.")
        for t in items:
            print(f"  {t}")