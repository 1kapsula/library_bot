import telebot
from database.dbapi import DatabaseConnector

token = '6197894236:AAGmwjj5aFgv2fR1jR9e0OCK9aZig4ew5bg'
bot = telebot.TeleBot(token)


class Book:
    def __init__(self, title="", author="", year=""):
        self.title = title
        self.author = author
        self.year = year

    def key_book(self):
        return f"{self.title}, {self.author}, {self.year}"


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Добро пожаловать в чат бота-библиотеки!")


@bot.message_handler(commands=['add'])
def add_book(message):
    bot.reply_to(message, "Введите название книги:")
    bot.register_next_step_handler(message, create_book, params=['title', 'add'])


@bot.message_handler(commands=['delete'])
def delete_book(message):
    bot.reply_to(message, "Введите название книги:")
    bot.register_next_step_handler(message, create_book, params=['title', 'delete'])


@bot.message_handler(commands=['list'])
def list_book(message):
    lst = con.list_books()
    resp = ''
    for l in lst:
        if l[5] is None:
            resp += f'{l[1]}, {l[2]}, {l[3]}\n'
        else:
            resp += f'{l[1]}, {l[2]}, {l[3]} (удалена)\n'
    bot.reply_to(message, resp)


@bot.message_handler(commands=['find'])
def find_book(message):
    bot.reply_to(message, "Введите название книги:")
    bot.register_next_step_handler(message, create_book, params=['title', 'find'])


@bot.message_handler(commands=['borrow'])
def borrow_book(message):
    bot.reply_to(message, "Введите название книги:")
    bot.register_next_step_handler(message, create_book, params=['title', 'borrow'])


@bot.message_handler(commands=['retrieve'])
def retrieve(message):
    try:
        id, book_id = con.get_last_borrow(message.from_user.id)
    except:
        bot.reply_to(message, "У вас нет забронированных книг")
        return
    if id is None:
        bot.reply_to(message, "Ошибка")
    else:
        book_info = con.get_book_by_id(book_id)
        if con.retrieve(id):
            bot.reply_to(message, f"Вы вернули книгу {book_info[0]} {book_info[1]} {book_info[2]}")


@bot.message_handler(commands=['stats'])
def stat_book(message):
    bot.reply_to(message, "Введите название книги:")
    bot.register_next_step_handler(message, create_book, params=['title', 'stats'])


def create_book(message, params):
    if params[0] == "title":
        bot.send_message(message.chat.id, "Введите автора:")
        book.title = message.text
        bot.register_next_step_handler(message, create_book, params=['author', params[1]])

    elif params[0] == 'author':
        bot.send_message(message.chat.id, 'Введите год:')
        book.author = message.text
        bot.register_next_step_handler(message, create_book, params=['year', params[1]])

    elif params[0] == 'year':
        try:
            book.year = int(message.text)
        except:
            bot.send_message(message.chat.id, "Введите корректный год выпуска")
            bot.register_next_step_handler(message, create_book, params=['year', params[1]])
            return
        if params[1] == 'add':
            id = con.add(book.title, book.author, book.year)
            if not id:
                bot.send_message(message.chat.id, "Ошибка при добавлении книги")
            else:
                bot.send_message(message.chat.id, f"Книга добавлена ({id})")
        if params[1] == 'delete':
            id = con.get_book(book.title, book.author, book.year)
            if not id:
                bot.send_message(message.chat.id, "Ошибка при удалении книги")
            else:
                bot.send_message(message.chat.id, f"Найдена книга: {book.title} {book.author} {book.year}. Удаляем?")
                bot.register_next_step_handler(message, yes_no, params=['delete', id])
        if params[1] == 'find':
            id = con.get_book(book.title, book.author, book.year)
            if not id:
                bot.send_message(message.chat.id, "Такой книги у нас нет")
            else:
                bot.send_message(message.chat.id, f"Найдена книга: {book.title} {book.author} {book.year}")
        if params[1] == 'borrow':
            id = con.get_book(book.title, book.author, book.year)
            if not id:
                bot.send_message(message.chat.id, "Книгу сейчас невозможно взять")
            else:
                bot.send_message(message.chat.id, f"Найдена книга: {book.title} {book.author} {book.year}. Берем?")
                bot.register_next_step_handler(message, yes_no, params=['borrow', id])
        if params[1] == 'stats':
            id = con.get_book(book.title, book.author, book.year)
            if not id:
                bot.send_message(message.chat.id, "Нет такой книги")
            else:
                bot.send_message(message.chat.id, f"Статистика доступна по адресу http://0.0.0.0:8080/download/{id}")


def yes_no(message, params):
    if message.text.lower() == 'да':
        if params[0] == 'delete':
            if con.delete(params[1]):
                bot.send_message(message.chat.id, "Книга удалена")
            else:
                bot.send_message(message.chat.id, "Ошибка при удалении книги")
        elif params[0] == 'borrow':
            if not con.borrow(message.from_user.id, params[1]):
                bot.send_message(message.chat.id, "Книгу сейчас невозможно взять")
            else:
                bot.send_message(message.chat.id, "Вы взяли книгу")
    elif message.text.lower() == 'нет':
        if params[0] == 'delete':
            bot.send_message(message.chat.id, "Книга не удалена")
        elif params == 'borrow':
            bot.send_message(message.chat.id, "Книга не взята")


if __name__ == "__main__":
    con = DatabaseConnector(dbname='bot_db', user='', password='', host='localhost', port='5432')
    book = Book()
    bot.infinity_polling()
