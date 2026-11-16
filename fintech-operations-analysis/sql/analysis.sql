-- All rows are simulated; queries are SQLite-compatible.
-- 1. Approval rates and volume by market and payment channel
SELECT market, channel,
       COUNT(*) AS payments,
       SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END) AS approvals,
       ROUND(100.0 * AVG(CASE WHEN status = 'approved' THEN 1.0 ELSE 0.0 END), 2) AS approval_pct
FROM payments
GROUP BY market, channel
ORDER BY approval_pct ASC, payments DESC;

-- 2. Breakdown of declined payments, including actionable technical errors
SELECT market, channel, decline_reason,
       COUNT(*) AS declined_payments
FROM payments
WHERE status = 'declined'
GROUP BY market, channel, decline_reason
ORDER BY declined_payments DESC;

-- 3. Contact rate by customer payment segment
SELECT p.market, p.channel,
       COUNT(*) AS payment_count,
       COUNT(t.ticket_id) AS ticket_count,
       ROUND(100.0 * COUNT(t.ticket_id) / COUNT(*), 2) AS contact_pct
FROM payments p
LEFT JOIN support_tickets t ON p.payment_id = t.payment_id
GROUP BY p.market, p.channel
ORDER BY contact_pct DESC;

-- 4. Service quality measures
SELECT COUNT(*) AS tickets,
       ROUND(AVG(resolution_hours), 2) AS mean_resolution_hours,
       ROUND(100.0 * AVG(CASE WHEN resolution_hours <= 24 THEN 1.0 ELSE 0.0 END), 2) AS resolved_within_24h_pct,
       ROUND(100.0 * AVG(escalated), 2) AS escalation_pct
FROM support_tickets;

-- 5. Monthly trend; useful for distinguishing durable patterns from one-off events
SELECT SUBSTR(date, 1, 7) AS month,
       COUNT(*) AS payment_count,
       ROUND(100.0 * AVG(CASE WHEN status = 'approved' THEN 1.0 ELSE 0.0 END), 2) AS approval_pct
FROM payments
GROUP BY SUBSTR(date, 1, 7)
ORDER BY month;
