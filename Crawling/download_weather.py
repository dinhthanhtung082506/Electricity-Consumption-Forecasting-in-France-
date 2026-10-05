import requests
import pandas as pd
from pathlib import Path

OUT = Path(r"C:\Users\tungd\Downloads\Demand Electric\Data\Raw")
OUT.mkdir(parents=True, exist_ok=True)

START = "2012-01-01"
END = "2026-06-30"

URL = "https://archive-api.open-meteo.com/v1/archive"
PARAMS = {
    "latitude": 48.8566,
    "longitude": 2.3522,
    "start_date": START,
    "end_date": END,
    "hourly": (
        "temperature_2m,relative_humidity_2m,cloud_cover,"
        "shortwave_radiation,wind_speed_10m,precipitation"
    ),
    "timezone": "Europe/Paris",
    "wind_speed_unit": "kmh",
    "precipitation_unit": "mm",
    "temperature_unit": "celsius",
}

response = requests.get(URL, params=PARAMS, timeout=180)
response.raise_for_status()
data = response.json()

df = pd.DataFrame(data["hourly"])
df["timestamp"] = pd.to_datetime(df["time"])
df = df.drop(columns=["time"])

df.to_csv(
    OUT / "weather_hourly_paris.csv",
    index=False,
    encoding="utf-8-sig"
)

daily = df.groupby(df["timestamp"].dt.date).agg(
    temperature_mean=("temperature_2m", "mean"),
    temperature_max=("temperature_2m", "max"),
    humidity_mean=("relative_humidity_2m", "mean"),
    cloud_cover_mean=("cloud_cover", "mean"),
    shortwave_radiation_mean=("shortwave_radiation", "mean"),
    wind_speed_mean=("wind_speed_10m", "mean"),
    precipitation_sum=("precipitation", "sum"),
    valid_hour_count=("timestamp", "count"),
).reset_index(names="date")

daily.to_csv(
    OUT / "weather_daily_paris.csv",
    index=False,
    encoding="utf-8-sig"
)

print(f"Đã lưu dữ liệu thời tiết vào: {OUT}")
print(f"Số bản ghi giờ: {len(df)}")
print(f"Số ngày: {len(daily)}")