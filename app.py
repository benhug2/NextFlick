from flask import Flask, request, jsonify, render_template
import pandas as pd
import random
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Temporary in-memory user storage
usersDb = {}
userPreferences = {}

# Load movie data from CSV file
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
    genre = request.args.get('genre', '')
    language = request.args.get('language', '')
    
    if not genre or not language:
        return jsonify({'message': 'Genre and language parameters are required'}), 400
    
    # Filter movies based on the genre and language
    filteredMovies = moviesDf[(moviesDf['genres'].str.contains(genre, case=False, na=False)) & 
                              (moviesDf['original_language'] == language)]
    
    # Randomly select one movie from the filtered list
    if not filteredMovies.empty:
        randomMovie = filteredMovies.sample(n=1)
        return jsonify(randomMovie.to_dict(orient='records')), 200
    
    return jsonify({'message': 'No movies found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
