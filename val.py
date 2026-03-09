#!/usr/bin/env python3
import requests

def convert_currency(from_currency: str, to_currency: str, amount: float):
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    url = f"https://open.er-api.com/v6/latest/{from_currency}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("result") == "success" and "rates" in data and to_currency in data["rates"]:
            rate = data["rates"][to_currency]
            result = amount * rate
            return f"Курс: 1 {from_currency} = {rate} {to_currency}\n" \
                   f"{amount} {from_currency} = {result} {to_currency}"
        else:
            return f"Ошибка: не удалось получить курс валют. Проверьте коды валют.\nОтвет сервера: {data}"
    except requests.RequestException as e:
        return f"Ошибка при запросе данных: {e}"

if __name__ == "__main__":
    from_currency = input("Из какой валюты: ").upper()
    to_currency = input("В какую валюту: ").upper()
    try:
        amount = float(input("Сколько конвертировать: "))
    except ValueError:
        print("Ошибка: введите корректное число для суммы.")
        exit(1)

    print(convert_currency(from_currency, to_currency, amount))
