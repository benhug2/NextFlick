from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 

# In-memory user store: {username: {'password': '...', 'favorites': []}}
users = {}

# Load movie data
moviesDf = pd.read_csv('tmdb_5000_movies.csv')

def login_required(f):
    def wrapper(*args, **kwargs):
        if 'username' not in session or session['username'] not in users:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/')
@login_required
def home():
    username = session.get('username')
    user_favorites = users[username]['favorites']
    return render_template('index.html', favorites=user_favorites, username=username)

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'GET':
        return render_template('signup.html')

    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        return render_template('signup.html', error='Username and password are required.')

    if username in users:
        return render_template('signup.html', error='Username already exists.')

    # Create user
    users[username] = {'password': password, 'favorites': []}
    return redirect(url_for('login_page'))

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    
    username = request.form.get('username')
    password = request.form.get('password')
    if username not in users or users[username]['password'] != password:
        return render_template('login.html', error='Invalid username or password.')
    
    session['username'] = username
    return redirect(url_for('home'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login_page'))

@app.route('/movies/by_mood_and_language', methods=['GET'])
@login_required
def recommendMovieByMoodAndLanguage():
    mood = request.args.get('mood', '').strip().lower()
    language = request.args.get('language', '').strip().lower()

    if not mood or not language:
        return jsonify({'message': 'Mood and language parameters are required'}), 400

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

    filteredMovies = moviesDf[
        moviesDf['genres'].apply(lambda x: any(genre in x for genre in genres)) &
        (moviesDf['original_language'] == language)
    ]

    if filteredMovies.empty:
        return jsonify({'message': f'No movies found for mood: {mood} and language: {language}'}), 404

    random_movie = filteredMovies.sample(n=1).iloc[0].to_dict()

    if 'title' not in random_movie:
        return jsonify({'message': 'Selected movie does not have a title field.'}), 500

    session['last_recommended_movie'] = random_movie
    return jsonify({
        'title': random_movie.get('title', ''),
        'overview': random_movie.get('overview', ''),
        'release_date': random_movie.get('release_date', ''),
        'vote_average': random_movie.get('vote_average', '')
    }), 200

@app.route('/favorite', methods=['POST'])
@login_required
def favorite_movie():
    if 'last_recommended_movie' not in session:
        return jsonify({'message': 'No recommended movie to favorite'}), 400

    username = session.get('username')
    if username not in users:
        return jsonify({'message': 'User not found'}), 400

    movie_data = session['last_recommended_movie']
    movie_title = movie_data.get('title')

    if not movie_title:
        return jsonify({'message': 'Cannot favorite a movie without a title'}), 400

    if movie_title not in users[username]['favorites']:
        users[username]['favorites'].append(movie_title)
        return jsonify({'message': f'{movie_title} added to favorites'}), 200
    else:
        return jsonify({'message': f'{movie_title} is already in favorites'}), 200

if __name__ == '__main__':
    app.run(debug=True)
