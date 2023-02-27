import requests
import datetime as dt
from twilio.rest import Client
import os

STOCK = "TSlA"
COMPANY_NAME = "Tesla Inc"

account_sid = "123"
auth_token = "123"


yesterday = str(dt.date.today()- dt.timedelta(days=3))
day_before_yesterday = str(dt.date.today() - dt.timedelta(days=4))

news_api_key = "123"
news_url = "https://newsapi.org/v2/everything"
news_parameters = {
    "q": COMPANY_NAME,
    "from": yesterday,
    "to": yesterday,
    "sortBy": "popularity",
    "apiKey": news_api_key,
}



stock_api_key = " 123"
stock_url = "https://www.alphavantage.co/query"
stock_parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
     "symbol": STOCK,
     "apikey": stock_api_key,
}

stock_response = requests.get(stock_url, params=stock_parameters)
stock_response.raise_for_status()
data = stock_response.json()

y_close = float(data["Time Series (Daily)"][yesterday]["4. close"])
b_close = float(data["Time Series (Daily)"][day_before_yesterday]["4. close"])

def p():
    remainder = abs(y_close - b_close)
    num = (remainder / y_close) * 100
    return num

if p() > 1 :
    news_response = requests.get(news_url, params=news_parameters)
    news_response.raise_for_status()
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    list = [f"title: {num['title']}  description: {num['description']}" for num in three_articles]

    for article in list:
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=article,
            from_="1234",
            to="1234"
        )
        print(message.sid)

