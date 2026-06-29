import requests


def get_game():

    url = "https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=50"

    data = requests.get(url).json()

    if not data:
        return None

    game = data[0]

    return {
        "title": game["title"],
        "price": game["salePrice"],
        "discount": round(float(game["savings"])),
        "image": game["thumb"]
    }