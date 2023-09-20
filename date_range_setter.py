from datetime import datetime, timedelta
import json

with open("config.json", 'r') as json_config:
    config = json.load(json_config)
    start_date_in_config = config["start_date"]
    days_limit = config["days_limit"]

start_date = (datetime.strptime(start_date_in_config, "%Y-%m-%d") if start_date_in_config else datetime.now()).date()
final_date = start_date + timedelta(days=days_limit)
print(final_date)