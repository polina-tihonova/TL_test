import requests
import pandas as pd
import xml.etree.ElementTree as ET
from booking.config import GEO_PATH
from dateutil.relativedelta import relativedelta


# Загружаем в dataframe данные из files\countries_cities.xlsx
# Файл подготовлен заренее, содержит 20 стран с городами в них.
def load_geo_locations():
    return pd.read_excel(GEO_PATH, dtype={'country': str, 'city': str})


# Загружаем в dataframe данные по странам из files\countries_cities.xlsx
def import_countries():
    countries = load_geo_locations()[['country_name']]
    countries = countries.drop_duplicates(ignore_index=True)
    countries = countries.dropna()
    return countries


# Загружаем в dataframe данные по городам из files\countries_cities.xlsx
def import_cities():
    cities = load_geo_locations()[['city_name']]
    cities = cities.drop_duplicates(ignore_index=True)
    cities = cities.dropna()
    return cities


# Запрос на нахождение курсов валют за период
def load_currency_rates(currency_codes, start_date, end_date):
    sbr_codes = load_currency_sbr_codes()
    dates = generate_dates(start_date, end_date)
    currency_rates = []

    for currency in currency_codes:
        sbr_code = sbr_codes[currency]
        for date in dates:
            new_date = date
            currency_rate = load_exchange_rate(currency, sbr_code, date)

            # Если на текущую дату нет курса, ищем последний день, когда курс был
            while 'rate' not in currency_rate:
                new_date -= relativedelta(days=1)
                currency_rate = load_exchange_rate(currency, sbr_code, new_date)
            currency_rate.update({'date': date})
            currency_rates.append(currency_rate)

    sbr_exchange_rates = pd.DataFrame(currency_rates, columns=['id_currency', 'date', 'rate'])
    sbr_exchange_rates['date'] = pd.to_datetime(sbr_exchange_rates['date'])
    sbr_exchange_rates['rate'] = sbr_exchange_rates['rate'].str.replace(',', '.').astype(float)
    return sbr_exchange_rates


# Генерирует список с днями между двумя датами
def generate_dates(period_start, period_end):
    date_arr = pd.date_range(period_start, period_end, freq='D')
    date_arr = pd.Series(date_arr).tolist()
    return date_arr


# Запрашивает коды валют по ЦБ
def load_currency_sbr_codes():
    url = 'http://www.cbr.ru/scripts/XML_valFull.asp'
    response = requests.get(url)

    root = ET.fromstring(response.content)
    currency_sbr_codes = {}
    for child in root:
        currency_sbr_codes.update({child[5].text: child.attrib['ID']})
    return currency_sbr_codes


# Запрашивает курс валюты на дату с сайта ЦБ РФ, возвращает dictionary с кодом валюты и курсом
def load_exchange_rate(currency_code, sbr_code, date):
    url = 'http://www.cbr.ru/scripts/XML_dynamic.asp?'\
          'date_req1=' + date.strftime('%d/%m/%Y') + \
          '&date_req2=' + date.strftime('%d/%m/%Y') + \
          '&VAL_NM_RQ=' + sbr_code
    response = requests.get(url)
    root = ET.fromstring(response.content)
    currency_rates = {}
    for child in root:
        currency_rates.update({
            'id_currency': currency_code,
            'rate': child[1].text
        })
    return currency_rates
