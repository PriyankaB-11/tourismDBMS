CREATE DATABASE IF NOT EXISTS tourism_db;
USE tourism_db;

DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS destinations;
DROP TABLE IF EXISTS admins;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_users_email (email)
);

CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE destinations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    location VARCHAR(120) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    image_path VARCHAR(255),
    available_slots INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_dest_price_non_negative CHECK (price >= 0),
    CONSTRAINT chk_dest_slots_non_negative CHECK (available_slots >= 0),
    INDEX idx_destinations_name (name),
    INDEX idx_destinations_location (location)
);

CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    destination_id INT NOT NULL,
    travel_date DATE NOT NULL,
    guests INT NOT NULL DEFAULT 1,
    notes TEXT,
    status ENUM('Pending', 'Confirmed', 'Cancelled', 'Completed') NOT NULL DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_bookings_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_bookings_destination FOREIGN KEY (destination_id) REFERENCES destinations(id) ON DELETE CASCADE,
    CONSTRAINT chk_bookings_guests_positive CHECK (guests > 0),
    INDEX idx_bookings_user_id (user_id),
    INDEX idx_bookings_destination_id (destination_id),
    INDEX idx_bookings_status (status),
    INDEX idx_bookings_travel_date (travel_date)
);

INSERT INTO admins (username, password_hash) VALUES
('admin', 'scrypt:32768:8:1$kiOJRc0eECMvcx6r$923cbf85de070293c52b1a18eee3663f96354f744d5635921632af475356a0b1dcb9c815a476bac75ba820501cedfab01ef3b64e5fd2e5a3072cc738a1403c7d');

INSERT INTO users (full_name, email, password_hash) VALUES
('Aarav Sharma', 'aarav@example.com', 'scrypt:32768:8:1$DntT3Qrn2UmvH5bH$b42fa5ebdfb089429e928c49839875f7ba5acbe9b1a1ed514c2dd1c0692fe2a690fcbe60400996e13df69ad3a784bdbbdc39817e5353c62983a71dfd002fae47'),
('Meera Patel', 'meera@example.com', 'scrypt:32768:8:1$0l1Lzp8tcSe5ngUL$be3cd07a7af9888caf76eab4b9f6b3c158d453e1044e89096276258e9d741e37bd62ee7170a166deb427cf4561f4a36f1eb825e01e66631bd617ca8a72474e9a');

INSERT INTO destinations (name, location, description, price, image_path, available_slots) VALUES
('Goa Beach Escape', 'Goa, India', 'Sun, sand, water sports, and a relaxed coastal experience.', 14999.00, 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80', 25),
('Jaipur Heritage Tour', 'Jaipur, India', 'Explore forts, palaces, and local markets in the Pink City.', 9999.00, 'https://images.unsplash.com/photo-1549880338-65ddcdfd017b?auto=format&fit=crop&w=1200&q=80', 18),
('Kerala Backwaters', 'Alleppey, India', 'A calm houseboat journey through lush backwaters.', 12999.00, 'https://images.unsplash.com/photo-1505765053452-4a3f86a0c3c8?auto=format&fit=crop&w=1200&q=80', 12);

INSERT INTO bookings (user_id, destination_id, travel_date, guests, notes, status) VALUES
(1, 1, '2026-06-15', 2, 'Window seat if available.', 'Confirmed'),
(2, 2, '2026-07-10', 4, 'Family trip.', 'Pending');

DELIMITER $$

-- Trigger: Prevent confirming a booking if not enough available slots
CREATE TRIGGER trg_bookings_before_update
BEFORE UPDATE ON bookings
FOR EACH ROW
BEGIN
    -- When changing status to Confirmed, ensure destination has enough slots and decrement
    IF NEW.status = 'Confirmed' AND OLD.status <> 'Confirmed' THEN
        IF (SELECT available_slots FROM destinations WHERE id = NEW.destination_id) < NEW.guests THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Not enough available slots to confirm booking';
        ELSE
            UPDATE destinations SET available_slots = available_slots - NEW.guests WHERE id = NEW.destination_id;
        END IF;
    -- When moving away from Confirmed, restore previously reserved slots
    ELSIF OLD.status = 'Confirmed' AND NEW.status <> 'Confirmed' THEN
        UPDATE destinations SET available_slots = available_slots + OLD.guests WHERE id = OLD.destination_id;
    END IF;
END$$

-- Trigger: If a confirmed booking is deleted, restore slots
CREATE TRIGGER trg_bookings_before_delete
BEFORE DELETE ON bookings
FOR EACH ROW
BEGIN
    IF OLD.status = 'Confirmed' THEN
        UPDATE destinations SET available_slots = available_slots + OLD.guests WHERE id = OLD.destination_id;
    END IF;
END$$

DELIMITER ;
