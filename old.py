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
        
        # Print response details for debugging
        print(f"Request Data: {data}")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        
        # Attempt to parse the JSON response
        return response.json()
    except Exception as e:
        print(f"Error sending request: {e}")
        return None
