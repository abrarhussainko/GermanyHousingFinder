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
    min_price = str(data.get('minPrice', '0'))
    max_price = str(data.get('maxPrice', '1000'))
    housing_type = data.get('housingType', 'all')  # wg, single, full, all

    q_city = urllib.parse.quote(city)
    city_slug = city.lower().replace(" ", "-")

    all_portals = []

    # 1. WG-Gesucht (Shared Rooms & WG Focus)
    if housing_type in ['wg', 'all']:
        all_portals.append({
            "id": "wg_gesucht",
            "source": "WG-Gesucht.de",
            "title": f"WG-Zimmer & Shared Flat Offers in {city}",
            "type": "WG / Shared Room",
            "price_range": f"€{min_price} - €{max_price}/mo",
            "description": f"Direct shared flat rooms and student WG listings in {city}.",
            "applyUrl": f"https://www.wg-gesucht.de/wg-gesucht-in-{q_city}.0.0.0.html"
        })

    # 2. Kleinanzeigen (Private Offers across all budget types)
    all_portals.append({
        "id": "kleinanzeigen",
        "source": "Kleinanzeigen.de",
        "title": f"Private Landlord Offers in {city}",
        "type": "Private Sublet / Flat",
        "price_range": f"€{min_price} - €{max_price}/mo",
        "description": f"Direct postings without agency fees for {housing_type.upper()} housing in {city}.",
        "applyUrl": f"https://www.kleinanzeigen.de/s-wohnung-mieten/{q_city}/preis:{min_price}:{max_price}/c203"
    })

    # 3. Studierendenwerk (Student Dormitories - Filtered for low budget / student status)
    if int(max_price) <= 600 or housing_type in ['wg', 'single', 'all']:
        all_portals.append({
            "id": "studierendenwerk",
            "source": "Studierendenwerk (Dorms)",
            "title": f"University Residences & Student Dorms in {city}",
            "type": "Student Housing",
            "price_range": f"€{min_price} - €{max_price}/mo",
            "description": f"Public subsidized student dormitories and residence halls in {city}.",
            "applyUrl": f"https://www.google.com/search?q={urllib.parse.quote(f'studierendenwerk wohnen {city}')}"
        })

    # 4. Immowelt (Studios & Apartments)
    if housing_type in ['single', 'full', 'all']:
        all_portals.append({
            "id": "immowelt",
            "source": "Immowelt.de",
            "title": f"Studios & Apartments in {city}",
            "type": "Studio / Flat",
            "price_range": f"€{min_price} - €{max_price}/mo",
            "description": f"Verified rental listings matching €{min_price}–€{max_price} in {city}.",
            "applyUrl": f"https://www.immowelt.de/liste/{q_city}/wohnungen/mieten?prmin={min_price}&prmax={max_price}"
        })

    # 5. ImmobilienScout24 (Full Flats)
    if housing_type in ['full', 'single', 'all']:
        all_portals.append({
            "id": "immoscout",
            "source": "ImmobilienScout24",
            "title": f"Flats & Student Accommodation in {city}",
            "type": "Apartment / Flat",
            "price_range": f"€{min_price} - €{max_price}/mo",
            "description": f"ImmoScout24 listings for {city} between €{min_price} and €{max_price}.",
            "applyUrl": f"https://www.immobilienscout24.de/Suche/de/{q_city}/wohnung-mieten?price={min_price}.0-{max_price}.0"
        })

    # 6. WG-Suche
    if housing_type in ['wg', 'all']:
        all_portals.append({
            "id": "wg_suche",
            "source": "WG-Suche.de",
            "title": f"Shared Flats & Student WGs in {city}",
            "type": "WG Room",
            "price_range": f"€{min_price} - €{max_price}/mo",
            "description": f"Filtered WG room search in {city}.",
            "applyUrl": f"https://www.wg-suche.de/wg-zimmer-in-{city_slug}"
        })

    # 7. MeinStadt
    all_portals.append({
        "id": "meinstadt",
        "source": "MeinStadt.de",
        "title": f"Local City Housing in {city}",
        "type": "Local Apartment",
        "price_range": f"€{min_price} - €{max_price}/mo",
        "description": f"Local community housing listings in {city}.",
        "applyUrl": f"https://wohnen.meinstadt.de/{q_city}/immobilien/wohnung-mieten"
    })

    # 8. HousingAnywhere (Furnished / International Student)
    all_portals.append({
        "id": "housinganywhere",
        "source": "HousingAnywhere",
        "title": f"Furnished Student Rooms in {city}",
        "type": "Furnished Flat / Room",
        "price_range": f"€{min_price} - €{max_price}/mo",
        "description": f"Mid-term student accommodation in {city}.",
        "applyUrl": f"https://housinganywhere.com/s/{city}--Germany?priceMin={min_price}00&priceMax={max_price}00"
    })

    # 9. Google Live Custom Search Index
    all_portals.append({
        "id": "google_live",
        "source": "Google Live Index",
        "title": f"Live Indexed Listings for {city}",
        "type": "All Active Portals",
        "price_range": f"€{min_price} - €{max_price}/mo",
        "description": f"Directly query indexed posts on WG-Gesucht & Kleinanzeigen for {city}.",
        "applyUrl": f"https://www.google.com/search?q={urllib.parse.quote(f'site:wg-gesucht.de OR site:kleinanzeigen.de {city} {housing_type} miete {min_price} bis {max_price} euro')}"
    })

    return jsonify({"status": "success", "count": len(all_portals), "data": all_portals})

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
