import streamlit as st
from urllib.parse import urlencode, urlparse, urlunparse, quote
from datetime import datetime, date, time
import json
import os

# ---------------------------------
# Basis-Links
# ---------------------------------
basis_links = {
    "Ulla Popken DE": "https://www.ullapopken.de/de",
    "Happy Size DE": "https://www.happy-size.de/de",
    "JP1880 DE": "https://www.jp1880.de/de",
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
        final_url = urlunparse(parsed_base._replace(query=query))

        st.success("URL erfolgreich generiert ✅")
        st.text_area("Fertige URL", final_url, height=150)

        st.code(final_url)
