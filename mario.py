#!/usr/bin/env python3
import os, subprocess, random
from datetime import datetime, timedelta

# کدگذاری رنگ‌ها:
# 0 = خالی
# 1 = پوست
# 2 = قرمز (کلاه ماریو/قارچ)
# 3 = آبی (شلوار)
# 4 = قهوه‌ای/مشکی (مو/کفش)
# 5 = سبز (کلاه لوئیجی)
# 6 = سفید (لکه‌های قارچ)

MARIO_LUIGI_MUSHROOM = [
"000022200000000000000000000055500000000000000000222000",
"002222220000000000000000005555550000000000000022662200",
"022211122200000000000000555111555000000000000226666220",
"022222222200000000000000555555555000000000000222666220",
"000220220000000000000000005505500000000000000022666220",
"000004400000000000000000000055000000000000000002266220",
"000044440000000000000000000555000000000000000000222000",
]

WEEKS = 53
DAYS = 7
START_DATE = "2024-01-07"

LEVEL_COMMITS = {
    "0": 0,   # خالی
    "1": 2,   # پوست
    "2": 5,   # قرمز
    "3": 8,   # آبی
    "4": 11,  # قهوه‌ای
    "5": 7,   # سبز
    "6": 3,   # سفید
}

def get_start_sunday(start_str):
    dt = datetime.strptime(start_str, "%Y-%m-%d")
    weekday = dt.weekday()
    days_to_sunday = (weekday + 1) % 7
    return dt - timedelta(days=days_to_sunday)

def make_commits(pattern, start_date):
    try:
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("❌ داخل ریپو نیستی. اول git init بزن.")
        return

    for w in range(WEEKS):
        for d in range(DAYS):
            level = pattern[d][w]
            count = LEVEL_COMMITS.get(level, 0)
            if count == 0:
                continue
            day_date = start_date + timedelta(weeks=w, days=d)
            for i in range(count):
                hour = random.randint(10, 18)
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                dt = datetime(day_date.year, day_date.month, day_date.day, hour, minute, second)
                datestr = dt.strftime("%Y-%m-%dT%H:%M:%S")
                env = os.environ.copy()
                env["GIT_AUTHOR_DATE"] = datestr
                env["GIT_COMMITTER_DATE"] = datestr
                subprocess.run(
                    ["git", "commit", "--allow-empty", "-m", f"MarioLuigiMushroom {w}-{d}-{i}"],
                    check=True,
                    env=env,
                )
    print("✅ ماریو + لوئیجی + قارچ ساخته شد! git push بزن و روی گیت‌هاب ببین.")

if __name__ == "__main__":
    start_sunday = get_start_sunday(START_DATE)
    make_commits(MARIO_LUIGI_MUSHROOM, start_sunday)
