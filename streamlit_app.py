import datetime

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import yfinance as yf

# Налаштування назви сторінки
st.set_page_config(page_title='Практична робота №4', page_icon=':mortar_board:')


stock_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "UNH"]

def load_stock_data(tickers: list, start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    data = yf.download(tickers, start=start_date, end=end_date)
    
    if len(tickers) > 1:
        data = data["Adj Close"]
    
    return data


# Відображення опису і заголовку
'''
# :ticket: Перегляд ціни акцій

Цей застосунок розроблен в рамках індивідуальної роботи по університетській практиці.
Усі дані щодо ціни акцій збираються Python бібліотекою [`yfinance`](https://pypi.org/project/yfinance/), 
яка працює як обгортка до Yahoo Finance.
Початковий код застосунку можна переглянути у [GitHub репозиторії](https://github.com/selfkilla666/practice_work_4).

'''

st.divider()

# Налаштування дати
today_date = datetime.date.today()
month_ago_date = today_date - datetime.timedelta(days=28)

start_col, end_col = st.columns(2)

start_date = start_col.date_input("Початок періоду", month_ago_date)
end_date = end_col.date_input("Кінець періоду", today_date)

# Налаштування тікетів акцій
selected_tickers = st.multiselect(
    "Оберіть акції які Вам потрібні",
    stock_tickers,
    ["AAPL", "MSFT", "GOOGL"],
    placeholder="Потрібно обрати хоча б одну акцію"
)

# Заголовок для графіків
st.header("Ціна акцій за обраний час", divider="green")

# Перевірка коректності даних
if len(selected_tickers) == 0:
    st.error("Помилка: потрібно обрати хоча б одну акцію")
else:
    # Отримання даних
    data = load_stock_data(selected_tickers, start_date, end_date)

    if data.empty:
        st.warning("Помилка: немає даних про обрані акції та обраний період")
    else:
        # Підготовка даних для відображення
        data = data.reset_index().melt(id_vars="Date", var_name="Акція", value_name="Ціна закриття")

        # Побудова графіку
        chart_figure = px.line(data, x="Date", y="Ціна закриття", color="Акція")
        
        # Відображення
        st.plotly_chart(chart_figure)
