import requests  # Used to make HTTP requests to the TMDB API
import openai  # Used to interact with the OpenAI API for answering questions
from flask import Flask, render_template, request  # Flask for web app, request to handle form data
import sqlite3  # Used to interact with SQLite database

app = Flask(__name__)  # Initialize the Flask app

# Set your API keys
openai.api_key = 'OPEN_API_SECRET_KEY' # removed secret key for security reasons 
tmdb_api_key = '2b5cc5a10c5bf3af578238348e7f3683'

# Initialize the SQLite database to store movie data
def init_db():
    conn = sqlite3.connect('movies.db')  # Connect to the database
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    # Create a table to store movie information (title, rating, and revenue)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            rating REAL,
            revenue INTEGER
        )
    ''')
    conn.commit()  # Save the changes to the database
    conn.close()  # Close the connection to the database

# Function to fetch movie data from TMDB API and store it in the database
def fetch_movie_data():
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={tmdb_api_key}&primary_release_date.gte=2000-01-01&primary_release_date.lte=2010-12-31&sort_by=popularity.desc"
    response = requests.get(url)
    data = response.json()

    # Connect to the database and insert movie data
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()

    # Loop through each movie and extract title, rating, and revenue
    for movie in data['results']:
        title = movie['title']
        rating = movie['vote_average']
        revenue = get_movie_revenue(movie['id'])
        cursor.execute("INSERT INTO movies (title, rating, revenue) VALUES (?, ?, ?)", (title, rating, revenue))

    conn.commit()  # Save changes to the database
    conn.close()  # Close the connection

# Function to get movie revenue from TMDB
def get_movie_revenue(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}"
    response = requests.get(url)
    data = response.json()
    return data.get('revenue', 'N/A')  # Return the revenue or 'N/A' if not available

# Route to display the movie data and handle user input for OpenAI
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title, rating, revenue FROM movies")  # Get all movies from the database
    movies = cursor.fetchall()  # Fetch the data
    conn.close()

    # If a user submits a question
    if request.method == 'POST':
        user_question = request.form['question']  # Get the question from the form
        openai_response = ask_openai(user_question)  # Get the answer from OpenAI
        return render_template('index.html', movies=movies, response=openai_response)

    return render_template('index.html', movies=movies, response=None)

# Function to send the user's question to OpenAI and get a response
def ask_openai(question):
    response = openai.Completion.create(
        engine="text-davinci-003",  # The AI engine
        prompt=question,  # The question from the user
        max_tokens=100  # Limit the response length
    )
    return response.choices[0].text.strip()  # Return the text of the AI's response

# Initialize the database when the app starts
init_db()

# Run the app
if __name__ == '__main__':
    fetch_movie_data()  # Fetch the movie data when the app starts
    app.run(debug=True)  # Start the Flask app in debug mode
