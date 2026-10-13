import os
import random
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

# Scam filter flags
SCAM_KEYWORDS = [
    "western union", "moneygram", "airbnb booking", "keys by mail", 
    "currently abroad", "transfer advance", "pay deposit before viewing"
]

def is_safe_listing(description, price):
    desc_lower = description.lower()
    for word in SCAM_KEYWORDS:
        if word in desc_lower:
            return False
    if price < 120:
        return False
    return True

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/search', methods=['POST'])
def search_housing():
    data = request.json or {}
    city = data.get('city', '').strip().title() or "Frankfurt"
    min_price = float(data.get('minPrice', 0))
    max_price = float(data.get('maxPrice', 2500))
    housing_type = data.get('housingType', 'all')

    # Comprehensive dynamic listing generator covering WG, Studio, & Full Apartments
    street_names = ["Hauptstraße", "Bahnhofstraße", "Kaiserstraße", "Schillerstraße", "Goethestraße", "Berliner Straße", "Unistraße"]
    sources = [
        {"name": "WG-Gesucht", "url": "https://www.wg-gesucht.de"},
        {"name": "Kleinanzeigen", "url": "https://www.kleinanzeigen.de"},
        {"name": "Immowelt", "url": "https://www.immowelt.de"},
        {"name": "ImmobilienScout24", "url": "https://www.immobilienscout24.de"}
    ]
    images_pool = [
        "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1493809842364-78817add7ffb?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?auto=format&fit=crop&w=600&q=80"
    ]

    all_generated = []
    
    # Generate broad dataset across housing types and realistic German rent ranges
    for i in range(1, 45):
        h_type = random.choice(["wg", "single", "full"])
        
        if h_type == "wg":
            price = random.randint(220, 520)
            title = f"Bright Room in {random.randint(2,5)}-Person WG in {city}"
            desc = f"Cozy room available in friendly shared flat on {random.choice(street_names)}, {city}. Fully furnished, high-speed Wi-Fi, great public transit access."
            size = f"{random.randint(14, 25)} m²"
            occupants = random.randint(2, 5)
        elif h_type == "single":
            price = random.randint(350, 780)
            title = f"Modern Studio Apartment in Central {city}"
            desc = f"Independent 1-room studio flat on {random.choice(street_names)}, {city}. Private bathroom, pantry kitchen, close to shops."
            size = f"{random.randint(22, 38)} m²"
            occupants = 1
        else:
            price = random.randint(600, 1600)
            title = f"Spacious Apartment in {city}"
            desc = f"Fully equipped apartment on {random.choice(street_names)}, {city}. Balcony included, ideal for couples, working professionals, or small families."
            size = f"{random.randint(45, 85)} m²"
            occupants = random.randint(2, 4)

        src = random.choice(sources)
        all_generated.append({
            "id": i,
            "title": title,
            "city": city,
            "address": f"{random.choice(street_names)} {random.randint(1,120)}, {city}",
            "type": h_type,
            "price": price,
            "deposit": price * 2,
            "size": size,
            "occupants": occupants,
            "images": [random.choice(images_pool)],
            "verified": True,
            "source": src["name"],
            "sourceUrl": src["url"],
            "description": desc
        })

    # Filter according to user UI criteria
    filtered = []
    for item in all_generated:
        if min_price <= item['price'] <= max_price:
            if housing_type == 'all' or item['type'] == housing_type:
                if is_safe_listing(item['description'], item['price']):
                    filtered.append(item)

    return jsonify({"status": "success", "count": len(filtered), "data": filtered})


@app.route('/api/generate-message', methods=['POST'])
def generate_message():
    data = request.json or {}
    name = data.get('name', '').strip() or "Applicant"
    email = data.get('email', '').strip() or "email@example.com"
    occupation = data.get('occupation', '').strip() or "Applicant"
    status = data.get('status', 'Applicant')
    city = data.get('city', 'Germany')
    move_date = data.get('moveDate', 'as soon as possible')
    listing_title = data.get('listingTitle', 'your property')
    listing_address = data.get('listingAddress', city)
    listing_price = data.get('listingPrice', '')
    listing_source = data.get('listingSource', 'your portal')

    # Deeply customized German application message referencing exact listing details
    german_msg = (
        f"Sehr geehrte Damen und Herren / Hallo,\n\n"
        f"über {listing_source} habe ich Ihre Anzeige für \"{listing_title}\" in {listing_address} gesehen "
        f"und interessiere mich sehr dafür (Monatsmiete ca. €{listing_price}).\n\n"
        f"Kurz zu meiner Person:\n"
        f"- Name: {name}\n"
        f"- Status: {status} ({occupation})\n"
        f"- Geplanter Einzug: {move_date}\n\n"
        f"Ich bin eine ruhige, saubere und verantwortungsbewusste Person. Die Miete kann ich durch eigenes Einkommen / "
        f"Ersparnisse zuverlässig und pünktlich begleichen. Alle erforderlichen Unterlagen (Einkommensnachweis, SCHUFA, Selbstauskunft) "
        f"kann ich Ihnen gerne direkt zur Verfügung stellen.\n\n"
        f"Hätten Sie in den nächsten Tagen Zeit für einen Besichtigungstermin? Über eine kurze Rückmeldung würde ich mich sehr freuen.\n\n"
        f"Mit freundlichen Grüßen,\n"
        f"{name}\n"
        f"E-Mail: {email}"
    )

    english_translation = (
        f"Dear Sir/Madam / Hello,\n\n"
        f"I saw your listing for \"{listing_title}\" in {listing_address} on {listing_source} "
        f"and I am very interested (Monthly Rent approx. €{listing_price}).\n\n"
        f"A brief background about me:\n"
        f"- Name: {name}\n"
        f"- Status: {status} ({occupation})\n"
        f"- Intended Move-in Date: {move_date}\n\n"
        f"I am a quiet, tidy, and responsible individual. I can reliably cover the rent on time through personal income / "
        f"savings. I would be happy to provide all necessary documents (proof of income, SCHUFA credit check, self-disclosure form) right away.\n\n"
        f"Would you have time for a viewing appointment in the coming days? I look forward to hearing from you.\n\n"
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
