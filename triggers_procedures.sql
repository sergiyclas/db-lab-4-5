DELIMITER $$
CREATE TRIGGER after_transaction_insert
AFTER INSERT ON transactions
FOR EACH ROW
BEGIN
    INSERT INTO logs (transaction_id, log_action)
    VALUES (NEW.transaction_id, 'Transaction inserted');

    INSERT INTO logs (transaction_id, log_action)
    VALUES (NEW.transaction_id, 'Transaction reviewed');

    INSERT INTO logs (transaction_id, log_action)
    VALUES (NEW.transaction_id, 'Transaction approved');
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE insert_into_table(
 IN table_name VARCHAR(255),
 IN column_list VARCHAR(255),
 IN value_list VARCHAR(255)
)
BEGIN
 SET @sql = CONCAT('INSERT INTO ', table_name, ' (', column_list, ')
VALUES (', value_list, ')');
 SELECT @sql AS generated_sql;
 PREPARE stmt FROM @sql;
 EXECUTE stmt;
 DEALLOCATE PREPARE stmt;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE insert_into_relation_accounts_transactions (
    IN value1 VARCHAR(50),
    IN value2 VARCHAR(50)
)
BEGIN
    SET @query = CONCAT('INSERT INTO TransactionsAccounts (account_id, transaction_id) ',
                        'SELECT (SELECT account_id FROM accounts WHERE account_number = "', value1, '"), ',
                        '(SELECT transaction_id FROM transactions WHERE transaction_id = "', value2, '")');
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END;
$$
DELIMITER ;

DELIMITER $$

CREATE PROCEDURE insert_multiple_rows_customers (
    IN start_num INT,
    IN end_num INT
)
BEGIN
    DECLARE i INT;
    SET i = start_num;
    WHILE i <= end_num DO
        SET @query = CONCAT('INSERT INTO customers (customer_name) VALUES ("Noname', i, '")');
        PREPARE stmt FROM @query;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        SET i = i + 1;
    END WHILE;
END;

$$
DELIMITER ;

DELIMITER //
CREATE PROCEDURE calculate_column_transactions_proc (
    IN column_name VARCHAR(50),
    IN operation VARCHAR(10),
    OUT result DECIMAL(15,2)
)
BEGIN
    -- Змінна для SQL-запиту
    SET @query = '';
    SET @temp_result = 0; -- Тимчасова змінна для результату

    -- Вибір операції залежно від введеного параметра
    IF operation = 'MAX' THEN
        SET @query = CONCAT('SELECT MAX(', column_name, ') INTO @temp_result FROM transactions');
    ELSEIF operation = 'MIN' THEN
        SET @query = CONCAT('SELECT MIN(', column_name, ') INTO @temp_result FROM transactions');
    ELSEIF operation = 'SUM' THEN
        SET @query = CONCAT('SELECT SUM(', column_name, ') INTO @temp_result FROM transactions');
    ELSEIF operation = 'AVG' THEN
        SET @query = CONCAT('SELECT AVG(', column_name, ') INTO @temp_result FROM transactions');
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Unsupported operation';
    END IF;

    -- Виконання запиту
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

    -- Присвоєння результату OUT-параметру
    SET result = @temp_result;
END;
//

CREATE PROCEDURE select_with_function_transactions (
    IN column_name VARCHAR(50),
    IN operation VARCHAR(10)
)
BEGIN
    DECLARE result DECIMAL(15,2);
    CALL calculate_column_transactions_proc(column_name, operation, result);
    SELECT result AS result;
END;
//
DELIMITER;


DELIMITER $$
CREATE PROCEDURE `CreateRandomTransactionTablesAndCopyData`()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE transId INT;
    DECLARE transAmount DECIMAL(15, 2);
    DECLARE transDate DATE;
    DECLARE transaction_cursor CURSOR FOR SELECT transaction_id, amount, transaction_date FROM transactions;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    SET @table1_name = CONCAT('transaction_data_', DATE_FORMAT(NOW(), '%Y%m%d_%H%i%s'));
    SET @table2_name = CONCAT('transaction_data_', DATE_FORMAT(NOW(), '%Y%m%d_%H%i%s'), '_copy');

    SET @create_table1_sql = CONCAT('CREATE TABLE ', @table1_name, ' (
        transaction_id INT NOT NULL,
        amount DECIMAL(15, 2) NOT NULL,
        transaction_date DATE NOT NULL,
        PRIMARY KEY (transaction_id)
    ) ENGINE=InnoDB;');

    SET @create_table2_sql = CONCAT('CREATE TABLE ', @table2_name, ' (
        transaction_id INT NOT NULL,
        amount DECIMAL(15, 2) NOT NULL,
        transaction_date DATE NOT NULL,
        PRIMARY KEY (transaction_id)
    ) ENGINE=InnoDB;');

    PREPARE stmt1 FROM @create_table1_sql;
    EXECUTE stmt1;
    DEALLOCATE PREPARE stmt1;

    PREPARE stmt2 FROM @create_table2_sql;
    EXECUTE stmt2;
    DEALLOCATE PREPARE stmt2;

    OPEN transaction_cursor;

    read_loop: LOOP
        FETCH transaction_cursor INTO transId, transAmount, transDate;

        IF done THEN
            LEAVE read_loop;
        END IF;

        IF (RAND() < 0.5) THEN
            SET @insert_sql = CONCAT('INSERT INTO ', @table1_name,
                ' (transaction_id, amount, transaction_date) VALUES (',
                transId, ', ', transAmount, ', ', QUOTE(transDate), ');');
        ELSE
            SET @insert_sql = CONCAT('INSERT INTO ', @table2_name,
                ' (transaction_id, amount, transaction_date) VALUES (',
                transId, ', ', transAmount, ', ', QUOTE(transDate), ');');
        END IF;

        PREPARE stmt3 FROM @insert_sql;
        EXECUTE stmt3;
        DEALLOCATE PREPARE stmt3;
    END LOOP;

    CLOSE transaction_cursor;
END
$$
DELIMITER ;


DELIMITER //
CREATE TRIGGER prevent_delete_transactions
BEFORE DELETE ON transactions
FOR EACH ROW
BEGIN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Deleting rows from the transactions table is not allowed.';
END;
//
DELIMITER ;


DELIMITER //
CREATE TRIGGER prevent_invalid_email
BEFORE INSERT ON customers
FOR EACH ROW
BEGIN
    IF NEW.email LIKE '%00' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Email cannot end with two zeros.';
    END IF;
END;
//
DELIMITER ;


CREATE TABLE allowed_names (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL
);

-- Тригер для перевірки імені
DELIMITER //
CREATE TRIGGER validate_allowed_names
BEFORE INSERT ON allowed_names
FOR EACH ROW
BEGIN
    IF NEW.name NOT IN ('Svitlana', 'Petro', 'Olha', 'Taras') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Only the names Svitlana, Petro, Olha, or Taras are allowed.';
    END IF;
END;//
DELIMITER ;



-- CALL CreateRandomTransactionTablesAndCopyData();

-- CALL insert_into_notifications('account_id, message', '1, "Account notification"');
-- CALL insert_into_relation_accounts_transactions('ACC10001', '10');
-- CALL insert_multiple_rows_customers(1, 10);
-- CALL calculate_column_transactions_proc('amount', 'SUM', @result);
-- SELECT @result;

-- CALL calculate_column_transactions_proc('amount', 'AVG', @result);
-- SELECT @result;

-- CALL select_with_function_transactions('amount', 'AVG');
*/

