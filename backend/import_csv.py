import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

DB_CONFIG = {
    "host": "localhost",
    "database": "genz_social",
    "user": "postgres",
    "password": "postgres",
    "port": 5432
}

df = pd.read_csv("genz_social_media_usage_1M.csv")

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

cur.execute("""
DROP TABLE IF EXISTS social_media_usage;

CREATE TABLE social_media_usage (
    id SERIAL PRIMARY KEY,
    age INTEGER,
    gender TEXT,
    country TEXT,
    daily_usage_hours FLOAT,
    primary_platform TEXT,
    num_platforms_used INTEGER,
    purpose TEXT,
    avg_session_minutes FLOAT,
    night_usage TEXT,
    mental_health_score INTEGER,
    addiction_level TEXT,
    screen_time_before_sleep FLOAT
);
""")

records = df[[
    "age",
    "gender",
    "country",
    "daily_usage_hours",
    "primary_platform",
    "num_platforms_used",
    "purpose",
    "avg_session_minutes",
    "night_usage",
    "mental_health_score",
    "addiction_level",
    "screen_time_before_sleep"
]].values.tolist()

execute_values(cur, """
    INSERT INTO social_media_usage (
        age, gender, country, daily_usage_hours,
        primary_platform, num_platforms_used, purpose,
        avg_session_minutes, night_usage,
        mental_health_score, addiction_level,
        screen_time_before_sleep
    )
    VALUES %s
""", records)

conn.commit()
cur.close()
conn.close()

print(f"Zaimportowano {len(records)} rekordów ✅")