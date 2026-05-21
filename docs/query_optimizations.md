# Query Optimization Notes

This document records optimization recommendations and examples for the project's SQL queries.

1) Pagination and COUNT optimization
- Current approach in `routes/destinations.py` builds a base query and uses `SELECT COUNT(*) FROM (base_query) AS filtered` to compute totals. For large datasets, prefer copying filters into a single `COUNT(*)` query (already used) and ensure filters use indexed columns.

2) Index usage
- Indexes present: `idx_users_email`, `idx_destinations_name`, `idx_destinations_location`, `idx_bookings_status`, `idx_bookings_travel_date`.
- Ensure queries that filter by `name`, `location`, or `travel_date` use these indexed columns in WHERE clauses (avoid functions on indexed columns which can prevent index usage).

3) JOINs and aggregates
- Reporting queries in `database/reports.sql` use LEFT JOINs where appropriate to include destinations/users with zero bookings.
- Use GROUP BY on primary keys (e.g., `d.id`) and include only needed columns in SELECT to reduce memory footprint.

4) EXPLAIN and profiling (example commands)
- To inspect query plans, run in MySQL Workbench or CLI:

```sql
EXPLAIN FORMAT=JSON
SELECT b.*, d.name AS destination_name
FROM bookings b
JOIN destinations d ON b.destination_id = d.id
WHERE b.user_id = 1
ORDER BY b.created_at DESC
LIMIT 5;
```

- Look for `using index` or `Using where; Using index` and ensure `possible_keys` includes the intended index.

5) Concurrency & transactions
- Mutating operations that affect `available_slots` should be executed inside transactions when done from application code. The schema includes triggers which perform updates atomically on the DB side; if converting to application-managed logic, wrap updates in transactions:

```sql
START TRANSACTION;
UPDATE destinations SET available_slots = available_slots - %s WHERE id = %s AND available_slots >= %s;
INSERT INTO bookings (...);
COMMIT;
```

6) Avoid subquery overhead
- For repeated computations, consider materialized views or precomputed aggregates if reporting on very large datasets.

7) Misc notes
- Monitor slow query log for long-running queries and add targeted indexes where necessary.
