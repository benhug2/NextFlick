from flask import Flask, request, jsonify, render_template
import pandas as pd
import random

app = Flask(__name__)

# Load movie data
try:
    moviesDf = pd.read_csv('tmdb_5000_movies.csv')
    # Ensure necessary columns
    moviesDf['genres'] = moviesDf['genres'].fillna('[]')  # Fill missing genres
    moviesDf['title'] = moviesDf['title'].fillna('Unknown Title')  # Fill missing titles
except FileNotFoundError:
    print("Error: The file 'tmdb_5000_movies.csv' was not found.")
    exit(1)
except Exception as e:
    print(f"Error loading CSV: {e}")
    exit(1)

def get_genre_list():
    # Extract unique genres from the dataset
    genres = set()
    for genre_list in moviesDf['genres']:
        try:
            genre_data = eval(genre_list)  # Convert string to list of dicts
            for genre in genre_data:
                genres.add(genre['name'])
        except:
            continue
    return sorted(genres)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/genres', methods=['GET'])
def fetchGenres():
    return jsonify(get_genre_list()), 200

@app.route('/movies/by_genre', methods=['GET'])
def getMovieByGenre():
    genre = request.args.get('genre', '').strip()
    if not genre:
        return jsonify({'message': 'Genre parameter is required'}), 400

    filteredMovies = moviesDf[moviesDf['genres'].str.contains(genre, case=False, na=False)]

    if filteredMovies.empty:
        return jsonify({'message': f'No movies found for genre: {genre}'}), 404

    # Select a random movie
    random_movie = filteredMovies.sample(n=1)
    return jsonify(random_movie[['title', 'overview', 'release_date', 'vote_average']].to_dict(orient='records')[0]), 200

@app.route('/movies/details', methods=['GET'])
def movieDetails():
    title = request.args.get('title', '').strip()
    if not title:
        return jsonify({'message': 'Title parameter is required'}), 400

    movie = moviesDf[moviesDf['title'].str.contains(title, case=False, na=False)].head(1)
    if movie.empty:
        return jsonify({'message': f'No details found for movie: {title}'}), 404
    return jsonify(movie.to_dict(orient='records')[0]), 200

if __name__ == '__main__':
    app.run(debug=True)
