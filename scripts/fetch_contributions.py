import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def fetch_contributions(username="nikhilchalamalla", output_json="data/contributions.json"):
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    days_data = []
    total_contributions = 0

    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            day_cells = soup.find_all("td", class_="ContributionCalendar-day")
            
            for cell in day_cells:
                date_str = cell.get("data-date")
                level_str = cell.get("data-level", "0")
                if not date_str:
                    continue
                
                # Extract count from aria-label or id/tooltip
                count = 0
                cell_id = cell.get("id")
                if cell_id:
                    tool_tip = soup.find("tool-tip", {"for": cell_id})
                    if tool_tip:
                        txt = tool_tip.text.strip()
                        parts = txt.split(" ")
                        if parts[0].isdigit():
                            count = int(parts[0])
                
                level = int(level_str)
                days_data.append({
                    "date": date_str,
                    "level": level,
                    "count": count
                })
                total_contributions += count
    except Exception as e:
        print(f"Warning: Failed to fetch live contributions: {e}")

    # Fallback generator if empty or blocked
    if not days_data:
        print("Using generated fallback contribution structure...")
        today = datetime.now()
        for i in range(371, -1, -1):
            d = today - timedelta(days=i)
            d_str = d.strftime("%Y-%m-%d")
            # Generate deterministic sample activity based on date hash
            val = (d.day * 7 + d.month * 13) % 10
            level = 0 if val < 5 else (1 if val < 7 else (2 if val < 9 else 3))
            count = 0 if level == 0 else level * 3 + (d.day % 4)
            days_data.append({
                "date": d_str,
                "level": level,
                "count": count
            })
            total_contributions += count

    # Calculate streaks
    days_data.sort(key=lambda x: x["date"])
    current_streak = 0
    longest_streak = 0
    temp_streak = 0

    for day in days_data:
        if day["count"] > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0
            
    # Current streak from end
    for day in reversed(days_data):
        if day["count"] > 0:
            current_streak += 1
        else:
            break

    payload = {
        "username": username,
        "total_contributions": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "updated_at": datetime.now().isoformat(),
        "days": days_data
    }

    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Fetched {len(days_data)} days data ({total_contributions} total contributions). Saved to: {output_json}")

if __name__ == "__main__":
    fetch_contributions("nikhilchalamalla")
