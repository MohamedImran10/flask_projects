import random
import string
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class URLMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(10), unique=True, nullable=False)

def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form["long_url"]
        short_code = generate_short_code()
        
        new_entry = URLMapping(long_url=long_url, short_url=short_code)
        db.session.add(new_entry)
        db.session.commit()

        return render_template("result.html", short_url=short_code)

    return render_template("index.html")

@app.route("/<short_url>")
def redirect_to_original(short_url):
    url_entry = URLMapping.query.filter_by(short_url=short_url).first()
    if url_entry:
        return redirect(url_entry.long_url)
    return "Invalid URL", 404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
