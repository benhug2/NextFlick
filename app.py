# app.py - Advanced Flask Server with Additional Functionalities

import pandas as pd
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Temporary in-memory user storage
usersDb = {}
userPreferences = {}

# Load movie data from CSV file
moviesDf = pd.read_csv('tmdb_5000_movies.csv')

@app.route('/signup', methods=['POST'])
def signUp():
    userDetails = request.get_json()
    username = userDetails['username']
    password = userDetails['password']
    if username in usersDb:
        return jsonify({'message': 'Username exists'}), 409
    usersDb[username] = generate_password_hash(password)
    userPreferences[username] = {'preferences': []}  # Initialize preferences
    return jsonify({'message': 'User created'}), 201

@app.route('/login', methods=['POST'])
def logIn():
    loginDetails = request.get_json()
    username = loginDetails['username']
    password = loginDetails['password']
    if username not in usersDb or not check_password_hash(usersDb[username], password):
        return jsonify({'message': 'Invalid credentials'}), 401
    return jsonify({'message': 'Logged in'}), 200

@app.route('/movies/search', methods=['GET'])
def searchMovies():
    query = request.args.get('query', '')
    filteredMovies = moviesDf[moviesDf['title'].str.contains(query, case=False, na=False)]
    return jsonify(filteredMovies.to_dict(orient='records'))

@app.route('/movies/filter', methods=['GET'])
def filterMovies():
    genre = request.args.get('genre', '')
    filteredMovies = moviesDf[moviesDf['genres'].str.contains(genre, case=False, na=False)]
    return jsonify(filteredMovies.to_dict(orient='records'))

@app.route('/movies/sort', methods=['GET'])
def sortMovies():
    sortBy = request.args.get('sortBy', 'rating')
    sortedMovies = moviesDf.sort_values(by=[sortBy], ascending=False)
    return jsonify(sortedMovies.to_dict(orient='records'))

@app.route('/movies/<int:movieId>', methods=['GET'])
def getMovie(movieId):
    movie = moviesDf[moviesDf['id'] == movieId]
    if movie.empty:
        return jsonify({'message': 'Movie not found'}), 404
    return jsonify(movie.to_dict(orient='records'))

@app.route('/user/preferences', methods=['POST'])
def updateUserPreferences():
    preferencesDetails = request.get_json()
    username = preferencesDetails['username']
    preferences = preferencesDetails['preferences']
    if username not in usersDb:
        return jsonify({'message': 'User not found'}), 404
    userPreferences[username] = {'preferences': preferences}
    return jsonify({'message': 'Preferences updated'}), 200

if __name__ == '__main__':
    app.run(debug=True)
