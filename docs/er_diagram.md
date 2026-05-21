# ER Diagram & Conceptual Design

Below is the conceptual ER diagram for the Tourism Management System and a brief explanation of entities, attributes, and cardinalities.

```mermaid
erDiagram
    USERS {
        INT id PK
        VARCHAR full_name
        VARCHAR email UNIQUE
        VARCHAR password_hash
        TIMESTAMP created_at
    }
    ADMINS {
        INT id PK
        VARCHAR username UNIQUE
        VARCHAR password_hash
        TIMESTAMP created_at
    }
    DESTINATIONS {
        INT id PK
        VARCHAR name
        VARCHAR location
        TEXT description
        DECIMAL price
        VARCHAR image_path
        INT available_slots
        TIMESTAMP created_at
    }
    BOOKINGS {
        INT id PK
        INT user_id FK
        INT destination_id FK
        DATE travel_date
        INT guests
        TEXT notes
        ENUM status
        TIMESTAMP created_at
    }

    USERS ||--o{ BOOKINGS : makes
    ADMINS ||--o{ DESTINATIONS : manages
    DESTINATIONS ||--o{ BOOKINGS : receives
```

Entities & attributes
- Users: `id` (PK), `full_name`, `email` (unique), `password_hash`, `created_at`.
- Admins: `id` (PK), `username` (unique), `password_hash`, `created_at`.
- Destinations: `id` (PK), `name`, `location`, `description`, `price`, `image_path`, `available_slots`, `created_at`.
- Bookings: `id` (PK), `user_id` (FK -> users.id), `destination_id` (FK -> destinations.id), `travel_date`, `guests`, `notes`, `status`, `created_at`.

Relationships & cardinality
- A `User` can make zero or many `Bookings` (1-to-many): `USERS (1) ||--o{ BOOKINGS`.
- A `Destination` can have zero or many `Bookings` (1-to-many): `DESTINATIONS (1) ||--o{ BOOKINGS`.
- An `Admin` manages destinations and views bookings (modeled as 1-to-many for `DESTINATIONS`).

Constraints & business rules
- `users.email` is unique.
- `bookings.user_id` and `bookings.destination_id` are FK constraints with `ON DELETE CASCADE` in the DDL.
- CHECK constraints enforce `price >= 0`, `available_slots >= 0`, and `guests > 0`.
- Triggers (added in `database/schema.sql`) adjust `available_slots` atomically when bookings are confirmed, cancelled, or deleted; triggers raise an error if confirming would overbook.

Normalization
- Schema is normalized to 3NF: repeated information is factored into `users`, `destinations`, and `bookings` with appropriate PK/FK relationships.

Design rationale
- `bookings` stores denormalized derived values (like `guests`) required for accurate slot accounting and revenue calculations in reports; sums are computed in reporting queries rather than duplicating price.
- `available_slots` is stored on `destinations` for fast checks; triggers ensure consistency when bookings change status.
