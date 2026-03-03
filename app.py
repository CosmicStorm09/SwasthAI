import streamlit as st
import requests
import json
import os

# Constants
BACKEND_URL = "http://localhost:8000/triage"
FACILITIES_FILE = "facilities.json"

# Function to load facilities from JSON file
def load_facilities():
    if os.path.exists(FACILITIES_FILE):
        with open(FACILITIES_FILE, 'r') as f:
            return json.load(f)
    else:
        return []

# Function to send POST request to backend
def get_triage_data(text, lang):
    payload = {"text": text, "lang": lang}
    try:
        response = requests.post(BACKEND_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend: {e}")
        return None

# Main Streamlit app
def main():
    st.title("SwasthAI – Community Health Assistant")
    st.markdown("*Not medical advice. For awareness only.*")

    # Text area for symptoms
    user_input = st.text_area("Describe your symptoms", height=100)

    # Language selectbox
    language = st.selectbox("Language", ["English", "Hindi"])

    # Button to get guidance
    if st.button("Get Guidance"):
        if len(user_input.strip()) < 10:
            st.warning("Please provide at least 10 characters describing your symptoms.")
        else:
            # Send request to backend
            data = get_triage_data(user_input, language)
            if data:
                # Display preliminary guidance
                st.subheader("Preliminary Guidance")
                st.write(data.get("guidance", "No guidance available."))

                # Display red flag alerts
                red_flags = data.get("red_flags", [])
                if red_flags:
                    st.subheader("Red Flag Alerts")
                    for alert in red_flags:
                        st.error(f"⚠️ {alert}")
                else:
                    st.info("No red flag alerts.")

                # Display when to see a doctor
                st.subheader("When to See a Doctor")
                st.write(data.get("when_to_see_doctor", "No advice available."))

                # Display nearby public facilities
                facilities = load_facilities()
                if facilities:
                    st.subheader("Nearby Public Facilities")
                    for facility in facilities:
                        st.write(f"- **{facility.get('name', 'Unknown')}**: {facility.get('address', 'Address not available')}")
                else:
                    st.info("No facilities data available.")

if __name__ == "__main__":
    main()
