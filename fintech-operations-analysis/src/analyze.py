"""Reproducible SQL-driven diagnostic report over fictional operations data."""
from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_csv(conn: sqlite3.Connection, table: str, filename: str, schema: str) -> None:
    conn.execute(f"CREATE TABLE {table} ({schema})")
    with (ROOT / "data" / filename).open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        keys = reader.fieldnames
        assert keys is not None
        placeholders = ",".join("?" for _ in keys)
        conn.executemany(f"INSERT INTO {table} ({','.join(keys)}) VALUES ({placeholders})",
                         ([row[k] if row[k] != "" else None for k in keys] for row in reader))
    conn.commit()


def build_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    load_csv(conn, "payments", "payments.csv",
             "payment_id TEXT PRIMARY KEY, date TEXT, market TEXT, channel TEXT, "
             "amount_eur REAL, status TEXT, decline_reason TEXT, settlement_hours REAL")
    load_csv(conn, "support_tickets", "support_tickets.csv",
             "ticket_id TEXT PRIMARY KEY, payment_id TEXT, category TEXT, "
             "resolution_hours REAL, escalated INTEGER")
    return conn


def rows_as_markdown(rows: list[sqlite3.Row]) -> str:
    if not rows:
        return "_(No data)_"
    keys = list(rows[0].keys())
    lines = ["| " + " | ".join(keys) + " |", "| " + " | ".join("---" for _ in keys) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[k]) if row[k] is not None else "—" for k in keys) + " |")
    return "\n".join(lines)


def run() -> dict:
    conn = build_db()
    summary = conn.execute("""SELECT COUNT(*) AS payments,
                ROUND(100.0 * AVG(CASE WHEN status='approved' THEN 1.0 ELSE 0.0 END),2) AS approval_pct,
                ROUND(SUM(amount_eur), 2) AS attempted_value_eur
                FROM payments""").fetchone()
    segments = conn.execute("""SELECT market, channel, COUNT(*) AS payments,
                ROUND(100.0 * AVG(CASE WHEN status='approved' THEN 1.0 ELSE 0.0 END),2) AS approval_pct
                FROM payments GROUP BY market, channel ORDER BY approval_pct, payments DESC""").fetchall()
    reasons = conn.execute("""SELECT decline_reason, COUNT(*) AS declines
                FROM payments WHERE status='declined'
                GROUP BY decline_reason ORDER BY declines DESC""").fetchall()
    support = conn.execute("""SELECT COUNT(*) AS tickets,
                ROUND(AVG(resolution_hours), 2) AS mean_resolution_hours,
                ROUND(100.0 * AVG(CASE WHEN resolution_hours <= 24 THEN 1.0 ELSE 0.0 END),2)
                AS within_24h_pct
                FROM support_tickets""").fetchone()
    weak = segments[0]
    # Scenario is a hypothetical management sensitivity, NOT measured causation.
    hypothetical_extra_approvals = round(weak["payments"] * 0.03)
    report = f"""# Operational diagnostics — synthetic sample

> **Important:** This is a self-directed educational project. All payment and support records are generated, fictional data. It does not describe Revolut, any employer, or actual customers. No real business results are claimed.

## Executive summary

- **{summary['payments']:,}** sample payment attempts; **{summary['approval_pct']}%** approved.
- **€{summary['attempted_value_eur']:,.0f}** attempted payment value (not revenue).
- **{support['tickets']}** simulated customer support tickets; **{support['within_24h_pct']}%** resolved within 24 hours.
- Lowest-approval segment: **{weak['market']} / {weak['channel']} ({weak['approval_pct']}%, n={weak['payments']})**.

## Segment comparison

{rows_as_markdown(segments)}

## Decline reasons

{rows_as_markdown(reasons)}

## Business recommendations

1. **Investigate the low-approval segment first.** Compare technical decline logs, payment routing, and issuer feedback for the weakest market/channel combination. The pattern is *diagnostic*, not evidence of root cause.
2. **Prioritise actionable failures.** Separate technical issues from risk or insufficient-funds declines before changing any payment process; protect fraud controls and compliance.
3. **Set up operational guardrails.** Track approval rates alongside loss/fraud indicators, customer contact rate, and support resolution time. Run controlled experiments before scaling changes.
4. **Estimate upside conservatively.** A hypothetical **+3 percentage point** increase in the weakest segment, holding volume constant, implies roughly **{hypothetical_extra_approvals} additional approved transactions** in this sample. This is *not* a forecast or a claim that the improvement is achievable.

## Method and limitations

- Generated in Python using a fixed random seed; analysed using SQL/SQLite.
- Sample period: July–September 2026; data and patterns were deliberately simulated.
- Approval rate = approved attempts / all attempts in the segment.
- No customer identifiers, personal data, causal inference, experimental validation, or actual fintech performance data.
- Small segment samples and selection effects may alter rankings; further validation would be required in real operations.

## How to reproduce

```bash
python src/generate_data.py
python src/analyze.py
python -m unittest discover -s tests -v
```
"""
    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "reports" / "analysis.md").write_text(report, encoding="utf-8")
    conn.close()
    return {"payments": summary["payments"], "approval_pct": summary["approval_pct"],
            "weakest_market": weak["market"], "weakest_channel": weak["channel"],
            "tickets": support["tickets"]}


if __name__ == "__main__":
    print(run())
