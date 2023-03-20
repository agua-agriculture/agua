import requests

BASE_URL="http://127.0.0.1:5000"

def test_create():
    resp = requests.post(BASE_URL + '/send-recommendations')
    print(resp.json())

if __name__ == '__main__':
    test_create()