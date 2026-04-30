import requests
from app.config import Config

def generate_from_llm(prompt: str):
    # For testing purposes, return mock response instead of calling real API
    # Uncomment the code below to use real API when token is available

    # response = requests.post(
    #     f"{Config.BASE_URL}/llm/chat",
    #     json={
    #         "token": Config.LLM_TOKEN,
    #         "chat": prompt
    #     }
    # )
    #
    # if response.status_code != 200:
    #     raise Exception("LLM request failed")
    #
    # return response.json()

    # Mock response for testing
    mock_response = {
        "response": '''```json
{
    "motivations": [
        {"text": "Jangan pernah menyerah dalam menghadapi tantangan"},
        {"text": "Setiap hari adalah kesempatan baru untuk sukses"},
        {"text": "Percayalah pada dirimu sendiri"},
        {"text": "Kerja keras akan membuahkan hasil"},
        {"text": "Tetaplah positif dalam segala situasi"}
    ]
}
```'''
    }
    return mock_response