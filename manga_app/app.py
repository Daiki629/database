from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# データベース初期化
def init_db():
    conn = sqlite3.connect("manga.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS manga (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            watched INTEGER,
            rating INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect("manga.db")
    c = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        watched = request.form["watched"]
        rating = request.form["rating"] if watched == "1" else None

        c.execute(
            "INSERT INTO manga (title, watched, rating) VALUES (?, ?, ?)",
            (title, watched, rating)
        )
        conn.commit()
        return redirect("/")

    c.execute("SELECT * FROM manga")
    mangas = c.fetchall()
    conn.close()

    return render_template("index.html", mangas=mangas)

if __name__ == "__main__":
    app.run(debug=True)
