
import sqlite3


def main():
    try:
        conn = sqlite3.connect('booksall.db')
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS books(
           book TEXT,
           creator TEXT,
           description TEXT);
        """)
        cur.execute("""CREATE TABLE IF NOT EXISTS genres(
           Хоррор TEXT DEFAULT NULL,
           Детектив TEXT DEFAULT NULL,
           Бизнес TEXT DEFAULT NULL);
        """)
        # cur.execute("""CREATE TABLE IF NOT EXISTS books(
        #    book TEXT,
        #    creator TEXT,
        #    description TEXT);
        # """)
        conn.commit()
        conn.close()
        print('Введите номер нужного действия\n'
              f'-------------------------------------------\n'
              f'| 1. Список книг                          |\n'
              f'| 2. Поиск книги                          |\n'
              f'| 3. Удалить книгу                        |\n'
              f'| 4. Добавить книгу                       |\n'
              f'| 5. Выбрать книгу                        |\n'
              f'| 0. Закончить работу                     |\n'
              f'-------------------------------------------'
              )
        value = int(input("Ввод:"))
        if value == 1:
            all_books()
        if value == 2:
            search_book()
        if value == 3:
            delete_book()
        if value == 4:
            add_book()
        if value == 5:
            select_book()
        if value == 0:
            return
    except:
        print('Введите номер нужного действия')
        main()

def all_books():
    try:
        print(f'Выберите вариант списка\n'
              f'---------------------------\n'
              f'|1. Показать все книги    |\n'
              f'|2. Выбрать жанр книг     |\n'
              f'|0. Главное меню          |\n'
              f'---------------------------')
        book_list = input('Ввод:')
        if book_list == '1':
            conn = sqlite3.connect('booksall.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM books;")
            rows = cur.fetchall()
            print(f'В базе есть {len(rows)} книг')
            for row in rows:
                print(f'--------------------\n'
                      f'|Название: «{row[0]}»\n'
                      f'|Автор: {row[1]}\n'
                      f'--------------------')
            conn.close()
            main()
        elif book_list == '0':
            main()
        elif book_list == '2':
            conn = sqlite3.connect('booksall.db')
            cur = conn.cursor()
            cur.execute(f"PRAGMA table_info('genres')")
            columns = cur.fetchall()
            dones = [column[1] for column in columns]
            donesstr = ', '.join(dones)
            print(f'|Жанры которые есть в таблице: {donesstr} \n'
                  f'|Напишите 1 из них для просмотра книг в этом жанре')
            genre = input('Ввод:')
            cur.execute(f"SELECT {genre} FROM genres WHERE {genre} IS NOT NULL")
            result = cur.fetchall()
            if result:
                for row in result:
                    creator = cur.execute(f"SELECT creator FROM books WHERE book=?", (row[0],)).fetchone()
                    print(f'--------------------\n'
                          f'|Название: «{row[0]}»\n'
                          f'|Автор: {creator[0]}\n'
                          f'--------------------')
            else:
                print(f'Жанр {genre} не найден или пуст')
            conn.close()
            main()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
        main()

def add_book():
    print(f'------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n'
          '|Введите данные добавляемой книги: Название/ Создатель/ Описание                                                                                                             |\n'
          '|Пример: Десять негритят/ Агата Кристи/ Неизвестный пригласил десять человек на остров и предъявил им обвинения. Затем все приглашённые были убиты согласно детской считалке.|\n'
          '|Чтобы вернуться к главному меню [0]                                                                                                                                         |\n'
          '------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    try:
        new_book = list(input('Ввод:').split('/'))
        if len(new_book) == 3:
            conn = sqlite3.connect('booksall.db')
            cur = conn.cursor()
            info = cur.execute('SELECT * FROM books WHERE book=? AND creator=? AND description=?',
                               (new_book[0].strip(), new_book[1].strip(), new_book[2].strip())).fetchone()
            # Если запрос вернул None, то...
            if info is None:
                try:
                    cur.execute(f"PRAGMA table_info('genres')")
                    columns = cur.fetchall()
                    dones = [column[1] for column in columns]
                    donesstr = ', '.join(dones)
                    print(f'|Жанры которые есть в таблице: {donesstr} \n'
                          f'|Укажите какой из них соответствует книге или введите новый одним словом\n'
                          f'|Чтобы вернуться к главному меню [0]')
                    genre = str(input('Ввод:'))
                    print(genre)
                    if genre == '0':
                        main()
                    elif genre in donesstr:
                        cur.execute(f"INSERT INTO genres ({genre}) VALUES (?)", (new_book[0].strip(),))
                        cur.execute("INSERT INTO books (book, creator, description) VALUES (?, ?, ?)",
                                    (new_book[0].strip(), new_book[1].strip(), new_book[2].strip()))
                        conn.commit()
                        print(f"|Книга «{new_book[0].strip()}» успешно добавлена в таблицу")
                        conn.close()
                        main()
                    else:
                        cur.execute(f"ALTER TABLE genres ADD COLUMN {genre} TEXT DEFAULT NULL")
                        cur.execute(f"INSERT INTO genres ({genre}) VALUES (?)", (new_book[0].strip(),))
                        cur.execute("INSERT INTO books (book, creator, description) VALUES (?, ?, ?)",
                                    (new_book[0].strip(), new_book[1].strip(), new_book[2].strip()))
                        conn.commit()
                        print(f"|Книга «{new_book[0].strip()}» успешно добавлена в таблицу")
                        conn.close()
                        main()
                except sqlite3.Error as error:
                    conn.close()
                    print("Ошибка при работе с SQLite", error)
                    add_book()

            else:
                conn.commit()
                print("Книга существует в базе данных")
                cur.close()
                add_book()

        elif len(new_book) == 1 and new_book == list(0):
            main()
        else:
            print('Данные введены некорректно попробуйте еще раз')
            add_book()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite:", error)
        main()

def search_book():
    try:
        print(f'Выберите вариант поиска\n' 
              f'---------------------------\n'
              f'|1. По Названию           |\n'
              f'|2. По Автору             |\n'
              f'|3. По Названию и Автору  |\n'
              f'|0. Главное меню          |\n'
              f'---------------------------')
        search = input('Ввод:')
        if search == '0':
            main()
        elif search == '1':
            print('|Введите элемент названия книги')
            find = input('Ввод:')
            conn = sqlite3.connect('booksall.db')
            cur = conn.cursor()
            info = cur.execute('SELECT book, creator FROM books').fetchall()
            if info:
                for name, creator in info:
                    if find.lower() in name.lower():
                        print(f'--------------------\n'
                              f'|Название: «{name}»\n'
                              f'|Автор: {creator}\n'
                              f'--------------------')
            else:
                print('Ничего не найдено')
            conn.close()
            main()
        elif search == '2':
            print('|Введите элемент названия Автора')
            find = input('Ввод:')
            conn = sqlite3.connect('booksall.db')
            cur = conn.cursor()
            info = cur.execute('SELECT book, creator FROM books').fetchall()
            if info:
                for name, creator in info:
                    if find.lower() in creator.lower():
                        print(f'--------------------\n'
                              f'|Название: «{name}»\n'
                              f'|Автор: {creator}\n'
                              f'--------------------')
            else:
                print('Ничего не найдено')
            conn.close()
            main()
        elif search == '3':
            print('|Введите элемент названия Книги и автора: Десять/ Агата')
            find = list(input('Ввод:').split('/'))
            conn = sqlite3.connect('booksall.db')
            cur = conn.cursor()
            info = cur.execute('SELECT book, creator FROM books').fetchall()
            if info:
                for name, creator in info:
                    if find[0].strip().lower() in name.lower() and find[1].strip().lower() in creator.lower():
                        print(f'--------------------\n'
                              f'|Название: «{name}»\n'
                              f'|Автор: {creator}\n'
                              f'--------------------')
            else:
                print('Ничего не найдено')
            conn.close()
            main()
        else:
            search_book()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite:", error)
        main()

def delete_book():
    try:
        print('---------------------------------------\n'
              '|Напишите название книги для удаления.|\n'
              '|Напишите 0 для возврата в меню       |\n'
              '---------------------------------------')
        delbook = input('Ввод:')
        if delbook == '0':
            main()
        else:
            conn = sqlite3.connect('booksall.db')
            cur = conn.cursor()
            info = cur.execute('SELECT * FROM books WHERE book=?', (delbook, )).fetchone()
            if info:
                cur.execute(f"PRAGMA table_info('genres')")
                columns = [column[1] for column in cur.fetchall()]
                where_clause = " OR ".join([f"{column} = '{delbook}'" for column in columns])
                cur.execute(f"DELETE FROM genres WHERE {where_clause}")
                cur.execute('DELETE FROM books WHERE book=?', (delbook, ))
                conn.commit()
                conn.close()
                print(f'|Книга «{delbook}» удалена из базы данных')
                main()
            else:
                print(f'Книга «{delbook}» не найдена')
                delete_book()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite:", error)
        main()

def select_book():
    try:
        print('-------------------------------------------------------\n'
              '|Введите название книги для получения информации о ней|\n'
              '|Напишите 0 для возврата в меню                       |\n'
              '-------------------------------------------------------')
        selected_book = input('Ввод:')
        if selected_book == '0':
            main()
        else:
            conn = sqlite3.connect('booksall.db')
            cur = conn.cursor()
            cur.execute(f"SELECT creator, description FROM books WHERE book=?", (selected_book,))
            book_info = cur.fetchone()
            if book_info:
                creator, description = book_info
                cur.execute(f"PRAGMA table_info('genres')")
                columns = cur.fetchall()
                for column in columns:
                    cur.execute(f"SELECT {column[1]} FROM genres WHERE {column[1]}=?", (selected_book,))
                    genre_info = cur.fetchone()
                    if genre_info:
                        genre = genre_info[0]
                        print(f"Вот информация о вашей книге\n"
                              f"----------------------------------"
                              f"|Название: {selected_book}\n"
                              f"|Автор: {creator}\n"
                              f"|Жанр: {genre}\n"
                              f"|Описание: {description}"
                              f"----------------------------------")
                        main()
            else:
                print('Книга не найдена')
                main()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite:", error)
        main()

if __name__ == '__main__':
    main()