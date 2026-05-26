import uuid
from datetime import datetime
#1-3
class Ticket:
    VALID_STATUSES = ["open", "in_progress", "closed"]
    VALID_PRIORITIES = ["low", "medium", "high", "critical"]
    ALLOWED_TRANSITIONS = {
        "open": ["in_progress"],
        "in_progress": ["closed"],
        "closed": []
    }
    def __init__(self, title, priority, status="open"):
        if not title or not title.strip():
            raise ValueError("Название тикета не может быть пустым.")
        if len(title) > 100:
            raise ValueError("Название не должно превышать 100 символов.")
        if priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Неверный приоритет: '{priority}'. Допустимые: {self.VALID_PRIORITIES}")
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Неверный статус: '{status}'. Допустимые: {self.VALID_STATUSES}")
        self.id = str(uuid.uuid4())[:8]
        self.title = title
        self.priority = priority
        self.status = status
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history = [f"{self.created_at} — создан со статусом '{status}'"]
    def change_status(self, new_status):
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Неверный статус: '{new_status}'")
        allowed = self.ALLOWED_TRANSITIONS[self.status]
        if new_status not in allowed:
            raise ValueError(
                f"Переход '{self.status}' → '{new_status}' запрещён. "
                f"Допустимые: {allowed if allowed else 'нет'}"
            )
        old_status = self.status
        self.status = new_status
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"{timestamp} — статус изменён: '{old_status}' → '{new_status}'")
    def show(self):
        print(f"Тикет #{self.id}")
        print(f"  Название:  {self.title}")
        print(f"  Приоритет: {self.priority}")
        print(f"  Статус:    {self.status}")
        print(f"  Создан:    {self.created_at}")
    def show_history(self):
        print(f"История тикета #{self.id}:")
        for entry in self.history:
            print(f"  {entry}")
    def __repr__(self):
        return f"[#{self.id}] {self.title} | {self.priority} | {self.status}"