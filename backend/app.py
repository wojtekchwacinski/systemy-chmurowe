from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "genz_social"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "port": int(os.getenv("DB_PORT", 5432))
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

# ======================
# GET ALL + FILTER
# ======================
@app.route("/usage", methods=["GET"])
def get_usage():
    platform = request.args.get("platform")

    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    if platform:
        cur.execute(
            "SELECT * FROM social_media_usage WHERE primary_platform ILIKE %s",
            (f"%{platform}%",)
        )
    else:
        cur.execute("SELECT * FROM social_media_usage ORDER BY id ASC LIMIT 100")

    data = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(data)

# ======================
# POST
# ======================
@app.route("/usage", methods=["POST"])
def add_usage():
    data = request.json

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO social_media_usage (
            age, gender, country, daily_usage_hours,
            primary_platform, num_platforms_used, purpose,
            avg_session_minutes, night_usage,
            mental_health_score, addiction_level,
            screen_time_before_sleep
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data["age"],
        data["gender"],
        data["country"],
        data["daily_usage_hours"],
        data["primary_platform"],
        data["num_platforms_used"],
        data["purpose"],
        data["avg_session_minutes"],
        data["night_usage"],
        data["mental_health_score"],
        data["addiction_level"],
        data["screen_time_before_sleep"]
    ))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Dodano"}), 201

# ======================
# PUT
# ======================
@app.route("/usage/<int:id>", methods=["PUT"])
def update_usage(id):
    data = request.json

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE social_media_usage
        SET age=%s, gender=%s, country=%s,
            daily_usage_hours=%s,
            primary_platform=%s,
            num_platforms_used=%s,
            purpose=%s,
            avg_session_minutes=%s,
            night_usage=%s,
            mental_health_score=%s,
            addiction_level=%s,
            screen_time_before_sleep=%s
        WHERE id=%s
    """, (
        data["age"],
        data["gender"],
        data["country"],
        data["daily_usage_hours"],
        data["primary_platform"],
        data["num_platforms_used"],
        data["purpose"],
        data["avg_session_minutes"],
        data["night_usage"],
        data["mental_health_score"],
        data["addiction_level"],
        data["screen_time_before_sleep"],
        id
    ))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Zaktualizowano rekord"})

@app.route("/usage/<int:id>", methods=["GET"])
def get_usage_by_id(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT * FROM social_media_usage WHERE id = %s", (id,))
    data = cur.fetchone()

    cur.close()
    conn.close()

    if data is None:
        return jsonify({"error": "Nie znaleziono rekordu"}), 404

    return jsonify(data)

# ======================
# STATS
# ======================
@app.route("/stats", methods=["GET"])
def get_stats():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT 
            primary_platform,
            ROUND(AVG(daily_usage_hours)::numeric, 2) AS avg_daily_usage,
            ROUND(AVG(mental_health_score)::numeric, 2) AS avg_mental_health,
            COUNT(*) AS users
        FROM social_media_usage
        GROUP BY primary_platform
        ORDER BY avg_daily_usage DESC
    """)

    data = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
