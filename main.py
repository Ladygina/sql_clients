import psycopg2
import numpy as np

conn= psycopg2.connect(database='Netology_db',
                 user = 'postgres',
                 password ='Fdnjcthdbc!')

###################### defs db processing###################
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
def add_new_client(cursor, name_in, surname_in, number_in, email_in):
        cursor.execute("""
        INSERT INTO client (name, surname, numbers, email) VALUES (%s,%s,%s,%s);
        """, (name_in, surname_in, number_in, email_in))
def add_phone(cursor, client_id, new_add_number):
    cursor.execute("""
                SELECT numbers FROM client WHERE id =%s;
                """, (client_id,))

    arr = list(cursor.fetchall())[0][0]  # извлечение массива номеров для выбранного пользователя
    arr.append(new_add_number)  # добавление нового номера

    new_numbers_list = [int(item) for item in arr]  # новое значение поля numbers

    cursor.execute("""                                  
                UPDATE client SET numbers=%s
                WHERE id=%s;
        """, (new_numbers_list, client_id))  # Обновление поля номеров для выбранного пользователя
def update_client(cursor, client_id, new_name=None, new_surname=None, new_number=None, new_email=None):
        if not new_name==None:
            cursor.execute("""
                            UPDATE client SET name=%s
                            WHERE id=%s;
                            """, (new_name,client_id))
        if not new_surname==None:
            cursor.execute("""
                            UPDATE client SET surname=%s
                            WHERE id=%s;
                            """, (new_surname,client_id))
        if not new_number==None:
            cursor.execute("""
                            UPDATE client SET numbers=%s
                            WHERE id=%s;
                            """, (new_number, client_id))

        if not new_email==None:
            cursor.execute("""
                            UPDATE client SET email=%s
                            WHERE id=%s;
                            """, (new_email, client_id))
def delete_phone(cursor, client_id, delete_number):
        cursor.execute("""
                    SELECT numbers FROM client WHERE id =%s;
                    """, (client_id,))

        arr = list(cursor.fetchall())[0][0]  # извлечение массива номеров
        arr.remove(delete_number)  # добавление нового номера

        new_numbers_list = [int(item) for item in arr]  # новое значение поля numbers

        cursor.execute("""
                    UPDATE client SET numbers=%s
                    WHERE id=%s;
            """, (new_numbers_list, client_id))
def delete_client(cursor, id_delete):
        cursor.execute("""
                DELETE FROM client WHERE id=%s;
                """, (id_delete,))
def search_client(cursor, id_search=None, name_search=None, surname_search=None, phone_search=None, email_search=None):
    attributes_select = []
    attributes_values=[]
    attributes_map={}
    if not id_search==None:
        attributes_map['id']= id_search
    if not name_search == None:
        attributes_map['name'] = name_search
    if not surname_search == None:
        attributes_map['surname'] = surname_search
    if not phone_search == None:
        attributes_map['numbers'] = phone_search
    if not email_search == None:
        attributes_map['email'] = email_search
    condition_strings=[]
    values=[]

    message='search client by '
    for column, value in attributes_map.items():
        message+=column+'='+str(value) +' '
        if column!='numbers':
            condition_strings.append(f"{column} = %s")
            values.append(value)
        else:
            cursor.execute("""
                                SELECT numbers FROM client;
                                """, )
            numbers_list = list(cursor.fetchall())
            for i in range(len(numbers_list)):
                if phone_search in numbers_list[i][0]:  # если телефон в коллекции
                    numbers_search = numbers_list[i]  # то находим пользователя по всей коллеции в numbers
                    values.append(numbers_search[0])
            condition_strings.append(f"numbers = %s")

    condition_clause = " AND ".join(condition_strings)
    query = f"SELECT * FROM client WHERE {condition_clause}"

    cursor.execute(query, values)
    results = cursor.fetchall()

    print(message, ':\n', results, '\n')
def show_results(cursor):
    cursor.execute("""
                SELECT * FROM client;                   
                """)
    print(curr.fetchall())

#################### defs db processing #####################

with psycopg2.connect(database='Netology_db',
                 user = 'postgres',
                 password ='Fdnjcthdbc!') as conn:

    curr = conn.cursor()
    curr.execute("""DROP TABLE client""")  # comment if doesn't exist

# 1 task #############
    python_id = create_table(curr)

# 2 task #######

    note_Vasya = add_new_client(curr,'Vasya', 'Sizykh',[3456,7894], 'Vasya@email.ru' )
    note_Segrei = add_new_client(curr, 'Segrei', 'Sizykh', [3278, 1123, 8976], 'Segrei@email.ru')
    note_Grigoryi = add_new_client(curr, 'Grigoryi', 'Serov', [4578, 2002, 9087], 'Gr@email.ru')

    print("\n_______task2______\nadding new clients:\n")
    show_results(curr)

# 4 task ######
    update_client(curr, 2, new_name='Seryoga')
    print("\n_______task4______\nupdate client 1 param(id=2):\n")
    show_results(curr)

    update_client(curr, 2, new_surname='Sergeev', new_number=[345, 9089])
    print("\n_______task4______\nupdate client several params (id=2):\n")
    show_results(curr)

# 3 task #######
    add_phone(curr, 2, 123)
    print("\n_______task3______\nadd phone:\n")
    show_results(curr)

# 5 task #######

    delete_phone(curr, 3, 2002)
    print("\n_______task5______\ndelete phone:\n")
    show_results(curr)

# 6 task ######
    delete_client(curr, 1)
    print("\n_______task6______\ndelete client(id=1):\n")
    show_results(curr)

# 7 task #########################
    print("\n_______task7______\nsearch client:\n")
    search_client(curr, surname_search='Serov')
    search_client(curr, surname_search='Serov',phone_search=4578,email_search = 'Gr@email.ru' )
    search_client(curr, id_search=3, phone_search=9087)

conn.close()