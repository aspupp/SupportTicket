import matplotlib.pyplot as plt
from fastapi import FastAPI, Query
from typing import Optional
from Tickets import Ticket
#13-14

class SLAChart:
    SLA_HOURS = {"critical": 4, "high": 12, "medium": 24, "low": 48}

    def __init__(self, tickets):
        self.tickets = tickets

    def plot(self, save_path="sla_chart.png"):
        priority_order = ["critical", "high", "medium", "low"]
        colors = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71"]

        counts = {}
        for p in priority_order:
            counts[p] = 0
        for t in self.tickets:
            if t.priority in counts:
                counts[t.priority] += 1

        priorities = list(counts.keys())
        values = list(counts.values())

        plt.figure(figsize=(8, 5))
        plt.bar(priorities, values, color=colors)
        plt.title("Количество тикетов по приоритетам")
        plt.xlabel("Приоритет")
        plt.ylabel("Количество")
        plt.grid(axis="y", linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
        plt.show()
        print(f"График сохранён: {save_path}")


class SupportDeskAPI:
    def __init__(self, tickets):
        self.tickets = tickets
        self.app = FastAPI(title="Support Desk API")
        self._register_routes()

    def _to_dict(self, t):
        return {
            "id": t.id,
            "title": t.title,
            "priority": t.priority,
            "status": t.status,
            "created_at": t.created_at
        }

    def _register_routes(self):
        tickets = self.tickets

        @self.app.get("/tickets")
        def get_tickets(
            status: Optional[str] = Query(None),
            priority: Optional[str] = Query(None)
        ):
            result = []
            for t in tickets:
                if status and t.status != status:
                    continue
                if priority and t.priority != priority:
                    continue
                result.append(self._to_dict(t))
            return {"count": len(result), "tickets": result}

        @self.app.get("/tickets/{ticket_id}")
        def get_ticket(ticket_id: str):
            for t in tickets:
                if t.id == ticket_id:
                    return self._to_dict(t)
            return {"error": f"Тикет #{ticket_id} не найден"}

        @self.app.get("/report")
        def get_report():
            by_status = {}
            by_priority = {}
            for t in tickets:
                by_status[t.status] = by_status.get(t.status, 0) + 1
                by_priority[t.priority] = by_priority.get(t.priority, 0) + 1
            return {
                "total": len(tickets),
                "by_status": by_status,
                "by_priority": by_priority
            }