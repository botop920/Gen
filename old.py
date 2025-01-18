import requests
import uuid
from threading import Thread

# Function to send the request
def send_request(available_taps, count, token):
    url = 'https://api-gw.geagle.online/tap'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': f'Bearer {token}',
        'content-type': 'application/json',
        'origin': 'https://telegram.geagle.online',
        'referer': 'https://telegram.geagle.online/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    timestamp = int(time.time())
    salt = str(uuid.uuid4())

    data = {
        "available_taps": available_taps,
        "count": count,  # Attempting a large number of taps
        "timestamp": timestamp,
        "salt": salt
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Response for token {token}: {response.json()}")
    except Exception as e:
        print(f"Error for token {token}: {e}")

# Function to continuously send requests for one token
def handle_token(token):
    while True:
        send_request(available_taps=100000, count=100000, token=token)  # Attempt 100,000 taps
        # No delay to continuously send requests

# Read tokens from data.txt
with open('data.txt', 'r') as file:
    tokens = [line.strip() for line in file.readlines()]

# Create a thread for each token
threads = []
for token in tokens:
    thread = Thread(target=handle_token, args=(token,))
    threads.append(thread)
    thread.start()

# Wait for all threads (script will run indefinitely)
for thread in threads:
    thread.join()
