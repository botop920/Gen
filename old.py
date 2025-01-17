import requests
import time
import uuid
import threading

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
        return response.json()
    except Exception as e:
        print(f"Error sending request: {e}")
        return None

# Worker function to process taps for each token
def process_taps(token, count):
    while True:
        try:
            # Send request to use the maximum taps
            response = send_request(1000, count, token)
            if response:
                print(f"Response for token {token}: {response}")
                if "remaining_taps" in response:
                    remaining_taps = response["remaining_taps"]
                    if remaining_taps <= 0:
                        print(f"Taps exhausted for token {token}. Skipping...")
                        break  # Stop thread for this token if taps are exhausted
        except Exception as e:
            print(f"Error sending request for token {token}: {e}")
            break

# Read the Bearer token from data.txt
with open('data.txt', 'r') as file:
    token = file.readline().strip()

# Fixed values
count = 1000  # Max taps per request (each request = 1000 taps)
target_points_per_second = 10000  # Points required per second

# Calculate the number of requests per second to achieve 10k points/s
requests_per_second = target_points_per_second // 1000  # Each request gives 1000 points

# Start multiple threads for sending requests as fast as possible
threads = []
for _ in range(requests_per_second):
    thread = threading.Thread(target=process_taps, args=(token, count))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()
