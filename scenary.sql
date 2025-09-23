DROP DATABASE IF EXISTS online_banking;
CREATE DATABASE IF NOT EXISTS online_banking;
USE online_banking;

-- Скидання таблиць
DROP TABLE IF EXISTS transactionsaccounts;
DROP TABLE IF EXISTS status_transactions;
DROP TABLE IF EXISTS payment_templates;
DROP TABLE IF EXISTS needs;
DROP TABLE IF EXISTS fees;
DROP TABLE IF EXISTS cards;
DROP TABLE IF EXISTS authorizations;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS transactions;

-- Створення таблиць
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(50) NOT NULL,
    email VARCHAR(50),
    phone VARCHAR(15)
);

CREATE TABLE accounts (
    account_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    account_number VARCHAR(20) NOT NULL,
    balance DECIMAL(15, 2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    amount DECIMAL(15, 2) NOT NULL,
    transaction_date DATE NOT NULL
);

CREATE TABLE TransactionsAccounts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT,
    transaction_id INT,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id) ON DELETE CASCADE
);

CREATE TABLE payment_templates (
    template_id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT,
    template_name VARCHAR(50) NOT NULL,
    template_details TEXT,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
);

CREATE TABLE cards (
    card_id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT,
    card_number VARCHAR(20) NOT NULL,
    card_type VARCHAR(50),
    expiry_date DATE,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
);

CREATE TABLE needs (
    need_id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_id INT UNIQUE,
    service_name VARCHAR(100),
    payment_date DATE,
    description TEXT,
    category VARCHAR(50),
    priority INT,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id) ON DELETE CASCADE
);

CREATE TABLE authorizations (
    auth_id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT,
    login_time TIMESTAMP,
    logout_time TIMESTAMP,
    password VARCHAR(100) NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
);

CREATE TABLE fees (
    fee_id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_id INT UNIQUE, -- обмеження для зв'язку один до одного
    fee_amount DECIMAL(15, 2),
    fee_date DATE,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id) ON DELETE CASCADE
);

CREATE TABLE status_transactions (
    status_id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_id INT UNIQUE, -- обмеження для зв'язку один до одного
    status VARCHAR(50),
    status_date DATE,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id) ON DELETE CASCADE
);


-- тригер
CREATE TABLE logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT NOT NULL,
    log_action VARCHAR(100),
    log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Заповнення таблиць
INSERT INTO customers (customer_name, email, phone) VALUES 
('Customer 1', 'customer1@mail.com', '+380981234567'),
('Customer 2', 'customer2@mail.com', '+380982345678'),
('Customer 3', 'customer3@mail.com', '+380983456789'),
('Customer 4', 'customer4@mail.com', '+380984567890'),
('Customer 5', 'customer5@mail.com', '+380985678901'),
('Customer 6', 'customer6@mail.com', '+380986789012'),
('Customer 7', 'customer7@mail.com', '+380987890123'),
('Customer 8', 'customer8@mail.com', '+380988901234'),
('Customer 9', 'customer9@mail.com', '+380989012345'),
('Customer 10', 'customer10@mail.com', '+380990123456'),
('Customer 11', 'customer11@mail.com', '+380991234567'),
('Customer 12', 'customer12@mail.com', '+380992345678');

INSERT INTO accounts (customer_id, account_number, balance) VALUES 
(1, 'ACC10001', 5000.00),
(2, 'ACC10002', 3000.50),
(3, 'ACC10003', 7500.75),
(4, 'ACC10004', 12000.20),
(5, 'ACC10005', 4500.00),
(6, 'ACC10006', 8200.00),
(7, 'ACC10007', 9600.50),
(8, 'ACC10008', 11050.30),
(9, 'ACC10009', 6200.75),
(10, 'ACC10010', 3700.60),
(11, 'ACC10011', 5400.40),
(12, 'ACC10012', 2500.90),
(1, 'ACC20001', '10000.00'),
(1, 'ACC20002', '3000.00'),
(2, 'ACC30012', 2500.90),
(3, 'ACC50001', '10000.00'),
(4, 'ACC30002', '3000.00');


INSERT INTO transactions (amount, transaction_date) VALUES 
(150.75, '2024-01-10'),
(200.00, '2024-02-15'),
(500.50, '2024-03-20'),
(320.25, '2024-04-25'),
(410.00, '2024-05-30'),
(650.75, '2024-06-10'),
(220.00, '2024-07-15'),
(530.50, '2024-08-20'),
(380.25, '2024-09-25'),
(490.00, '2024-10-30'),
(310.75, '2024-11-10'),
(560.50, '2024-12-15');

INSERT INTO TransactionsAccounts (account_id, transaction_id) VALUES 
(1, 2),
(2, 1),
(3, 5),
(4, 5),
(5, 1),
(6, 3),
(7, 4),
(8, 6),
(9, 7),
(10, 8),
(11, 9),
(12, 10),
(12, 2),
(5, 3),
(5, 6);

INSERT INTO payment_templates (account_id, template_name, template_details) VALUES 
(1, 'Template 1', 'Details of template 1'),
(2, 'Template 2', 'Details of template 2'),
(3, 'Template 3', 'Details of template 3'),
(4, 'Template 4', 'Details of template 4'),
(5, 'Template 5', 'Details of template 5'),
(6, 'Template 6', 'Details of template 6'),
(7, 'Template 7', 'Details of template 7'),
(8, 'Template 8', 'Details of template 8'),
(9, 'Template 9', 'Details of template 9'),
(10, 'Template 10', 'Details of template 10'),
(11, 'Template 11', 'Details of template 11'),
(12, 'Template 12', 'Details of template 12');

INSERT INTO cards (account_id, card_number, card_type, expiry_date) VALUES 
(1, '1234567890123456', 'Credit', '2026-12-31'),
(2, '2345678901234567', 'Debit', '2025-11-30'),
(3, '3456789012345678', 'Credit', '2027-10-29'),
(4, '4567890123456789', 'Debit', '2024-09-28'),
(5, '5678901234567890', 'Credit', '2028-08-27'),
(6, '6789012345678901', 'Debit', '2027-07-15'),
(7, '7890123456789012', 'Credit', '2026-06-20'),
(8, '8901234567890123', 'Debit', '2025-05-25'),
(9, '9012345678901234', 'Credit', '2029-04-30'),
(10, '0123456789012345', 'Debit', '2024-03-15'),
(11, '1234567890123457', 'Credit', '2026-02-12'),
(12, '2345678901234568', 'Debit', '2025-01-10');

INSERT INTO needs (transaction_id, service_name, payment_date, description, category, priority) VALUES 
(1, 'Electricity Bill', '2024-01-15', 'Monthly electricity payment', 'Utility', 1),
(2, 'Internet Bill', '2024-02-20', 'Internet service payment', 'Utility', 2),
(3, 'Water Bill', '2024-03-25', 'Water supply payment', 'Utility', 1),
(4, 'Rent Payment', '2024-04-30', 'Monthly house rent', 'Rent', 1),
(5, 'Gym Membership', '2024-05-05', 'Annual gym membership fee', 'Leisure', 3),
(6, 'Car Insurance', '2024-06-15', 'Annual car insurance', 'Insurance', 2),
(7, 'Health Insurance', '2024-07-10', 'Monthly health insurance', 'Insurance', 1),
(8, 'Phone Bill', '2024-08-05', 'Monthly phone bill', 'Utility', 2),
(9, 'Gas Bill', '2024-09-20', 'Gas supply payment', 'Utility', 1),
(10, 'Parking Fee', '2024-10-25', 'Monthly parking fee', 'Leisure', 2),
(11, 'Streaming Service', '2024-11-10', 'Monthly subscription', 'Entertainment', 3),
(12, 'Credit Card Payment', '2024-12-05', 'Monthly credit card payment', 'Finance', 1);

INSERT INTO authorizations (account_id, login_time, logout_time, password) VALUES 
(1, '2024-01-01 08:00:00', '2024-01-01 09:00:00', 'password1'),
(2, '2024-01-02 10:00:00', '2024-01-02 11:00:00', 'password2'),
(3, '2024-01-03 12:00:00', '2024-01-03 13:00:00', 'password3'),
(4, '2024-01-04 14:00:00', '2024-01-04 15:00:00', 'password4'),
(5, '2024-01-05 16:00:00', '2024-01-05 17:00:00', 'password5'),
(6, '2024-01-06 18:00:00', '2024-01-06 19:00:00', 'password6'),
(7, '2024-01-07 08:00:00', '2024-01-07 09:00:00', 'password7'),
(8, '2024-01-08 10:00:00', '2024-01-08 11:00:00', 'password8'),
(9, '2024-01-09 12:00:00', '2024-01-09 13:00:00', 'password9'),
(10, '2024-01-10 14:00:00', '2024-01-10 15:00:00', 'password10'),
(11, '2024-01-11 16:00:00', '2024-01-11 17:00:00', 'password11'),
(12, '2024-01-12 18:00:00', '2024-01-12 19:00:00', 'password12');

INSERT INTO fees (transaction_id, fee_amount, fee_date) VALUES 
(1, 5.00, '2024-01-10'),
(2, 10.00, '2024-02-15'),
(3, 7.50, '2024-03-20'),
(4, 15.00, '2024-04-25'),
(5, 12.50, '2024-05-30'),
(6, 8.00, '2024-06-10'),
(7, 6.50, '2024-07-15'),
(8, 9.75, '2024-08-20'),
(9, 4.25, '2024-09-25'),
(10, 11.00, '2024-10-30'),
(11, 5.75, '2024-11-10'),
(12, 13.50, '2024-12-15');

INSERT INTO status_transactions (transaction_id, status, status_date) VALUES 
(1, 'Completed', '2024-01-10'),
(2, 'Pending', '2024-02-15'),
(3, 'Completed', '2024-03-20'),
(4, 'Failed', '2024-04-25'),
(5, 'Completed', '2024-05-30'),
(6, 'Pending', '2024-06-10'),
(7, 'Completed', '2024-07-15'),
(8, 'Failed', '2024-08-20'),
(9, 'Completed', '2024-09-25'),
(10, 'Pending', '2024-10-30'),
(11, 'Completed', '2024-11-10'),
(12, 'Failed', '2024-12-15');


CREATE INDEX idx_customer_accounts ON accounts(customer_id);

CREATE INDEX idx_transaction_date ON transactions(transaction_date);

CREATE INDEX idx_category_priority_date ON needs(category, priority, payment_date);