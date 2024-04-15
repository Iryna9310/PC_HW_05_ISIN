import asyncio
import aiohttp
from datetime import datetime, timedelta
import sys

async def fetch_exchange_rates(date):
    """
    Функція для отримання курсів валют з API ПриватБанку за певну дату.
    """
    url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def get_exchange_rates(num_days):
    """
    Функція для отримання курсів валют за останні кілька днів.
    """
    today = datetime.today()
    exchange_rates = []
    for i in range(num_days):
        date = (today - timedelta(days=i)).strftime('%d.%m.%Y')
        data = await fetch_exchange_rates(date)
        exchange_rates.append({date: {
            'EUR': {
                'sale': data['exchangeRate'][0]['saleRate'],
                'purchase': data['exchangeRate'][0]['purchaseRate']
            },
            'USD': {
                'sale': data['exchangeRate'][1]['saleRate'],
                'purchase': data['exchangeRate'][1]['purchaseRate']
            }
        }})
    return exchange_rates

async def main():
    """
    Основна функція програми.
    """
    if len(sys.argv) != 2:
        print("Usage: python main.py <num_days>")
        return

    num_days = int(sys.argv[1])
    if num_days > 10:
        print("Error: Number of days must be at most 10")
        return

    exchange_rates = await get_exchange_rates(num_days)
    print(exchange_rates)

if __name__ == "__main__":
    asyncio.run(main())