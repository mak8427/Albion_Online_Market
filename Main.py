import requests
import polars as pl
import time

city_dict = {}
cities = [
    "Thetford",
    "Bridgewatch",
    "Martlock",
    "Lymhurst",
    "Fort Sterling",
    "Caerleon",
]
for city in cities:
    try:
        city_dict[city] = pl.read_csv(f"{city}.csv")
        NOT_LOADED = False
    except:
        NOT_LOADED = True
        city_dict[city] = pl.DataFrame(
            {
                "item_id": [],
                "city": [],
                "quality": [],
                "sell_price_min": [],
                "sell_price_min_date": [],
                "sell_price_max": [],
                "sell_price_max_date": [],
                "buy_price_min": [],
                "buy_price_min_date": [],
                "buy_price_max": [],
                "buy_price_max_date": [],
            }
        )

try:
    response = requests.get(
    "https://europe.albion-online-data.com/api/v2/stats/prices/T4_Soul.json?qualities=1"
    )
except:
    time.sleep(120)
    response = requests.get(
        "https://europe.albion-online-data.com/api/v2/stats/prices/T4_Soul.json?qualities=1"
    )

# json to dict
data = response.json()
df = pl.DataFrame(data)


def update_check(city_dict, df):
    return (
        city_dict[city]["sell_price_min_date"][-1]
        != df.filter(pl.col("city") == city)["sell_price_min_date"][-1]
    )


for city in cities:
    if NOT_LOADED:
        city_dict[city] = df.filter(pl.col("city") == city)
    if update_check(city_dict, df):
        # if the last timestamp is different
        city_dict[city] = city_dict[city].merge_sorted(
            df.filter(pl.col("city") == city), key="item_id"
        )
    else:
        print(
            f"{city} is up to date",
            city_dict[city]["sell_price_min_date"][-1],
            df.filter(pl.col("city") == city)["sell_price_min_date"][-1],
        )

    city_dict[city].write_csv(f"{city}.csv")
    print("")