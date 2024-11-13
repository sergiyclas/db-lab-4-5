# database/procedures.py
def setup_procedures(cursor):
    insert_procedure = """
    DELIMITER //
    CREATE PROCEDURE InsertIntoTable(IN tableName VARCHAR(50), IN columnName VARCHAR(50), IN value VARCHAR(50))
    BEGIN
        SET @sql = CONCAT('INSERT INTO ', tableName, ' (', columnName, ') VALUES (', QUOTE(value), ')');
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END //
    DELIMITER ;
    """

    insert_author_book_procedure = """
    DELIMITER //
    CREATE PROCEDURE AddAuthorBook(IN author_name VARCHAR(50), IN book_title VARCHAR(50))
    BEGIN
        DECLARE author_id INT;
        DECLARE book_id INT;

        SELECT author_id INTO author_id FROM authors WHERE name = author_name;
        SELECT book_id INTO book_id FROM books WHERE title = book_title;

        IF author_id IS NOT NULL AND book_id IS NOT NULL THEN
            INSERT INTO author_books (author_id, book_id) VALUES (author_id, book_id);
        END IF;
    END //
    DELIMITER ;
    """

    cursor.execute(insert_procedure)
    cursor.execute(insert_author_book_procedure)
