import logging
import requests
import os
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from flask import Flask, request, jsonify, render_template
app = Flask(__name__, template_folder="templates")

def get_db_connection():
    # Replace these with your actual database connection details
    db_config = {
        'user': 'root',
        'password': 'root',
        'host': 'mysql',
        'database': 'acestream'
    }
    return mysql.connector.connect(**db_config)

def remove_duplicates(items):
    seen_content_ids = set()
    unique_items = []

    for item in items:
        content_id = item.get('content_id')
        if content_id not in seen_content_ids:
            unique_items.append(item)
            seen_content_ids.add(content_id)

    return unique_items

def clean_builtin(manual_streams, builtin_streams):
    unique_items = builtin_streams;

    for manuel_stream in manual_streams:
        found = False
        for builtin_stream in builtin_streams:
            if manuel_stream.get('content_id') == builtin_stream.get('content_id'):
                found = True
        if not found:
            unique_items.append(manuel_stream)
    return unique_items



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    # Use requests to fetch data from your JSON service
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    words = query.split()
    # SQL query for default streams
    search_sql = "SELECT * FROM streams WHERE name LIKE %s"

    search_term = f"%{query}%"
    cursor.execute(search_sql, (search_term, ))

    # Fetch all matching records
    results = cursor.fetchall()

    # SQL query for default streams
    search_sql = "SELECT \"Submitted manually\" as name, content_id FROM streams_submitted WHERE " + " OR ".join(["keywords LIKE %s" for _ in words])

    params = [f"%{word}%" for word in words]
    cursor.execute(search_sql, params)
    final_result = clean_builtin(remove_duplicates(cursor.fetchall()), results)

    # Close the database connection
    cursor.close()
    conn.close()

    # Return the results as JSON
    return jsonify(final_result)

@app.route('/submit')
def submit():
    return render_template('submit.html')

@app.route('/submit_content_id', methods=['POST'])
def submit_form():
    data = request.json
    content_id = data.get('contentId')
    keywords = data.get('keywords')

    # Validate input
    if not content_id or not keywords:
        return jsonify({'message': 'Content ID and Keywords are required.'}), 400

    if len(content_id) != 40:
        return jsonify({'message': 'Content ID lenght should be 40'}), 400

    try:
        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert data into the database
        insert_query = """
        INSERT INTO streams_submitted (content_id, keywords, inserted_at)
        VALUES (%s, %s, %s)
        """
        inserted_at = datetime.now()
        cursor.execute(insert_query, (content_id, keywords, inserted_at))

        # Commit the transaction
        connection.commit()

        return jsonify({'message': 'Content ID submitted successfully.'}), 200

    except Error as e:
        return jsonify({'message': str(e)}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

if __name__ == '__main__':
    app.run()
