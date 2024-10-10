Movie Dashboard with OpenAI Integration
Overview
This project is a Flask-based web application that displays data about the most popular movies from 2000 to 2010. The data includes movie titles, ratings, and revenues, which are pulled from The Movie Database (TMDB) API. Additionally, the app integrates with OpenAI’s API (ChatGPT) to allow users to ask questions about the displayed movies. The project stores this data in an SQLite database and presents it in an organized HTML table.

Features

Movie Data Fetching: Retrieves the most popular movies, their ratings, and revenues using the TMDB API.

AI-Powered Q&A: Users can interact with OpenAI’s API to ask questions about the displayed movies and get responses.

Database Storage: Uses SQLite to store movie data for persistent access.

Flask-based Web Application: Renders the movie data and Q&A interaction in an HTML template.

Real-Time Interaction: Users can ask movie-related questions via a text input field, with AI-generated responses displayed instantly.

Technologies Used:

Python: The primary programming language used for backend development.

Flask: A lightweight web framework used to create the web app.

SQLite: A database to store and retrieve movie data.

TMDB API: Used to fetch movie details like title, ratings, and revenue.

OpenAI API (ChatGPT): Used to generate natural language responses to user queries about the movies.

HTML/CSS: Frontend technologies for rendering the data in a user-friendly format.
