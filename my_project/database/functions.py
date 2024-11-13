# database/functions.py
def setup_functions(cursor):
    calculate_stat_function = """
    DELIMITER //
    CREATE FUNCTION CalculateStat(statType VARCHAR(10), columnName VARCHAR(50), tableName VARCHAR(50))
    RETURNS DECIMAL(15, 2)
    DETERMINISTIC
    BEGIN
        SET @sql = CONCAT('SELECT ', statType, '(', columnName, ') FROM ', tableName);
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        RETURN @result;
    END //
    DELIMITER ;
    """

    cursor.execute(calculate_stat_function)
