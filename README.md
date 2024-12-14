#NextFlick

**Group Members: Bandhuli Maity, Branden Kooper, Ben Hug**

**Introduction**

NextFlick is a web-based application that provides personalized movie recommendations based on user moods and language preferences. Users can select their mood (e.g., Happy, Sad, Excited) and choose their preferred language to receive a movie recommendation tailored to their emotional state and linguistic preference. The system focuses on generating one movie at a time to help users decide quickly without endless scrolling. Users can create an account to save movies they love to their personalized "Favorites" list. With the click of a button, they can revisit their top picks anytime. 

**Technical Architecture**

**Frontend (Browser):**

Role in Application: The frontend provides the user interface for interacting with the application. Users can select their mood and language, view recommendations, and interact with features like "Show Me Another Option."
Interactions:
Sends user inputs (mood, language) to the backend via HTTP requests.
Displays responses from the backend, such as movie details.
Languages/Libraries:
HTML, CSS (Bootstrap for styling)
JavaScript (Fetch API for asynchronous requests)

**Backend (Flask Server):**

Role in Application: Handles business logic, processes user requests, and interacts with the data layer to fetch relevant movie recommendations.
Interactions:
Receives input from the frontend (via HTTP GET/POST requests).
Filters the dataset based on mood and language and returns appropriate movie data to the frontend.
Languages/Libraries:
Python (Flask for server-side logic)
Pandas (for dataset manipulation)

**Data Layer:**

Role in Application: Stores and provides access to the movie dataset.
Interactions:
Accessed by the backend for filtering and retrieving relevant movie records.
Languages/Libraries:
CSV file format
Manipulated using Pandas library in Python.
Dataset curated from TMDB and used directly in the backend.

**Installation Instructions:**

**Step 1: Install Python**

Ensure Python is installed on your system. You can download it from the official Python website.
Verify the installation:
Open a terminal or command prompt.

        Run: python --version (or python3 --version on some systems).
        
If Python is installed, you will see the version number.
        
**Step 2: Clone the Repository**

   Open a terminal or command prompt.

  Navigate to the directory where you want to clone the app:

     cd /path/to/your/directory

  Clone the GitHub repository:

     git clone https://github.com/CS222-UIUC/MovieGenerate

  Navigate into the cloned directory:

     cd your-repo-name
  
**Step 3: Install Flask and Other Dependencies**

   you can install Flask directly:

     pip install flask

**Step 4: Run the Flask App**

   Start the Flask application:

     python app.py

   Once the app starts, you should see output similar to:

       Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

   Open a web browser and go to http://127.0.0.1:5000/ to access the app.
