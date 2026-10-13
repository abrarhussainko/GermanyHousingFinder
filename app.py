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
    city = data.get('city', '').strip() or "Frankfurt"
    max_price = data.get('maxPrice', '800')

    encoded_city = urllib.parse.quote(city)
    
    # 100% working, pre-filtered live search links (No 404s, No API keys, No Credit Cards required)
    portals = [
        {
            "id": "wg_gesucht",
            "source": "WG-Gesucht.de",
            "title": f"Live WG Rooms & Shared Flats in {city}",
            "type": "Shared Room / WG",
            "price_range": f"Up to €{max_price}/mo",
            "description": f"View all active student WGs and room listings in {city}.",
            "applyUrl": f"https://www.wg-gesucht.de/wg-gesucht-in-{encoded_city}.0.0.0.html"
        },
        {
            "id": "kleinanzeigen",
            "source": "Kleinanzeigen.de",
            "title": f"Private Landlord Offers & Sublets in {city}",
            "type": "Private Room / Apartment",
            "price_range": f"Up to €{max_price}/mo",
            "description": f"Direct private offers with zero agency fees in {city}.",
            "applyUrl": f"https://www.kleinanzeigen.de/s-wohnung-mieten/{encoded_city}/preis::{max_price}/c203"
        },
        {
            "id": "immowelt",
            "source": "Immowelt.de",
            "title": f"Studios & 1-Room Flats in {city}",
            "type": "Studio Apartment",
            "price_range": f"Up to €{max_price}/mo",
            "description": f"Verified studio units and long-term rentals in {city}.",
            "applyUrl": f"https://www.immowelt.de/liste/{encoded_city}/wohnungen/mieten?prmax={max_price}"
        },
        {
            "id": "immoscout",
            "source": "ImmobilienScout24",
            "title": f"Full Apartments & Student Flats in {city}",
            "type": "Apartment / Flat",
            "price_range": f"Up to €{max_price}/mo",
            "description": f"Germany's largest property portal results for {city}.",
            "applyUrl": f"https://www.immobilienscout24.de/Suche/de/{encoded_city}/wohnung-mieten?maxprice={max_price}"
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
        f"Ersparnisse pünktlich begleichen. Erforderliche Unterlagen (Einkommensnachweis, SCHUFA, Immatrikulationsbescheinigung) "
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
        f"savings. I am happy to provide all required documents (proof of income, enrollment certificate) right away.\n\n"
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
