from flask import Flask, request, jsonify,render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/api')
def get_data():
    # Get query parameters from URL
    name = request.args.get('name')
    age = request.args.get('age')
    email=request.args.get('email')

    result = {
        'name': name,
        'age': age,
        'email':email
    }
    return jsonify(result)   # return as JSON

if __name__ == '__main__':
    app.run(debug=True)
