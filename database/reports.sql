USE tourism_db;

-- 1) Total bookings and estimated revenue by destination
SELECT
    d.name AS destination,
    COUNT(b.id) AS total_bookings,
    COALESCE(SUM(b.guests), 0) AS total_guests,
    COALESCE(SUM(b.guests * d.price), 0) AS estimated_revenue
FROM destinations d
LEFT JOIN bookings b ON b.destination_id = d.id
GROUP BY d.id, d.name
ORDER BY estimated_revenue DESC;

-- 2) Booking status summary
SELECT
    status,
    COUNT(*) AS total
FROM bookings
GROUP BY status
ORDER BY total DESC;

-- 3) User-wise booking history and spend
SELECT
    u.full_name,
    u.email,
    COUNT(b.id) AS bookings_count,
    COALESCE(SUM(b.guests * d.price), 0) AS estimated_spend
FROM users u
LEFT JOIN bookings b ON b.user_id = u.id
LEFT JOIN destinations d ON d.id = b.destination_id
GROUP BY u.id, u.full_name, u.email
ORDER BY estimated_spend DESC;

-- 4) Upcoming travel plan list
SELECT
    b.id AS booking_id,
    u.full_name,
    d.name AS destination,
    b.travel_date,
    b.guests,
    b.status
FROM bookings b
JOIN users u ON u.id = b.user_id
JOIN destinations d ON d.id = b.destination_id
WHERE b.travel_date >= CURDATE()
ORDER BY b.travel_date ASC;

-- 5) Destination slot pressure (simple metric)
SELECT
    d.name,
    d.available_slots,
    COUNT(b.id) AS current_bookings,
    CASE
        WHEN d.available_slots = 0 THEN 'Sold Out'
        WHEN COUNT(b.id) >= d.available_slots THEN 'High Demand'
        ELSE 'Available'
    END AS slot_status
FROM destinations d
LEFT JOIN bookings b ON b.destination_id = d.id
GROUP BY d.id, d.name, d.available_slots
ORDER BY current_bookings DESC;
