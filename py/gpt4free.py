import requests
url = "http://localhost:1337/v1/chat/completions"

while True:
    prompt = input(">>> ")
    body = {
        "model": "gpt-3.5-turbo-16k",
        "stream": False,
        "messages": [
            {"role": "assistant", "content": prompt}
            ]
        }
    json_response = requests.post(url, json=body).json().get('choices', [])
    for choice in json_response:
        print(choice.get('message', {}).get('content', ''))
