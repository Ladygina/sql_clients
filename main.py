import psycopg2

conn= psycopg2.connect(database='Netology_db',
                 user = 'postgres',
                 password ='Fdnjcthdbc!')
with conn.cursor() as curr:
    curr.execute("""DROP TABLE client""")  # comment if doesn't exist

################### 1 task #############
    def create_table(cursor):
        print("\n------ task1----------\n")
        print('\ncreate empty table:\n')
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS client(
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(40) NOT NULL,
                            surname VARCHAR(40) NOT NULL,
                            numbers INTEGER[], 
                            email VARCHAR(40)
        );                   
        """)

    python_id = create_table(curr)
    conn.commit()

##################### 2 task #######
    def add_new_client(cursor, name_in, surname_in, number_in, email_in):
        cursor.execute("""
        INSERT INTO client (name, surname, numbers, email) VALUES (%s,%s,%s,%s);
        """, (name_in, surname_in, number_in, email_in))
    note_Vasya = add_new_client(curr,'Vasya', 'Sizykh',[3456,7894], 'Vasya@email.ru' )
    note_Segrei = add_new_client(curr, 'Segrei', 'Sizykh', [3278, 1123, 8976], 'Segrei@email.ru')
    note_Grigoryi = add_new_client(curr, 'Grigoryi', 'Serov', [4578, 2002, 9087], 'Gr@email.ru')
    conn.commit()

    print("\n_______task2______\nadding new clients:\n")
    curr.execute("""
            SELECT * FROM client;                   
            """)
    print(curr.fetchall())


##################### 3 task #######
    def add_phone(cursor, client_id, new_add_number):
        cursor.execute("""
                SELECT numbers FROM client WHERE id =%s;
                """, (client_id,))

        arr = list(cursor.fetchall())[0][0]    # извлечение массива номеров для выбранного пользователя
        arr.append(new_add_number)                 # добавление нового номера

        new_numbers_list = [int(item) for item in arr]     # новое значение поля numbers

        cursor.execute("""                                  
                UPDATE client SET numbers=%s
                WHERE id=%s;
        """, (new_numbers_list, client_id))          # Обновление поля номеров для выбранного пользователя


##################### 4 task ######
    def update_client(cursor, client_id, new_name, new_surname, new_number, new_email):
        cursor.execute("""
                UPDATE client SET name=%s, surname=%s, numbers=%s, email=%s
                WHERE id=%s;
                """, (new_name,  new_surname, new_number,new_email,client_id))
    update_client(curr, 2, 'Sergei1', 'Sizykh', [3278, 1123, 8976], 'Segrei1@email.ru')
    conn.commit()

    print("\n_______task4______\nupdate client by client_id(id=2):\n")
    curr.execute("""
                SELECT * FROM client;                   
                """)
    print(curr.fetchall())

    add_phone(curr, 2, 123)
    conn.commit()

    print("\n_______task3______\nadd new phone by client_id(id=2):\n")
    curr.execute("""
                   SELECT * FROM client;                   
                   """)
    print(curr.fetchall())


##################### 5 task #######
    def delete_phone(cursor, client_id, delete_number):
        cursor.execute("""
                    SELECT numbers FROM client WHERE id =%s;
                    """, (client_id,))

        arr = list(cursor.fetchall())[0][0]  # извлечение массива номеров
        arr.remove(delete_number)  # удаление номера

        new_numbers_list = [int(item) for item in arr]  # новое значение поля numbers

        cursor.execute("""
                    UPDATE client SET numbers=%s
                    WHERE id=%s;
            """, (new_numbers_list, client_id))


    delete_phone(curr, 3, 2002)
    conn.commit()

    print("\n_______task5______\ndelete phone by client_id and client phone (id=3):\n")
    curr.execute("""
                      SELECT * FROM client;                   
                      """)
    print(curr.fetchall())

##################### 6 task ######
    def delete_client(cursor, id_delete):
        cursor.execute("""
                DELETE FROM client WHERE id=%s;
                """, (id_delete,))
    delete_client(curr, 1)
    conn.commit()

    print("\n_______task6______\ndelete client by client_id(id=1):\n")
    curr.execute("""
                      SELECT * FROM client;                   
                      """)
    print(curr.fetchall())

###################### 7 task #########################
    def search_client_by_id(cursor, id_search):
        print('\n____search_by_id, id =', str(id_search),'_______\n')
        cursor.execute("""
                SELECT * FROM client WHERE id=%s;
                """, (id_search,))
        print(cursor.fetchall())
    def search_client_by_name(cursor, name_search):
        print('\n____search_by_name, name =', str(name_search),'_______\n')
        cursor.execute("""
                SELECT * FROM client WHERE name=%s;
                """, (name_search,))
        print(cursor.fetchall())
    def search_client_by_surname(cursor, surname_search):
        print('\n____search_by_surname, surname =', str(surname_search),'_______\n')
        cursor.execute("""
           SELECT * FROM client WHERE surname=%s;
           """, (surname_search,))
        print(cursor.fetchall())
    def search_client_by_phone(cursor,phone_search):
        print('\n____search_by_phone, phone =', str(phone_search),'_______\n')
        cursor.execute("""
                        SELECT numbers FROM client;
                        """, )
        numbers_list = list(cursor.fetchall())

        for i in range(len(numbers_list)):
            if phone_search in numbers_list[i][0]:  #если телефон в коллекции
                numbers_search = numbers_list[i]    # то находим пользователя по всей коллеции в numbers
        cursor.execute("""
                                SELECT * FROM client WHERE numbers=%s;
                                """, (numbers_search,))
        print(cursor.fetchall())
    def search_client_by_email(cursor, email_search):
        print('\n____search_by_email, email =', str(email_search),'_______\n')
        cursor.execute("""
                        SELECT * FROM client WHERE email=%s;
                        """, (email_search,))
        print(cursor.fetchall())


    print("\n_______task7______\nsearch client:\n")
    search_client_by_surname(curr, 'Serov')
    search_client_by_email(curr,'Gr@email.ru')
    search_client_by_phone(curr, 1123)
    search_client_by_name(curr, 'Sergei1')
    search_client_by_id(curr, 3)
conn.close()
