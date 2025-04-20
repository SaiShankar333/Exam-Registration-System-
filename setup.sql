-- Create the database
CREATE DATABASE IF NOT EXISTS exam_system;
USE exam_system;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15),
    role ENUM('student', 'admin'),
    wallet DECIMAL(10,2) DEFAULT 500
);

-- Exams table
CREATE TABLE IF NOT EXISTS exams (
    exam_id INT AUTO_INCREMENT PRIMARY KEY,
    subject VARCHAR(100),
    cost DECIMAL(10,2) DEFAULT 100
);

-- Registrations table
CREATE TABLE IF NOT EXISTS registrations (
    registration_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    exam_id INT,
    registration_date DATE NOT NULL,
    status ENUM('active', 'cancelled') DEFAULT 'active',
    cancel_reason TEXT DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (exam_id) REFERENCES exams(exam_id)
);

-- Cancellation records table
CREATE TABLE IF NOT EXISTS exam_cancellations (
    cancellation_id INT AUTO_INCREMENT PRIMARY KEY,
    registration_id INT,
    reason VARCHAR(255),
    cancelled_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (registration_id) REFERENCES registrations(registration_id)
);

-- Insert subjects
INSERT INTO exams (subject) VALUES 
('Engineering Maths'), 
('Applied Mathematics'), 
('Physics'), 
('Chemistry'), 
('Python Programming'), 
('French-1'),
('German-1'), 
('Spanish-1'), 
('CSS');

