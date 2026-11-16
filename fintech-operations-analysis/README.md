# Fintech Operations Analysis | SQL + Python

A small, reproducible **strategy & operations** case study: find friction in a fictional digital-payments process, prioritise opportunities and turn data into a testable action plan.

**Status:** Educational portfolio example · **Dataset:** 100% synthetic · **Tools:** Python, SQLite/SQL, CSV · **No external packages required**

> This project is an AI-assisted learning exercise that I am reviewing and developing. The data are entirely fictional. It is **not** a Revolut project, does **not** represent any employer's performance and contains **no real customer data**.

## Business question

**Where should a fintech operations team investigate payment failure and support friction first, and how would we measure improvement?**

The case focuses on three operational decisions:

1. **Spot the problem:** Compare payment approval rates across countries and payment channels.
2. **Prioritise:** Examine decline reasons and support handling to avoid optimising a single metric at the expense of reliability or risk.
3. **Propose an experiment:** Frame a hypothetical improvement scenario with suitable guardrails.

## Quick results

See the [full diagnostic report](reports/analysis.md) with the generated metrics, segment table and recommendations.

## Structure

```text
fintech-operations-analysis/
├── README.md                   This guide and decision framework
├── data/
│   ├── payments.csv            4,800 invented payment attempts
│   └── support_tickets.csv     Invented support tickets
├── sql/analysis.sql            Five editable analytical SQL queries
├── src/
│   ├── generate_data.py        Deterministic sample data creation
│   └── analyze.py              SQLite analysis and Markdown report
├── reports/analysis.md         Example output and recommendations
├── tests/test_analysis.py      Reproducibility and data checks
└── .github/workflows/tests.yml Automated tests
```

## Run locally

Requires **Python 3.10+**, with no external dependencies.

```bash
python src/generate_data.py
python src/analyze.py
python -m unittest discover -s tests -v
```

The report is written to `reports/analysis.md`. The query file in `sql/analysis.sql` can be executed separately against the same data after importing the CSVs into SQLite.

## Key metrics

| Metric | Definition | Why it matters |
|---|---|---|
| Approval rate | Approved attempts / all attempts | Conversion / customer friction |
| Technical declines | Declines tagged `technical_error` | Possible operational fixes |
| Support contact rate | Payment attempts with a support ticket / attempts | Cost to serve and customer friction |
| Resolution within 24h | Tickets closed within 24 hours / tickets | Customer experience and speed |

## Suggested operating plan

- **Diagnose:** Check trends by market/channel and assess denominator sizes. Segment first; avoid decisions on global averages alone.
- **Validate:** Review routing and external network or issuer error classifications before changing the payment funnel.
- **Pilot:** Choose a narrow, controlled intervention; define success metrics before rollout.
- **Guardrail:** Monitor fraud losses, compliance risk, payment latency and ticket volumes — improved approval alone is insufficient.
- **Scale cautiously:** Roll out only after confirming stability and statistically meaningful results.

## Limits

This is an **illustrative simulation**, so unusual differences in the dataset were intentionally designed for practice. There is no basis for inference about real companies or payment rails. Real operations require privacy protection, risk/compliance approval, real event definitions, and experimental validation. The +3 percentage-point sensitivity scenario in the report is an assumption, not an achieved outcome.

## Next improvements

- Add true 7-day and 30-day time-series monitoring.
- Design a causal A/B test with sample-size and guardrail analysis.
- Add an exploratory SQL workbook and a lightweight dashboard.

---

*Intended for a graduate-level business analytics and operations portfolio.*
