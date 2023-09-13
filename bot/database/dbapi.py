import psycopg2


class DatabaseConnector:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def execute_query(self, query, fetch=False):
        connection = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        if fetch:
            result = cursor.fetchall()
        else:
            result = True
        cursor.close()
        connection.close()
        return result

    def add(self, title, author, published):
        query = f"INSERT INTO books (title, author, published, date_added) VALUES ('{title}', '{author}', '{published}', NOW()) RETURNING book_id;"
        result = self.execute_query(query, fetch=True)
        if result:
            return result[0][0]
        else:
            return False

    def delete(self, book_id):
        query = f"UPDATE books SET date_deleted = NOW() WHERE book_id = {book_id};"
        result = self.execute_query(query, fetch=False)
        return result

    def list_books(self):
        query = "SELECT * FROM Books;"
        result = self.execute_query(query, fetch=True)
        return result

    def get_book(self, title, author, published):
        query = f"SELECT book_id FROM Books WHERE title = '{title}' AND author = '{author}' AND published = {published};"
        result = self.execute_query(query, fetch=True)
        if result:
            return result[0][0]
        else:
            return None

    def get_book_by_id(self, book_id):
        query = f"SELECT title, author, published FROM Books WHERE book_id = '{book_id}'"
        result = self.execute_query(query, fetch=True)
        if result:
            return result[0]
        else:
            return None

    def borrow(self, user_id, book_id):
        query = f"SELECT COUNT(*) FROM Borrows WHERE user_id = {user_id} AND date_end IS NULL;"
        result = self.execute_query(query, fetch=True)
        print(result)
        if result[0][0] > 0:
            return False
        else:
            query = f"SELECT COUNT(*) FROM Borrows WHERE book_id = {book_id} AND date_end IS NULL;"
            result = self.execute_query(query, fetch=True)
            if result[0][0] > 0:
                return False
            else:
                query = f"INSERT INTO Borrows (user_id, book_id, date_start) VALUES ({user_id}, {book_id}, NOW()) RETURNING borrow_id;"
                result = self.execute_query(query, fetch=True)
                if result:
                    return result[0][0]
                else:
                    return False

    def get_borrow(self, user_id, book_id):
        query = f"SELECT borrow_id FROM Borrows WHERE user_id = {user_id} AND book_id = {book_id} AND date_end IS NULL;"
        result = self.execute_query(query, fetch=True)
        if result:
            return result[0][0]
        else:
            return None

    def get_last_borrow(self, user_id):
        query = f"SELECT borrow_id, book_id FROM Borrows WHERE user_id = {user_id} AND date_end IS NULL ORDER BY borrow_id DESC LIMIT 1"
        result = self.execute_query(query, fetch=True)
        if result:
            query = f"SELECT * FROM books WHERE book_id = {result[0][1]}"
            result_2 = self.execute_query(query, fetch=True)
            return result[0][0], result_2[0][0]
        else:
            return None

    def retrieve(self, borrow_id):
        query = f"UPDATE Borrows SET date_end = NOW() WHERE borrow_id = {borrow_id};"
        self.execute_query(query)
        return True


# connection_string = f"postgresql+psycopg2://:@localhost:5432/bot_db"
# engine = create_engine(connection_string)
# Base.metadata.create_all(engine)

#db_connector = DatabaseConnector(dbname='bot_db', user='', password='', host='localhost', port='5432')

