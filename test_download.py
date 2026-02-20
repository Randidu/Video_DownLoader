
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_download():
    print("Testing download endpoint...")
    url = "https://youtu.be/48PYc8jdyWc?si=Oy7QVV8UkoatZUcU" 
    
    payload = {
        "url": url,
        "format": "mp4",
        "quality": "720p" 
    }
    
    print(f"Sending request to {BASE_URL}/video/download")
    try:
        response = requests.post(f"{BASE_URL}/video/download", json=payload)
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("Success!")
            print(json.dumps(response.json(), indent=2))
        else:
            print("Failed!")
            print(response.text)
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_download()
