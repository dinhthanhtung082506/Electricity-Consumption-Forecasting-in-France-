import requests
import pandas as pd
from pathlib import Path

OUT = Path(r"C:\Users\tungd\Downloads\Demand Electric\Data\Raw")
OUT.mkdir(parents=True, exist_ok=True)

START = "2012-01-01"
END = "2026-06-30"
URL = "https://calendrier.api.gouv.fr/jours-feries/metropole"

records = []

for year in range(2012, 2027):
    url = f"{URL}/{year}.json"
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    for date, holiday_name in response.json().items():
        if START <= date <= END:
            records.append({
                "date": date,
                "holiday_name": holiday_name,
                "is_holiday": 1,
            })

holidays = pd.DataFrame(records, columns=["date", "holiday_name", "is_holiday"])

holidays.to_csv(
    OUT / "french_holidays.csv",
    index=False,
    encoding="utf-8-sig"
)

print(f"Đã lưu danh sách ngày lễ vào: {OUT / 'french_holidays.csv'}")
print(f"Số ngày lễ: {len(holidays)}")