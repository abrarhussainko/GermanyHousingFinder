import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

# Anti-scam filter keyword check
SCAM_KEYWORDS = [
    "western union", "moneygram", "airbnb booking", "keys by mail", 
    "currently abroad", "transfer advance", "pay deposit before viewing"
]

def is_safe_listing(description, price):
    desc_lower = description.lower()
    for word in SCAM_KEYWORDS:
        if word in desc_lower:
            return False
    if price < 150: # Unusually low rent flag for Germany
        return False
    return True

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/search', methods=['POST'])
def search_housing():
    data = request.json or {}
    city = data.get('city', 'Giessen').title()
    min_price = float(data.get('minPrice', 0))
    max_price = float(data.get('maxPrice', 2500))
    housing_type = data.get('housingType', 'all')

    # Mock accommodation database (Scraper targets connect here)
    all_listings = [
        {
            "id": 1,
            "title": f"Modern Cozy Studio Apartment - {city}",
            "city": city,
            "type": "single",
            "price": 380,
            "deposit": 760,
            "size": "28 m²",
            "occupants": 1,
            "images": [
                "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=600&q=80"
            ],
            "verified": True,
            "source": "WG-Gesucht",
            "sourceUrl": "https://www.wg-gesucht.de",
            "description": f"Spacious renovated studio in central {city}. Fully furnished with high-speed internet."
        },
        {
            "id": 2,
            "title": f"Friendly Shared Flat (WG Room) - {city}",
            "city": city,
            "type": "wg",
            "price": 310,
            "deposit": 600,
            "size": "22 m²",
            "occupants": 3,
            "images": [
                "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=600&q=80"
            ],
            "verified": True,
            "source": "Kleinanzeigen",
            "sourceUrl": "https://www.kleinanzeigen.de",
            "description": f"Bright room available in a 3-person shared flat in {city}. Close to public transit."
        },
        {
            "id": 3,
            "title": f"Spacious 2-Room Family Apartment - {city}",
            "city": city,
            "type": "full",
            "price": 750,
            "deposit": 1500,
            "size": "58 m²",
            "occupants": 2,
            "images": [
                "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=600&q=80"
            ],
            "verified": True,
            "source": "Immowelt",
            "sourceUrl": "https://www.immowelt.de",
            "description": f"Quiet 2-room apartment in {city} with balcony and built-in kitchen."
        }
    ]

    filtered = []
    for item in all_listings:
        if min_price <= item['price'] <= max_price:
            if housing_type == 'all' or item['type'] == housing_type:
                if is_safe_listing(item['description'], item['price']):
                    filtered.append(item)

    return jsonify({"status": "success", "count": len(filtered), "data": filtered})

@app.route('/api/generate-message', methods=['POST'])
def generate_message():
    data = request.json or {}
    name = data.get('name', 'Applicant')
    email = data.get('email', '')
    occupation = data.get('occupation', 'Professional / Student')
    status = data.get('status', 'Working Professional')
    city = data.get('city', 'Germany')
    move_date = data.get('moveDate', 'as soon as possible')
    listing_title = data.get('listingTitle', 'your apartment listing')

    german_msg = (
        f"Sehr geehrte Damen und Herren / Hallo,\n\n"
        f"mein Name ist {name} und ich interessiere mich sehr für Ihre Unterkunft "
        f"(\"{listing_title}\") in {city}.\n\n"
        f"Aktuell bin ich als {occupation} ({status}) tätig. Ich bin eine zuverlässige, "
        f"ruhige und ordentliche Person und suche eine passende Unterkunft ab {move_date}.\n\n"
        f"Die Miete kann ich durch eigenes Einkommen / Ersparnisse problemlos sicherstellen. "
        f"Gerne lasse ich Ihnen bei Bedarf weitere Unterlagen (Einkommensnachweis, SCHUFA) zukommen.\n\n"
        f"Über die Gelegenheit zu einer Besichtigung würde ich mich sehr freuen.\n\n"
        f"Mit freundlichen Grüßen,\n"
        f"{name}\n"
        f"E-Mail: {email}"
    )

    english_translation = (
        f"Dear Sir/Madam / Hello,\n\n"
        f"My name is {name} and I am very interested in your accommodation "
        f"(\"{listing_title}\") in {city}.\n\n"
        f"Currently, I am working/studying as {occupation} ({status}). I am a reliable, "
        f"quiet, and tidy person looking for suitable accommodation starting from {move_date}.\n\n"
        f"I can reliably cover the rent through personal income / savings. "
        f"I would be happy to provide further documents (proof of income, SCHUFA) if needed.\n\n"
        f"I would be delighted to have the opportunity for a viewing.\n\n"
        f"Best regards,\n"
        f"{name}\n"
        f"Email: {email}"
    )

    return jsonify({
        "status": "success",
        "german": german_msg,
        "english": english_translation
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)