import json
import os
import time
import xml.etree.ElementTree as ET
from datetime import date, datetime
from pprint import pprint

import apiclient.discovery as api_disc
import httplib2
import pandas as pd
import redis
import requests
import telebot
from oauth2client.service_account import ServiceAccountCredentials
from settings import (CHAT_ID, DB_PORT, POSTGRES_PASSWORD, POSTGRES_USER,
                      REDIS_HOST, REDIS_PORT, RESTART_TIME_SECONDS,
                      SPREADSHEET_ID, TOKEN)
from sqlalchemy import create_engine

# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = f"creds.json" if os.path.exists("creds.json") else f"app/creds.json"

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ],
)
httpAuth = credentials.authorize(httplib2.Http())
service = api_disc.build("sheets", "v4", http=httpAuth)
# engine = create_engine('postgresql://username:password@localhost:5432/mydatabase')
engine = create_engine(
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_PORT}/postgres"
)
redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

bot = telebot.TeleBot(TOKEN)

def get_sheet_values(service, spreadsheet_id):
    """
    Method receives data from google sheet.
    """
    sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()

    properties = sheet_metadata.get("sheets")
    pprint(properties)
    # read file
    values = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=spreadsheet_id,
            range=properties[0].get("properties").get("title"),
            majorDimension="ROWS",
        )
        .execute()
    )
    return values


def df_to_db(engine, values, curr_usd):
    """
    Method writes data to DB.
    """
    df = pd.DataFrame(data=values[1:], columns=values[0])
    df = df.astype({"стоимость,$": float})
    # возможно нужно брать курс доллара по дате заказа???
    # сейчас беру на текущий день
    df["стоимость,руб"] = df["стоимость,$"] * curr_usd

    df.to_sql("test", engine, if_exists="replace")
    return True


def dollar_exchange_rate():
    """
    Method return current dollar exchange rate.
    """
    currency_nb = requests.get("http://www.cbr.ru/scripts/XML_daily.asp")
    root = ET.fromstring(currency_nb.text)
    curr_usd = root.find("./Valute[NumCode='840']/Value").text
    curr_usd = float(curr_usd.replace(",", "."))
    print(f"curr_usd: {curr_usd}")
    return curr_usd


def delivery_check(values):
    df = pd.DataFrame(data=values[1:], columns=values[0])
    # df['срок поставки'] = pd.to_datetime(df['срок поставки'])
    date_format = "%d.%m.%Y"
    today = datetime.strptime(str(date.today()), "%Y-%m-%d")
    redis_get = json.loads(redis_conn.get('order_number'))
    list_order = []
    for _, row in df.iterrows():
        try:
            delivery_date = datetime.strptime(str(row['срок поставки']), date_format)
            day = (today-delivery_date).days
            if day > 0 and row['заказ №'] not in redis_get:
                text = f"Срок поставки заказа №: {row['заказ №']}, просрочен."
                list_order.append(row['заказ №'])
                bot.send_message(CHAT_ID, text)
        except ValueError:
            print("Not all fields are filled.")
    redis_conn.set('order_number', json.dumps(list_order+redis_get))


if __name__ == "__main__":
    curr_usd = dollar_exchange_rate()
    cnt = 0
    today = date.today()
    while True:
        if today != date.today():
            curr_usd = dollar_exchange_rate()
        values = get_sheet_values(service, SPREADSHEET_ID)
        delivery_check(values.get("values"))
        db_bool = df_to_db(engine, values.get("values"), curr_usd)
        cnt += 1
        pprint(f"cnt: {cnt}")
        time.sleep(RESTART_TIME_SECONDS)
