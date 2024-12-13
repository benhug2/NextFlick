from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load movie data from CSV file
moviesDf = pd.read_csv('tmdb_5000_movies.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/movies/by_mood', methods=['GET'])
def recommendMovieByMood():
    mood = request.args.get('mood', '').strip().lower()
    if not mood:
        return jsonify({'message': 'Mood parameter is required'}), 400

    # Map moods to genres
    mood_to_genre = {
        'happy': ['Comedy', 'Family', 'Animation'],
        'sad': ['Drama', 'Romance'],
        'excited': ['Action', 'Adventure', 'Thriller'],
        'curious': ['Science Fiction', 'Mystery'],
        'relaxed': ['Family', 'Animation', 'Fantasy']
    }

    genres = mood_to_genre.get(mood, [])
    if not genres:
        return jsonify({'message': f'No genres mapped for mood: {mood}'}), 404

    # Filter movies by the genres mapped to the mood
    filteredMovies = moviesDf[moviesDf['genres'].apply(
        lambda x: any(genre in x for genre in genres)
    )]

    if filteredMovies.empty:
        return jsonify({'message': f'No movies found for mood: {mood}'}), 404

    # Select a random movie
    random_movie = filteredMovies.sample(n=1)
    return jsonify(random_movie[['title', 'overview', 'release_date', 'vote_average']].to_dict(orient='records')[0]), 200

if __name__ == '__main__':
    app.run(debug=True)
