import logging
import requests
import os
import mysql.connector
from flask import Flask, request, jsonify, render_template
app = Flask(__name__, template_folder="templates")


ENGINE_URL = os.getenv("ENGINE_URL")

def get_db_connection():
    # Replace these with your actual database connection details
    db_config = {
        'user': 'root',
        'password': 'root',
        'host': 'mysql',
        'database': 'acestream'
    }
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_content_id', methods=['GET'])
def get_content_id():
    infohash = request.args.get('infohash')
    # Use requests to fetch data from your JSON service
    response = requests.get(f'{ENGINE_URL}/server/api?api_version=3&method=get_content_id&infohash={infohash}')
    data = response.json().get('result', {})
    return data

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    # Use requests to fetch data from your JSON service
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # SQL query to search for streams by name or categories
    search_sql = """
    SELECT infohash, name, categories, availability, availability_updated_at, content_id
    FROM streams
    WHERE name LIKE %s  ORDER BY name
    """
    search_term = f"%{query}%"
    cursor.execute(search_sql, (search_term,))

    # Fetch all matching records
    results = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    # Return the results as JSON
    return jsonify(results)


gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

if __name__ == '__main__':
    app.run()
