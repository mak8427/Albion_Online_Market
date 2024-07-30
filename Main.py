import  requests
import polars as pl


city_dict = {}
cities = ["Thetford", "Bridgewatch", "Martlock", "Lymhurst", "Fort Sterling", "Caerleon"]
for city in cities:
    city_dict[city] = pl.read_csv(f"{city}.csv")

response = requests.get("https://europe.albion-online-data.com/api/v2/stats/prices/T4_Soul.json?qualities=1")
#json to dict
data = response.json()
df = pl.DataFrame(data)
for city in cities:
    city_dict[city] = city_dict[city].merge_sorted(df.filter(pl.col("city") == city),key="item_id")
    city_dict[city].write_csv(f"{city}.csv")



