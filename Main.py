import  requests
import polars as pl
response = requests.get("https://europe.albion-online-data.com/api/v2/stats/prices/T4_Soul.json?qualities=1")
#json to dict
data = response.json()

df = pl.DataFrame(data)
df.write_csv("T4_SOUL_prices_polars.csv")
print(df )