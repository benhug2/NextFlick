from flask import Flask, request, jsonify, render_template
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Temporary in-memory user storage
usersDb = {}
userPreferences = {}

# Load movie data from CSV file
# Make sure tmdb_5000_movies.csv is in the same directory as app.py
moviesDf = pd.read_csv('tmdb_5000_movies.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signUp():
    userDetails = request.get_json()
    username = userDetails.get('username')
    password = userDetails.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    
    if username in usersDb:
        return jsonify({'message': 'Username already exists'}), 409

    usersDb[username] = generate_password_hash(password)
    userPreferences[username] = {'preferences': []}  # Initialize preferences
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def logIn():
    loginDetails = request.get_json()
    username = loginDetails.get('username')
    password = loginDetails.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    
    if username not in usersDb or not check_password_hash(usersDb[username], password):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    return jsonify({'message': 'Logged in successfully'}), 200

@app.route('/movies/search', methods=['GET'])
def searchMovies():
    query = request.args.get('query', '')
    if not query:
        return jsonify({'message': 'Query parameter is required'}), 400
    
    # Filter movies based on the query in the title
    filteredMovies = moviesDf[moviesDf['title'].str.contains(query, case=False, na=False)]
    
    # If no movies found, return an empty list
    if filteredMovies.empty:
        return jsonify([]), 200
    
    return jsonify(filteredMovies.to_dict(orient='records')), 200

if __name__ == '__main__':
    app.run(debug=True)
