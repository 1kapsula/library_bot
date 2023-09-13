from sqlalchemy import create_engine
if __name__ == "__main__":
    from models import *
else:
    from .models import *
import psycopg2


connection_string = f"postgresql+psycopg2://:@localhost:5432/bot_db"

if __name__ == "__main__":
    conn = psycopg2.connect(
        database="postgres",
        user='',
        password='',
        host='localhost',
        port='5432'
    )
    conn.autocommit = True
    cursor = conn.cursor()
    sql = ''' CREATE database bot_db '''
    cursor.execute(sql)
    print("Database has been created successfully !!")
    conn.close()
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)
