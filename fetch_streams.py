import requests
import mysql.connector
from datetime import datetime, timedelta

def get_db_connection():
    db_config = {
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
        'database': 'acestream'
    }
    return mysql.connector.connect(**db_config)


def fetch_data():
    url = "https://api.acestream.me/all?api_version=1.0&api_key=test_api_key"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    return response.json()

def create_playlist(data):
    ace_content = ["#EXTM3U"]
    vlc_content = ["#EXTM3U"]

    ace_file = '/root/playlists/playlist_ace.m3u8'
    vlc_file = '/root/playlists/playlist_vlc.m3u8'
    pid=1

    for entry in data:
        name = entry[1]
        content_id = entry[2]
        vlc_content.append(f"#EXTINF:-1,{name}")
        vlc_content.append(f"http://127.0.0.1:6878/ace/getstream?id={content_id}&pid={pid}")
        ace_content.append(f"#EXTINF:-1,{name}")
        ace_content.append(f"acestream://{content_id}")
        pid += 1

    with open(ace_file, 'w') as file:
        file.write("\n".join(ace_content))

    with open(vlc_file, 'w') as file:
        file.write("\n".join(vlc_content))



def save_to_database(data):

    # Establish a database connection
    conn = get_db_connection()
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
    print("Data successfully fetched and stored in database.")
    return bulk_data

def remove_expired_streams():

    connection = get_db_connection()
    # Create a cursor object
    cursor = connection.cursor()

    # Calculate the cutoff time
    cutoff_time = datetime.now() - timedelta(hours=72)

    # Prepare the SQL query to delete entries
    query = "DELETE FROM streams_submitted WHERE inserted_at < %s"

    # Execute the query
    cursor.execute(query, (cutoff_time,))

    # Commit the changes to the database
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    print("Streams older than 72 hours have been removed.")




def main():
    data = fetch_data()
    bulk_data = save_to_database(data)
    create_playlist(bulk_data)
    remove_expired_streams()

if __name__ == "__main__":
    main()
