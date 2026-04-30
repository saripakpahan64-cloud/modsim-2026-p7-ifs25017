import requests
from app.config import Config

def generate_from_llm(prompt: str, model: str = "anthropic/claude-opus-4.7", max_tokens: int = 1000):
    if Config.BASE_URL and Config.LLM_TOKEN:
        try:
            response = requests.post(
                f"{Config.BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {Config.LLM_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                }
            )

            if response.status_code != 200:
                raise Exception(f"LLM request failed: {response.status_code} {response.text}")

            return response.json()
        except Exception as e:
            print(f"API call failed: {e}, falling back to mock")

    # Mock response for testing when API credentials are not configured or API fails
    mock_content = '''{
  "destination": "Bali",
  "duration_days": 3,
  "people": 2,
  "budget": "murah",
  "budget_label": "Anggaran murah",
  "total_estimated_cost": "Rp 3.500.000",
  "currency": "IDR",
  "days": [
    {
      "day": 1,
      "title": "Wisata Alam Pantai",
      "activities": [
        {
          "time": "09:00",
          "name": "Pantai Kuta",
          "icon": "🏖",
          "estimated_cost": "Rp 50.000 / orang",
          "tip": "Bangun pagi untuk menikmati matahari terbit tanpa keramaian."
        },
        {
          "time": "12:00",
          "name": "Makan Siang Seafood",
          "icon": "🍤",
          "estimated_cost": "Rp 75.000 / orang",
          "tip": "Coba warung lokal untuk rasa autentik."
        },
        {
          "time": "15:00",
          "name": "Pantai Legian",
          "icon": "🏄",
          "estimated_cost": "Rp 30.000 / orang",
          "tip": "Sempurna untuk surfing pemula."
        }
      ]
    },
    {
      "day": 2,
      "title": "Eksplorasi Budaya",
      "activities": [
        {
          "time": "08:00",
          "name": "Pura Tanah Lot",
          "icon": "🕍",
          "estimated_cost": "Rp 100.000 / orang",
          "tip": "Datang saat matahari terbenam untuk pemandangan terbaik."
        },
        {
          "time": "11:00",
          "name": "Pasar Seni Ubud",
          "icon": "🎨",
          "estimated_cost": "Rp 50.000 / orang",
          "tip": "Tawar harga untuk souvenir unik."
        },
        {
          "time": "14:00",
          "name": "Restoran Tradisional",
          "icon": "🍛",
          "estimated_cost": "Rp 80.000 / orang",
          "tip": "Coba ayam betutu khas Bali."
        }
      ]
    },
    {
      "day": 3,
      "title": "Petualangan Alam",
      "activities": [
        {
          "time": "07:00",
          "name": "Gunung Batur Sunrise Trek",
          "icon": "🏔",
          "estimated_cost": "Rp 200.000 / orang",
          "tip": "Bawa jaket hangat dan minum banyak air."
        },
        {
          "time": "12:00",
          "name": "Danau Batur",
          "icon": "🏞",
          "estimated_cost": "Rp 50.000 / orang",
          "tip": "Nikmati pemandangan danau vulkanik."
        },
        {
          "time": "16:00",
          "name": "Kembali ke Kuta",
          "icon": "🚗",
          "estimated_cost": "Rp 100.000 / orang",
          "tip": "Istirahat sebelum penerbangan."
        }
      ]
    }
  ],
  "local_tips": [
    "Beli oleh-oleh di pasar seni setelah jam 10 pagi.",
    "Gunakan ojek online untuk jarak pendek.",
    "Bawa sunblock dan air minum.",
    "Coba makanan lokal di warung pinggir jalan.",
    "Hormati adat istiadat setempat."
  ]
}'''
    return {
        "choices": [
            {
                "message": {
                    "content": mock_content
                }
            }
        ]
    }
