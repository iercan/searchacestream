import logging
import requests
import os
from flask import Flask, request, jsonify, render_template
app = Flask(__name__, template_folder="templates")


ENGINE_URL = os.getenv("ENGINE_URL")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_content_id', methods=['POST'])
def get_content_id():
    infohash = request.form.get('infohash')
    # Use requests to fetch data from your JSON service
    response = requests.get(f'{ENGINE_URL}/server/api?api_version=3&method=get_content_id&infohash={infohash}')
    data = response.json()['result']
    return data

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    # Use requests to fetch data from your JSON service
    response = requests.get(f'{ENGINE_URL}/search?page_size=200&query={query}')
    data = response.json()['result']['results']
    results = []

    # Extract relevant data
    for item in data:
        for detail in item['items']:
            results.append({
                'name': item['name'],
                'infohash': detail['infohash'],
                'availability': detail['availability'],
                'status': detail['status'],
                'languages': ', '.join(detail.get('languages', []))
            })

    return jsonify(results)


gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

if __name__ == '__main__':
    app.run()
