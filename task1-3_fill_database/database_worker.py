import pymssql
import pandas as pd
from booking.config import *

# Подключение к базе данных, данные для авторизации берутся из модуля config (авторизация через SQL пользователя)
def connect():
    return pymssql.connect(host=HOST, server=SERVER, user=USER, password=PASSWORD, port=PORT, database=DATABASE)


# Выполнение запроса, создающего таблицы
# Скрипт в файле files\create_tables.txt
def create_tables():
    connection = connect()
    cursor = connection.cursor()
    sql_query = open(CREATE_QUERY_PATH).read()
    cursor.execute(sql_query)
    connection.commit()
    cursor.close()
    connection.close()


# Заполнение таблицы country из dataframe([country_name])
def insert_countries(data):
    connection = connect()
    cursor = connection.cursor()
    sql_query = "INSERT INTO [dbo].[country] ([country_name]) VALUES (%s)"
    sql_data = tuple(map(tuple, data.values))
    cursor.executemany(sql_query, sql_data)
    connection.commit()
    cursor.close()
    connection.close()


# Заполнение таблицы city из dataframe([city_name])
def insert_cities(data):
    connection = connect()
    cursor = connection.cursor()
    sql_query = "INSERT INTO [dbo].[city] ([city_name]) VALUES (%s)"
    sql_data = tuple(map(tuple, data.values))
    cursor.executemany(sql_query, sql_data)
    connection.commit()
    cursor.close()
    connection.close()


# Заполнение таблицы source из dataframe([source_name])
def insert_source(data):
    connection = connect()
    cursor = connection.cursor()
    sql_query = "INSERT INTO [dbo].[source] ([source_name]) VALUES (%s)"
    sql_data = tuple(map(tuple, data.values))
    cursor.executemany(sql_query, sql_data)
    connection.commit()
    cursor.close()
    connection.close()


# Заполнение таблицы currency_rate из dataframe([id_currency ], [date], [rate])
def insert_currency_rates(data):
    connection = connect()
    cursor = connection.cursor()
    sql_query = "INSERT INTO [dbo].[currency_rate] ([id_currency ], [date], [rate]) VALUES (%s, %s, %s)"
    sql_data = tuple(map(tuple, data.values))
    cursor.executemany(sql_query, sql_data)
    connection.commit()
    cursor.close()
    connection.close()


# Заполнение таблицы provider из dataframe([provider_name], [id_country], [id_city])
def insert_providers(data):
    connection = connect()
    cursor = connection.cursor()
    sql_query = "INSERT INTO [dbo].[provider] ([provider_name], [id_country], [id_city]) VALUES (%s, %s, %s)"
    sql_data = tuple(map(tuple, data.values))
    cursor.executemany(sql_query, sql_data)
    connection.commit()
    cursor.close()
    connection.close()


# Заполнение таблицы booking из dataframe([id_provider], [creation_date],
# [start_date], [status], [nights], [price], [id_currency], [id_source], [creator])
def insert_booking(data):
    connection = connect()
    cursor = connection.cursor()
    sql_query = "INSERT INTO [dbo].[booking] ([id_provider], [creation_date], [start_date], [status], [nights], " \
                "[price], [id_currency], [id_source], [creator]) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, '')"
    sql_data = tuple(map(tuple, data.values))
    cursor.executemany(sql_query, sql_data)
    connection.commit()
    cursor.close()
    connection.close()


# Получение данных из таблицы country в dataframe([id_country], [country_name])
def select_countries():
    connection = connect()
    sql_query = "SELECT id_country, country_name FROM [dbo].[country]"
    return pd.read_sql(sql_query, connection)


# Получение данных из таблицы city в dataframe([id_city], [city_name])
def select_cities():
    connection = connect()
    sql_query = "SELECT id_city, city_name FROM [dbo].[city]"
    return pd.read_sql(sql_query, connection)


# Получение данных из таблицы provider в dataframe([id_provider])
def select_providers():
    connection = connect()
    sql_query = "SELECT id_provider FROM [dbo].[provider]"
    return pd.read_sql(sql_query, connection)


# Получение данных из таблицы source в dataframe([id_source])
def select_sources():
    connection = connect()
    sql_query = "SELECT id_source FROM [dbo].[source]"
    return pd.read_sql(sql_query, connection)


# Создание view BookingDetails и BookingChannelManagerPercent
# Скрипт в файле files\create_views.txt
def create_views():
    connection = connect()
    cursor = connection.cursor()
    sql_query = open(CREATE_VIEWS_PATH).read()

    # Поочери выполняются SQL команды из файла
    for script in sql_query.split(';'):
        cursor.execute(script)

    connection.commit()
    cursor.close()
    connection.close()


# Заполнение поля creator таблицы booking
# Скрипт в файле files\update_booking_creator.txt
def update_bookings_creator():
    connection = connect()
    cursor = connection.cursor()
    sql_query = open(UPDATE_BOOKING_CREATOR_PATH).read()
    cursor.execute(sql_query)
    connection.commit()
    cursor.close()
    connection.close()
