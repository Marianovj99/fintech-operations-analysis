# Operational diagnostics — synthetic sample

> **Important:** This is a self-directed educational project. All payment and support records are generated, fictional data. It does not describe Revolut, any employer, or actual customers. No real business results are claimed.

## Executive summary

- **4,800** sample payment attempts; **89.83%** approved.
- **€846,317** attempted payment value (not revenue).
- **312** simulated customer support tickets; **89.74%** resolved within 24 hours.
- Lowest-approval segment: **ES / card_online (83.09%, n=1301)**.

## Segment comparison

| market | channel | payments | approval_pct |
| --- | --- | --- | --- |
| ES | card_online | 1301 | 83.09 |
| PT | card_online | 684 | 90.06 |
| PL | card_online | 542 | 91.7 |
| UK | card_online | 973 | 91.88 |
| PL | bank_transfer | 205 | 92.2 |
| ES | bank_transfer | 477 | 93.71 |
| UK | bank_transfer | 370 | 95.14 |
| PT | bank_transfer | 248 | 95.16 |

## Decline reasons

| decline_reason | declines |
| --- | --- |
| insufficient_funds | 219 |
| technical_error | 115 |
| risk_check | 85 |
| other | 69 |

## Business recommendations

1. **Investigate the low-approval segment first.** Compare technical decline logs, payment routing, and issuer feedback for the weakest market/channel combination. The pattern is *diagnostic*, not evidence of root cause.
2. **Prioritise actionable failures.** Separate technical issues from risk or insufficient-funds declines before changing any payment process; protect fraud controls and compliance.
3. **Set up operational guardrails.** Track approval rates alongside loss/fraud indicators, customer contact rate, and support resolution time. Run controlled experiments before scaling changes.
4. **Estimate upside conservatively.** A hypothetical **+3 percentage point** increase in the weakest segment, holding volume constant, implies roughly **39 additional approved transactions** in this sample. This is *not* a forecast or a claim that the improvement is achievable.

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
