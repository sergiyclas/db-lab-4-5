def drop_triggers(cursor):
    cursor.execute("DROP TRIGGER IF EXISTS check_customer_exists")
    cursor.execute("DROP TRIGGER IF EXISTS prevent_modification")
    cursor.execute("DROP TRIGGER IF EXISTS enforce_minimum_records")
    cursor.execute("DROP TRIGGER IF EXISTS enforce_format")


# database/triggers.py
def setup_triggers(cursor):
    create_orders_trigger = """
    CREATE TRIGGER IF NOT EXISTS check_customer_exists 
    BEFORE INSERT ON payment_templates
    FOR EACH ROW
    BEGIN
        IF (SELECT COUNT(*) FROM customers WHERE customers.customer_id = NEW.customer_id) = 0 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Customer does not exist';
        END IF;
    END;
    """

    prevent_modification_trigger = """
    CREATE TRIGGER IF NOT EXISTS prevent_modification BEFORE UPDATE ON customers
    FOR EACH ROW
    BEGIN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Modifications are not allowed on this table';
    END;
    """

    minimum_records_trigger = """
    CREATE TRIGGER IF NOT EXISTS enforce_minimum_records AFTER DELETE ON orders
    FOR EACH ROW
    BEGIN
        DECLARE record_count INT;
        SELECT COUNT(*) INTO record_count FROM orders;
        IF record_count < 6 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Minimum 6 records are required in this table';
        END IF;
    END;
    """

    format_enforcement_trigger = """
    CREATE TRIGGER IF NOT EXISTS enforce_format BEFORE INSERT ON cards
    FOR EACH ROW
    BEGIN
        IF NEW.some_column NOT REGEXP '^[^MR]{2}-[0-9]{3}-[0-9]{2}$' THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid format for column: must match pattern XX-XXX-XX';
        END IF;
    END;
    """

    cursor.execute(create_orders_trigger)
    cursor.execute(prevent_modification_trigger)
    cursor.execute(minimum_records_trigger)
    cursor.execute(format_enforcement_trigger)
