import requests
import json
from data import BITLY_API_KEY

headers = {
    'Authorization': f'Bearer {BITLY_API_KEY}',
    'Content-Type': 'application/json',
}
data = '{"long_url": "https://youtube.com"}'
response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers = headers, data = data)
json_data = json.loads(response.text)
print(json_data['id'])