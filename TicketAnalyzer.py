import pandas as pd
from Tickets import Ticket
#9-12

class TicketAnalyzer:
    def __init__(self, tickets):
        rows = []
        for t in tickets:
            row = {
                "id": t.id,
                "title": t.title,
                "priority": t.priority,
                "status": t.status,
                "created_at": t.created_at,
                "resolution_hours": getattr(t, "resolution_hours", None),
            }
            rows.append(row)
        self.df = pd.DataFrame(rows)
    def group_by_priority(self):
        grouped = self.df.groupby("priority")["id"].count()
        return grouped
    def group_by_status(self):
        grouped = self.df.groupby("status")["id"].count()
        return grouped
    def avg_resolution_by_priority(self):
        closed_tickets = self.df[self.df["status"] == "closed"]
        if closed_tickets.empty:
            return "Нет закрытых тикетов для анализа"
        result = closed_tickets.groupby("priority")["resolution_hours"].mean()
        return result.round(1)
    def pivot_summary(self):
        return pd.crosstab(
            self.df["priority"],
            self.df["status"],
            margins=True,
            margins_name="Итого",
        )