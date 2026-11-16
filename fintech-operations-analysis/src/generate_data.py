"""Generate deterministic, entirely fictional fintech operations sample data."""
from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKETS = ("ES", "PT", "UK", "PL")
CHANNELS = ("card_online", "bank_transfer")


def generate(seed: int = 2027, n: int = 4800) -> tuple[int, int]:
    rng = random.Random(seed)
    (ROOT / "data").mkdir(exist_ok=True)
    payments = []
    tickets = []
    for i in range(n):
        market = rng.choices(MARKETS, weights=(36, 20, 28, 16))[0]
        channel = rng.choices(CHANNELS, weights=(72, 28))[0]
        month_offset = rng.randrange(92)
        created_date = (date(2026, 7, 1) + timedelta(days=month_offset)).isoformat()
        p = 0.945 if channel == "bank_transfer" else 0.922
        if market == "ES" and channel == "card_online":
            p -= 0.105  # deliberately weak segment for a diagnosis exercise
        if market == "PT" and channel == "card_online":
            p -= 0.032
        approved = rng.random() < p
        result = "approved" if approved else "declined"
        reason = "" if approved else rng.choices(
            ("insufficient_funds", "risk_check", "technical_error", "other"),
            weights=(42, 23 if market != "ES" else 14, 15 if market != "ES" else 31, 20 if market != "ES" else 13),
        )[0]
        settlement_hours = "" if not approved else round(max(0.5, rng.gauss(11 if channel == "bank_transfer" else 6, 3.4)), 1)
        payment_id = f"P{i+1:05d}"
        payments.append({
            "payment_id": payment_id,
            "date": created_date,
            "market": market,
            "channel": channel,
            "amount_eur": f"{rng.uniform(8, 350):.2f}",
            "status": result,
            "decline_reason": reason,
            "settlement_hours": settlement_hours,
        })
        contact_prob = 0.17 if not approved else 0.055
        if rng.random() < contact_prob:
            resolution_hours = round(max(0.3, rng.lognormvariate(2.2, 0.76)), 1)
            ticket_id = f"T{len(tickets)+1:05d}"
            tickets.append({
                "ticket_id": ticket_id,
                "payment_id": payment_id,
                "category": "payment_declined" if not approved else rng.choice(("payment_status", "settlement_query", "other")),
                "resolution_hours": resolution_hours,
                "escalated": int(rng.random() < (0.29 if not approved else 0.11)),
            })

    for filename, rows in (("payments.csv", payments), ("support_tickets.csv", tickets)):
        with (ROOT / "data" / filename).open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
    return len(payments), len(tickets)


if __name__ == "__main__":
    p, t = generate()
    print(f"Generated {p} synthetic payments and {t} tickets")
