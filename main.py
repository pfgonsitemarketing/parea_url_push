import streamlit as st
from urllib.parse import urlencode, urlparse, urlunparse, quote
from datetime import datetime, date, time
import json
import os

# ---------------------------------
# Basis-Links
# ---------------------------------
basis_links = {
    "Happy Size BEFR": "https://www.happy-size.be/fr",
    "Happy Size BENL": "https://www.happy-size.be/nl",
    "Happy Size CHDE": "https://www.happy-size.ch/de",
    "Happy Size CHFR": "https://www.happy-size.ch/fr",
    "Happy Size DE": "https://www.happy-size.de/de",
    "Happy Size FR": "https://www.happy-size.fr/fr",
    "Happy Size NL": "https://www.happy-size.nl/nl",

    "JP1880 BEFR": "https://www.jp1880.be/fr",
    "JP1880 BENL": "https://www.jp1880.be/nl",
    "JP1880 CHDE": "https://www.jp1880.ch/de",
    "JP1880 CHFR": "https://www.jp1880.ch/fr",
    "JP1880 DE": "https://www.jp1880.de/de",
    "JP1880 FR": "https://www.jp1880.fr/fr",
    "JP1880 NL": "https://www.jp1880.nl/nl",
    "JP1880 PL": "https://www.jp1880.pl/pl",

    "Laurason DE": "https://www.laurason.de/de",

    "Studio Untold DE": "https://www.studiountold.de/de",

    "Ulla Popken AT": "https://www.ullapopken.at/de",
    "Ulla Popken BEFR": "https://www.ullapopken.be/fr",
    "Ulla Popken BENL": "https://www.ullapopken.be/nl",
    "Ulla Popken CHDE": "https://www.ullapopken.ch/de",
    "Ulla Popken CHFR": "https://www.ullapopken.ch/fr",
    "Ulla Popken CZ": "https://www.ullapopken.cz/cs",
    "Ulla Popken DE": "https://www.ullapopken.de/de",
    "Ulla Popken DK": "https://www.ullapopken.dk/da",
    "Ulla Popken ES": "https://www.ullapopken.es/es",
    "Ulla Popken EUDE": "https://www.ullapopken.eu/de",
    "Ulla Popken EUEN": "https://www.ullapopken.eu/en",
    "Ulla Popken FI": "https://www.ullapopken.fi/fi",
    "Ulla Popken FR": "https://www.ullapopken.fr/fr",
    "Ulla Popken IT": "https://www.ullapopken.it/it",
    "Ulla Popken NL": "https://www.ullapopken.nl/nl",
    "Ulla Popken NO": "https://www.ullapopken.no/no",
    "Ulla Popken PL": "https://www.ullapopken.pl/pl",
    "Ulla Popken RO": "https://www.ullapopken.ro/ro",
    "Ulla Popken SE": "https://www.ullapopken.se/sv",
    "Ulla Popken UK": "https://www.ullapopken.co.uk/en",
    "Ulla Popken US": "https://www.ullapopken.com/en",
}

# ---------------------------------
# Streamlit App
# ---------------------------------
st.set_page_config(page_title="Promo-URL Generator", layout="wide")

st.title("🔗 PromoArea Dynamic Promo Generator")

# ---------------------------------
# Basisfelder
# ---------------------------------
selected_shop = st.selectbox("Shop", list(basis_links.keys()))
base_url = st.text_input("Basis-URL", value=basis_links[selected_shop])

title = st.text_input("Title *")
claim = st.text_input("Claim")
cta = st.text_input("CTA *")
code = st.text_input("Code")
target_url = st.text_input("Ziel-URL *")
tracking = st.text_input("Tracking")

# ---------------------------------
# Datum & Uhrzeit
# ---------------------------------
st.subheader("Datum & Uhrzeit (todate)")

col1, col2, col3 = st.columns(3)

with col1:
    selected_date = st.date_input("Datum", value=date.today())

with col2:
    selected_hour = st.number_input("Stunde", min_value=0, max_value=23, value=datetime.now().hour)

with col3:
    selected_minute = st.number_input("Minute", min_value=0, max_value=59, value=datetime.now().minute)

todate = f"{selected_date.strftime('%Y-%m-%d')}T{int(selected_hour):02d}:{int(selected_minute):02d}"

# ---------------------------------
# Preselected
# ---------------------------------
preselected = st.radio("Preselected", ["0", "1"], format_func=lambda x: "Inaktiv" if x == "0" else "Aktiv")

# ---------------------------------
# URL generieren
# ---------------------------------
if st.button("URL generieren"):

    if not all([base_url, title, cta, target_url]):
        st.error("Bitte alle Pflichtfelder ausfüllen.")
    else:

        parsed_target = urlparse(target_url)
        relative_url = parsed_target.path or "/"
        if parsed_target.query:
            relative_url += "?" + parsed_target.query

        params = {
            "parea_push": "true",
            "title": title.strip(),
            "cta": cta.strip(),
            "href": relative_url,
            "todate": todate,
            "pre": preselected,
        }

        if claim:
            params["claim"] = claim.strip()
        if code:
            params["code"] = code.strip()

        query = urlencode(params, quote_via=quote)

        tracking_encoded = quote(tracking.strip(), safe="")
        if tracking_encoded:
            query += "&" + tracking_encoded

        parsed_base = urlparse(base_url)
        existing_query = parsed_base.query
        new_query = urlencode(params, quote_via=quote)
        tracking_encoded = quote(tracking.strip(), safe="")
        
        if tracking_encoded:
            new_query += "&" + tracking_encoded
        
        if existing_query:
            combined_query = existing_query + "&" + new_query
        else:
            combined_query = new_query
        
        # finale URL bauen
        final_url = urlunparse(parsed_base._replace(query=combined_query))

        st.success("URL erfolgreich generiert ✅")
        st.text_area("Fertige URL", final_url, height=150)

        st.code(final_url)
