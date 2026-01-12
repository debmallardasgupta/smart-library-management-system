from flask import Flask
app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect
@app.route("/")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True)