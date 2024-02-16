import requests
import pandas as pd
import os

# Ваш API ключ
api_key = 'your_api_key'
url_base = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key
}

cryptos = []
start = 1
limit = 100
total_coins = 5000  # Примерное общее количество монет (пишем фактическое количество)
images_folder = 'coin_images'  # Имя папки для сохранения изображений

# Создаем папку для изображений, если она еще не существует
if not os.path.exists(images_folder):
    os.makedirs(images_folder)

while start < total_coins:
    params = {'start': start, 'limit': limit}
    try:
        response = requests.get(url_base, headers=headers, params=params)
        data = response.json()['data']
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        break

    for crypto in data:
        # Собираем данные о монете
        name = crypto['name']
        symbol = crypto['symbol']
        price = crypto['quote']['USD']['price']
        market_cap = crypto['quote']['USD']['market_cap']
        icon_url = f"https://s2.coinmarketcap.com/static/img/coins/64x64/{crypto['id']}.png"
        cryptos.append([name, symbol, price, market_cap, icon_url])

        # Скачивание изображения
        img_data = requests.get(icon_url).content
        with open(os.path.join(images_folder, f"{symbol}.png"), 'wb') as img_file:
            img_file.write(img_data)

    start += limit

# Создание DataFrame и сохранение в Excel
df = pd.DataFrame(cryptos, columns=['Монета', 'Тикер', 'Цена', 'Капитализация', 'URL иконки'])
df.to_excel('crypto_data.xlsx', index=False)
