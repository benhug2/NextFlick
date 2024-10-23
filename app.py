# Flask Server for User Authentication and Movie Retrieval from CSV

import pandas as pd
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Temporary in-memory user storage
usersDb = {}

# Load movie data from CSV file
moviesDf = pd.read_csv('tmdb_5000_movies.csv')

@app.route('/signup', methods=['POST'])
def signUp():
    # signup and store password
    userDetails = request.get_json()
    username = userDetails['username']
    password = userDetails['password']
    if username in usersDb:
        return jsonify({'message': 'Username exists'}), 409
    usersDb[username] = generate_password_hash(password)
    return jsonify({'message': 'User created'}), 201

@app.route('/login', methods=['POST'])
def logIn():
    # Validate login 
    loginDetails = request.get_json()
    username = loginDetails['username']
    password = loginDetails['password']
    if username not in usersDb or not check_password_hash(usersDb[username], password):
        return jsonify({'message': 'Invalid credentials'}), 401
    return jsonify({'message': 'Logged in'}), 200

@app.route('/movies', methods=['GET'])
def getMovies():
    # Convert DataFrame to JSON
    moviesJson = moviesDf.to_json(orient='records')
    return moviesJson

if __name__ == '__main__':
    app.run(debug=True)
