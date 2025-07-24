import sys
import datetime

# --- Target Date ---
if '--test' in sys.argv:
    today = datetime.date.today()
    days_ahead = (6 - today.weekday()) % 7  # Sunday is 6
    target_date = today + datetime.timedelta(days=days_ahead)
else:
    target_date = datetime.date.today() + datetime.timedelta(days=14)

target_day = target_date.strftime("%A")
target_day_num = target_date.strftime("%-d")
target_month = target_date.strftime("%B")
target_label = f"{target_day} {target_day_num} {target_month}"

print(f"Booking attempt for {target_label}...")
