import os
import urllib.parse
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/search', methods=['POST'])
def search_housing():
    data = request.json or {}
    city = data.get('city', '').strip()
    max_price = data.get('maxPrice', '1000')
    housing_type = data.get('housingType', 'all')

    encoded_city = urllib.parse.quote(city) if city else "Giessen"

    # Direct Search Portal Links (Official Real-Time Platforms)
    portals = [
        {
            "id": "wg_gesucht",
            "source": "WG-Gesucht.de",
            "title": f"Live WG & Apartment Listings in {city or 'Germany'}",
            "type": "wg" if housing_type in ['wg', 'all'] else "single",
            "price": f"Up to €{max_price}/mo",
            "description": f"Browse active, real-time listings in {city or 'Germany'} directly on WG-Gesucht with zero filters blocked.",
            "directLink": f"https://www.wg-gesucht.de/wg-gesucht-in-{encoded_city}.0.0.0.html",
            "image": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": "kleinanzeigen",
            "source": "Kleinanzeigen.de",
            "title": f"Private Landlord Offers in {city or 'Germany'}",
            "type": "full" if housing_type == 'full' else "all",
            "price": f"Up to €{max_price}/mo",
            "description": f"Direct landlord posts, shared flats, and sublets available in {city or 'Germany'}.",
            "directLink": f"https://www.kleinanzeigen.de/s-wohnung-mieten/{encoded_city}/c203",
            "image": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": "immowelt",
            "source": "Immowelt.de",
            "title": f"Verified Apartments & Studios in {city or 'Germany'}",
            "type": "single",
            "price": f"Up to €{max_price}/mo",
            "description": f"Professional real estate listings, studios, and long-term apartments in {city or 'Germany'}.",
            "directLink": f"https://www.immowelt.de/liste/{encoded_city}/wohnungen/mieten",
            "image": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": "immoscout",
            "source": "ImmobilienScout24",
            "title": f"ImmoScout24 Housing Feed - {city or 'Germany'}",
            "type": "full",
            "price": f"Up to €{max_price}/mo",
            "description": f"Germany's largest property portal live search results for {city or 'Germany'}.",
            "directLink": f"https://www.immobilienscout24.de/Suche/de/{encoded_city}/wohnung-mieten",
            "image": "https://images.unsplash.com/photo-1493809842364-78817add7ffb?auto=format&fit=crop&w=600&q=80"
        }
    ]

    return jsonify({"status": "success", "count": len(portals), "data": portals})

@app.route('/api/generate-message', methods=['POST'])
def generate_message():
    data = request.json or {}
    name = data.get('name', '').strip() or "[Your Name]"
    email = data.get('email', '').strip() or "[Your Email]"
    phone = data.get('phone', '').strip() or "[Your Phone Number]"
    occupation = data.get('occupation', '').strip() or "[Your Occupation/Student Status]"
    status = data.get('status', 'Applicant')
    city = data.get('city', '').strip() or "[City]"
    move_date = data.get('moveDate', '').strip() or "as soon as possible"
    listing_title = data.get('listingTitle', 'your accommodation listing')
    listing_source = data.get('listingSource', 'your portal')

    german_msg = (
        f"Sehr geehrte Damen und Herren / Hallo,\n\n"
        f"über {listing_source} habe ich Ihre Anzeige (\"{listing_title}\") in {city} gesehen "
        f"und interessiere mich sehr dafür.\n\n"
        f"Zu meiner Person:\n"
        f"- Name: {name}\n"
        f"- Beruf / Status: {occupation} ({status})\n"
        f"- Geplanter Einzugstermin: {move_date}\n\n"
        f"Ich bin eine ruhige, saubere und zuverlässige Person. Die Miete kann ich durch eigenes Einkommen / "
        f"Ersparnisse pünktlich begleichen. Erforderliche Unterlagen (Einkommensnachweis, SCHUFA, Selbstauskunft) "
        f"stelle ich Ihnen gerne direkt zur Verfügung.\n\n"
        f"Über die Möglichkeit zu einem Besichtigungstermin würde ich mich sehr freuen.\n\n"
        f"Mit freundlichen Grüßen,\n"
        f"{name}\n"
        f"E-Mail: {email}\n"
        f"Telefon: {phone}"
    )

    english_translation = (
        f"Dear Sir/Madam / Hello,\n\n"
        f"I came across your listing (\"{listing_title}\") in {city} on {listing_source} "
        f"and I am very interested.\n\n"
        f"About me:\n"
        f"- Name: {name}\n"
        f"- Profession / Status: {occupation} ({status})\n"
        f"- Intended move-in date: {move_date}\n\n"
        f"I am a quiet, tidy, and responsible person. I can reliably pay the rent on time through my income / "
        f"savings. I am happy to provide all required documents (proof of income, SCHUFA credit check) right away.\n\n"
        f"I would be delighted to arrange a viewing appointment.\n\n"
        f"Best regards,\n"
        f"{name}\n"
        f"Email: {email}\n"
        f"Phone: {phone}"
    )

    return jsonify({
        "status": "success",
        "german": german_msg,
        "english": english_translation
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
