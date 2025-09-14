from flask import Flask, request, jsonify, render_template, redirect, url_for
import pymongo
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI")

if not MONGO_URI:
    raise ValueError("MONGODB_URI not found in environment variables.")

# MongoDB connection
client = pymongo.MongoClient(MONGO_URI)
db = client['flask_tutorial_db']
collection = db['users']

app = Flask(__name__)

# /api route
@app.route('/api', methods=['GET'])
def api():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Home page with form
@app.route('/', methods=['GET', 'POST'])
def home():
    error_message = None
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        email = request.form.get('email')

        user_data = {"name": name, "age": age, "email": email}

        try:
            collection.insert_one(user_data)
            return redirect(url_for('success'))
        except Exception as e:
            error_message = str(e)

    return render_template("index.html", error=error_message)

# Success page: show all submissions
@app.route('/success')
def success():
    try:
        # Fetch all documents from MongoDB
        users = list(collection.find())
        # Convert ObjectId to string for JSON/template
        for user in users:
            user["_id"] = str(user["_id"])
    except Exception as e:
        users = []
    return render_template("success.html", users=users)

if __name__ == '__main__':
    app.run(debug=True)
