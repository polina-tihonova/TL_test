import pandas as pd
from time import sleep
from datetime import date
from booking.data_loader import *
from booking.data_generator import *
from booking.database_worker import *


def main():
    # Создание таблиц
    # Скрипт в файле files\create_tables.txt
    create_tables()

    # Заполнение таблицы country
    insert_countries(import_countries())

    # Заполнение таблицы city
    insert_cities(import_cities())

    # Заполнение таблицы source
    insert_source(generate_source())

    # Заполнение таблицы currency_rate
    insert_currency_rates(
        load_currency_rates(
            ['USD', 'EUR'],
            start_date=date(2018, 1, 1),
            end_date=date(2018, 3, 1)
        )
    )

    # Заполнение таблицы provider
    insert_providers(generate_providers(10000))

    # Заполнение таблицы booking, через цикл для снижения нагрузки
    for i in range(10):
        insert_booking(
            generate_bookings(
                count=50000,
                start_date=date(2018, 1, 1),
                end_date=date(2018, 3, 1),
                currencies=['USD', 'EUR', 'RUB']
            )
        )
        sleep(2)

    # Заполнение поля creator таблицы booking
    # Скрипт в файле files\update_booking_creator.txt
    update_bookings_creator()

    # Создание view BookingDetails и BookingChannelManagerPercent
    # Скрипт в файле files\create_views.txt
    create_views()


if __name__ == '__main__':
    main()
