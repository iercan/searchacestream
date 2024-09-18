import requests
import mysql.connector

def fetch_data():
    url = "https://api.acestream.me/all?api_version=1.0&api_key=test_api_key"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    return response.json()

def save_to_database(data):
    # Replace these with your actual database connection details
    db_config = {
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
        'database': 'acestream'
    }

    # Establish a database connection
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()


    # Assuming a table named 'streams' with appropriate columns
    insert_sql = """
    INSERT INTO streams (infohash, name, content_id, categories, availability, availability_updated_at)
    VALUES (%s, %s, %s, %s, %s, FROM_UNIXTIME(%s))
    """

    # Prepare data for bulk insert
    bulk_data = []
    for entry in data:
        infohash=entry["infohash"]
        # Use requests to fetch data from your JSON service
        response = requests.get(f'http://localhost:6878/server/api?api_version=3&method=get_content_id&infohash={infohash}')
        content_id = response.json().get('result', {}).get("content_id", "")
        print(entry)
        print(content_id)
        categories = ', '.join(entry.get("categories",[]))  # Convert list to comma-separated string
        bulk_data.append((
            entry["infohash"],
            entry["name"],
            content_id,
            categories,
            entry["availability"],
            entry["availability_updated_at"]
        ))

    # Clean the table before inserting new data
    cursor.execute("DELETE FROM streams")
    # Execute bulk insert
    cursor.executemany(insert_sql, bulk_data)

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

def main():
    data = fetch_data()
    save_to_database(data)
    print("Data successfully fetched and stored in database.")

if __name__ == "__main__":
    main()
