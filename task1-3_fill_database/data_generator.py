import random
from faker import Faker
from datetime import date
from booking.data_loader import *
from booking.database_worker import *
from dateutil.relativedelta import relativedelta


# Генерируем названия source_name
def generate_source():
    source_values = pd.DataFrame(columns=['source_name'])
    source_values = source_values.append({'source_name': 'BS-CHANNEL_MANAGER'}, ignore_index=True)
    for i in range(1, 10):
        source_values = source_values.append({'source_name': 'Source_' + str(i)}, ignore_index=True)
    return source_values


# Получить маппинг городов и стран
def get_country_city_ids():
    locations = load_geo_locations()

    db_countries = select_countries()
    locations = locations.merge(db_countries,  how='left', on='country_name')

    db_cities = select_cities()
    locations = locations.merge(db_cities,  how='left', on='city_name')

    return locations


# Генерируем названия провайдеров
def get_random_provider_names(count):
    fake = Faker('ru_RU')
    provider_names = [fake.unique.company() for i in range(count)]
    return pd.DataFrame(provider_names)


# Подставляем рандомный город со страной
def get_random_location_ids(count):
    locations = get_country_city_ids()
    countries = []
    cities = []

    for i in range(count):
        location = locations.sample()
        location = location.to_dict('records')[0]
        countries.append(location['id_country'])
        cities.append(location['id_city'])

    location_ids = pd.DataFrame()
    location_ids['id_country'] = pd.Series(countries).values
    location_ids['id_city'] = pd.Series(cities).values
    return location_ids


# Генерируем данные для таблицы provider
def generate_providers(count=10000):
    providers = get_random_provider_names(count)
    location_ids = get_random_location_ids(count)
    return pd.concat([providers, location_ids], axis=1)


# Подставляем рандомный id_provider из таблицы в бд
def get_random_provider_ids(count):
    db_providers = select_providers()
    provider_ids = []
    for i in range(count):
        provider = db_providers.sample()
        provider = provider.to_dict('records')[0]
        provider_ids.append(provider['id_provider'])
    return provider_ids


# Подставляем рандомные даты
def get_random_dates(count, start_date, end_date):
    dates = []
    fake = Faker()
    for i in range(count):
        dates.append(fake.date_between(start_date, end_date))
    return dates


# Подставляем рандомный id_source из таблицы в бд
def get_random_source_ids(count):
    db_sources = select_sources()
    source_ids = []
    for i in range(count):
        source = db_sources.sample()
        source = source.to_dict('records')[0]
        source_ids.append(source['id_source'])
    return source_ids


# Генерируем данные для таблицы booking
def generate_bookings(count=100000, start_date=date(2018, 1, 1), end_date=date(2018, 3, 1), currencies=['USD', 'EUR', 'RUB']):
    provider_ids = get_random_provider_ids(count)
    creation_dates = get_random_dates(count, start_date, end_date)
    start_dates = [creation_dates[i] + relativedelta(days=random.randint(0, 300)) for i in range(0, count)]
    statuses = [random.randint(0, 5) for _ in range(0, count)]
    nights = [random.randint(1, 30) for _ in range(0, count)]
    prices = [round(random.uniform(100, 20000), 2) for _ in range(0, count)]
    currency_ids = [random.choice(currencies) for _ in range(0, count)]
    source_ids = get_random_source_ids(count)

    bookings = pd.DataFrame()
    bookings['id_provider'] = pd.Series(provider_ids).values
    bookings['creation_date'] = pd.Series(creation_dates).values
    bookings['start_date'] = pd.Series(start_dates).values
    bookings['status'] = pd.Series(statuses).values
    bookings['nights'] = pd.Series(nights).values
    bookings['price'] = pd.Series(prices).values
    bookings['id_currency'] = pd.Series(currency_ids).values
    bookings['id_source'] = pd.Series(source_ids).values

    return bookings
