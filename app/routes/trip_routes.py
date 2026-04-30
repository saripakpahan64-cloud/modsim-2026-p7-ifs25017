import json

from flask import Blueprint, request, jsonify

from app.services.llm_service import generate_from_llm

trip_bp = Blueprint("trip", __name__)


def _extract_text(response):
    if isinstance(response, dict):
        # OpenRouter / OpenAI compatible responses
        choices = response.get("choices")
        if choices and isinstance(choices, list):
            first = choices[0]
            message = first.get("message") if isinstance(first, dict) else None
            if message and isinstance(message, dict):
                return message.get("content") or ""
            return first.get("text") or ""

        if "response" in response:
            return response.get("response", "")

    return str(response)


@trip_bp.route("/trip/generate", methods=["POST"])
def generate_trip():
    data = request.get_json() or {}
    destination = (data.get("destination") or "").strip()
    duration = data.get("duration") or data.get("duration_days") or 3
    people = data.get("people") or 1
    budget = (data.get("budget") or "murah").strip().lower()

    if not destination:
        return jsonify({"error": "Destination is required"}), 400

    try:
        duration = int(duration)
        people = int(people)
    except (ValueError, TypeError):
        return jsonify({"error": "Duration and people must be numbers"}), 400

    if duration < 1 or duration > 30:
        return jsonify({"error": "Duration must be between 1 and 30"}), 400
    if people < 1 or people > 50:
        return jsonify({"error": "People must be between 1 and 50"}), 400
    if budget not in {"murah", "sedang", "mewah"}:
        budget = "murah"

    prompt = f"""
Kamu adalah travel planner ahli Indonesia. Buat itinerary perjalanan wisata ke \"{destination}\" selama {duration} hari untuk {people} orang dengan anggaran {budget}.

Balas HANYA dengan JSON valid berikut (tanpa markdown, tanpa penjelasan lain):
{{
  "destination": "nama kota",
  "duration_days": {duration},
  "people": {people},
  "budget": "{budget}",
  "budget_label": "label anggaran dalam bahasa Indonesia",
  "total_estimated_cost": "estimasi total biaya dalam Rupiah (format: Rp X.XXX.000)",
  "currency": "IDR",
  "days": [
    {{
      "day": 1,
      "title": "judul hari singkat",
      "activities": [
        {{
          "time": "08:00",
          "name": "nama aktivitas/destinasi",
          "icon": "emoji satu karakter",
          "estimated_cost": "Rp XX.000 / orang",
          "tip": "tips lokal singkat dan berguna"
        }}
      ]
    }}
  ],
  "local_tips": ["tip 1", "tip 2", "tip 3"]
}}

Isi {duration} hari dengan 3-4 aktivitas per hari. Gunakan nama tempat nyata di {destination}. Estimasi biaya sesuai level anggaran {budget}."""

    try:
        print("Calling generate_from_llm")
        response = generate_from_llm(prompt)
        raw_text = _extract_text(response)
        cleaned = raw_text.replace("```json", "").replace("```", "").strip()
        plan = json.loads(cleaned)

        return jsonify({"plan": plan})

    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
