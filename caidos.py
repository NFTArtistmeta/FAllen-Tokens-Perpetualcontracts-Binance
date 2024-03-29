from binance.client import Client
from tabulate import tabulate

def get_all_futures_symbols(client):
    exchange_info = client.futures_exchange_info()
    symbols = [symbol['symbol'] for symbol in exchange_info['symbols'] if symbol['contractType'] == 'PERPETUAL']
    return symbols[:300]  # Return only the first 300 symbols

def get_price_change(client, symbol):
    ticker = client.futures_mark_price(symbol=symbol)
    return float(ticker['markPrice']) - float(ticker['lastFundingRate'])

def get_funding_fee(client, symbol):
    ticker = client.futures_mark_price(symbol=symbol)
    return float(ticker['lastFundingRate'])

def get_most_fallen_symbols(client, limit=300):
    symbols = get_all_futures_symbols(client)
    most_fallen_symbols = []
    for symbol in symbols:
        price_change = get_price_change(client, symbol)
        funding_fee = get_funding_fee(client, symbol)
        current_price = float(client.futures_mark_price(symbol=symbol)['markPrice'])
        if len(most_fallen_symbols) < limit:
            most_fallen_symbols.append((symbol, funding_fee, price_change, current_price))
        else:
            most_fallen_symbols.sort(key=lambda x: x[2])
            if price_change < most_fallen_symbols[-1][2]:
                most_fallen_symbols.pop()
                most_fallen_symbols.append((symbol, funding_fee, price_change, current_price))
    most_fallen_symbols.sort(key=lambda x: x[2], reverse=True)
    return most_fallen_symbols

def main():
    api_key = "19SEwu5mB9w4tNNnBpfArbenyBs9CnYCV7GPkqfz1I8bsCGl91mu34inL36zCgA1"
    api_secret = "mQ5Fvc62Zc0UwVzRr6PpnX3Q0cJnK98EnFyaaUCyc1snB2RJqGj0oguQLxdmwFZ1"
    client = Client(api_key, api_secret)

    most_fallen_symbols = get_most_fallen_symbols(client)

    headers = ["Symbol", "Funding Fee", "Price Change", "Current Price"]
    data = [[symbol, funding_fee, price_change, current_price] for symbol, funding_fee, price_change, current_price in most_fallen_symbols]
    print(tabulate(data, headers=headers, tablefmt="grid", numalign="right"))

if __name__ == "__main__":
    main()