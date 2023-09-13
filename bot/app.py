from flask import Flask, send_file, after_this_request
from pandas import read_sql
from sqlalchemy import create_engine
import os

app = Flask(__name__)


@app.route('/download/<book_id>')
def show_customers(book_id):
    engine = create_engine("postgresql+psycopg2://:@localhost:5432/bot_db")
    connection = engine.connect()
    read_sql(f"SELECT borrow_id, book_id, date_start, date_end FROM borrows", connection).\
        to_excel(f"../user_downloads/book_{book_id}_info.xlsx")

    @after_this_request
    def remove_file(response):
        try:
            os.remove(f"../user_downloads/book_{book_id}_info.xlsx")
        except Exception as error:
            app.logger.error("Error removing or closing downloaded file handle", error)
        return response
    return send_file(f"../user_downloads/book_{book_id}_info.xlsx")


if __name__ == "__main__":
    app.run("0.0.0.0", port=8080)
