import requests
import time
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
        "count": count,
        "timestamp": timestamp,
        "salt": salt
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Check for HTTP errors
        try:
            return response.json()  # Attempt to parse JSON
        except ValueError:
            print(f"Non-JSON response for token {token}: {response.text}")
            return {"error": "Invalid JSON response"}
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed for token {token}: {e}")
        return {"error": str(e)}

# Function to continuously send requests for one token
def handle_token(token):
    while True:
        response = send_request(available_taps=1000, count=1000, token=token)  # Start with smaller values
        print(f"Response for token {token}: {response}")
        time.sleep(0.1)  # Small delay to avoid overload

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
