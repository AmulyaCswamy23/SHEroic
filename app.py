import streamlit as st
from pymongo import MongoClient
import hashlib
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import requests

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["Sheroic"]

st.set_page_config(page_title="SHEroic - Women Empowerment", page_icon="🔴")

# --- Authentication ---
def authenticate_user(username, password):
    user_collection = db["user"]
    user = user_collection.find_one({"username": username})
    if user and hashlib.sha256(password.encode()).hexdigest() == user["password"]:
        return user
    return None

def signup_user(username, password, role):
    user_collection = db["user"]
    if user_collection.find_one({"username": username}):
        return False
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user_collection.insert_one({
        "username": username,
        "password": hashed_password,
        "role": role
    })
    return True

# --- Gynecologist Finder ---
def find_gynecologists(location):
    API_KEY = "AIzaSyCQDm-jvpXkwWZjGi0fY6vDqznYIXOcMjs"
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={API_KEY}"
    response = requests.get(geocode_url)
    results = response.json()

    if response.status_code == 200 and results['status'] == 'OK':
        lat_lng = results['results'][0]['geometry']['location']
        lat, lng = lat_lng['lat'], lat_lng['lng']

        places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=10000&keyword=gynecologist&key={API_KEY}"
        places_response = requests.get(places_url)
        places_results = places_response.json()

        gynecologists = []
        if places_results['status'] == 'OK':
            for place in places_results['results']:
                gynecologists.append({
                    "name": place.get("name", "N/A"),
                    "address": place.get("vicinity", "N/A"),
                    "rating": place.get("rating", "N/A"),
                    "open_now": place.get("opening_hours", {}).get("open_now", "N/A")
                })
        return gynecologists
    else:
        return []

# --- Login / Signup ---
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = authenticate_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.user_role = user["role"]
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password.")

def signup():
    st.title("Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.radio("Select Role", ("woman", "organization"))
    if st.button("Sign Up"):
        success = signup_user(username, password, role)
        if success:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.user_role = role
            st.success("Signed up successfully!")
        else:
            st.error("Username already exists.")

# --- Dashboard Rendering ---
def render_dashboard():
    st.title(f"Welcome, {st.session_state.username}")

    if st.session_state.user_role == "woman":
        st.sidebar.title("Women Features")
        option = st.sidebar.radio("Choose a feature", (
            "Period Tracker", "Safe Routes", "Gynecologist Finder", "Upload Complaint", "Job Recommendations"))

        if option == "Period Tracker":
            st.subheader("Period Tracker")
            st.title("SHEroic - Menstrual Cycle Tracker")

            with st.form("cycle-tracker-form"):
                st.subheader("Menstrual Cycle Tracker")
                start_date = st.date_input("Start Date")
                cycle_length = st.number_input("How long did it last? (in days):", min_value=1)
                usual_cycle_length = st.number_input("Usual Cycle Length (in days):", min_value=1)
                submit_button = st.form_submit_button("Track Cycle")

                if submit_button:
                    current_date = datetime.today().date()
                    days_passed = (current_date - start_date).days
                    upcoming_start_date = start_date + timedelta(days=28)

                    if days_passed < 5:
                        phase = "Menstruation"
                        details = ["Expect bleeding and discomfort."]
                        dos = ["Rest, hydrate, use pain relief."]
                        donts = ["Avoid overexertion."]
                        prev = "Luteal"
                        next_ = "Follicular"
                    elif days_passed < 15:
                        phase = "Follicular"
                        details = ["Hormone levels are rising."]
                        dos = ["Exercise, eat balanced meals."]
                        donts = ["Avoid stress."]
                        prev = "Menstruation"
                        next_ = "Ovulation"
                    elif days_passed < 23:
                        phase = "Ovulation"
                        details = ["Fertile window is open."]
                        dos = ["Have safe sex if desired."]
                        donts = ["Avoid unprotected sex if not ready."]
                        prev = "Follicular"
                        next_ = "Luteal"
                    else:
                        phase = "Luteal"
                        details = ["Hormone levels high."]
                        dos = ["Relax, manage PMS."]
                        donts = ["Avoid caffeine, stress."]
                        prev = "Ovulation"
                        next_ = "Menstruation"

                    st.subheader("Cycle Details")
                    st.write(f"**Menstrual Phase:** {phase}")
                    for d in details: st.write(f"- {d}")
                    st.write("**Do's and Don'ts:**")
                    for d in dos + donts: st.write(f"- {d}")
                    st.write(f"**Previous Stage:** {prev}")
                    st.write(f"**Upcoming Stage:** {next_}")
                    st.write(f"**Previous Start Date:** {start_date.strftime('%Y-%m-%d')}")
                    st.write(f"**Upcoming Start Date:** {upcoming_start_date.strftime('%Y-%m-%d')}")
                    if current_date > upcoming_start_date:
                        st.markdown(f"**Your period is {(current_date - upcoming_start_date).days} days late.**")

        elif option == "Safe Routes":
            st.subheader("Safe Route Finder")
            with st.form("route-form"):
                source = st.text_input("Enter your starting location")
                destination = st.text_input("Enter your destination")
                submit = st.form_submit_button("Get Route")

            if submit and source and destination:
                api_key = "AIzaSyCQDm-jvpXkwWZjGi0fY6vDqznYIXOcMjs"
                map_html = f"""
                <iframe
                    width="100%"
                    height="500"
                    style="border:0"
                    loading="lazy"
                    allowfullscreen
                    src="https://www.google.com/maps/embed/v1/directions?key={api_key}&origin={source}&destination={destination}&mode=walking">
                </iframe>
                """
                st.components.v1.html(map_html, height=550, scrolling=False)
            elif submit:
                st.error("Both start and destination must be filled.")

        elif option == "Gynecologist Finder":
            st.subheader("Gynecologist Finder")
            location = st.text_input('Enter your location:')
            if location:
                gynecologists = find_gynecologists(location)
                if gynecologists:
                    for idx, g in enumerate(gynecologists, 1):
                        st.write(f"**Gynecologist #{idx}:**")
                        st.write(f"- **Name:** {g['name']}")
                        st.write(f"- **Address:** {g['address']}")
                        st.write(f"- **Rating:** {g['rating']}")
                        st.write(f"- **Open Now:** {'Yes' if g['open_now'] else 'No'}")
                        st.write("---")
                else:
                    st.write("No gynecologists found near the entered location.")
        elif option == "Upload Complaint":
            st.subheader("Upload Complaint")
            caption = st.text_input("Complaint Title")
            description = st.text_area("Describe your issue")
            uploaded_file = st.file_uploader("Attach a file (optional)", type=["jpg", "jpeg", "png", "mp4", "mp3", "pdf"])

            if st.button("Submit Complaint"):
                if caption and description:
                    complaint_doc = {
                        "username": st.session_state.username,
                        "caption": caption,
                        "description": description,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

                    if uploaded_file:
                        file_data = uploaded_file.read()
                        complaint_doc["file"] = file_data
                        complaint_doc["filename"] = uploaded_file.name
                        complaint_doc["filetype"] = uploaded_file.type

                    db["complaints"].insert_one(complaint_doc)
                    st.success("Complaint submitted successfully.")
                else:
                    st.error("Both caption and description are required.")

        elif option == "Job Recommendations":
            st.subheader("Job Recommendations")
            st.info("Feature under development.")

    elif st.session_state.user_role == "organization":
        st.sidebar.title("Organization Features")
        option = st.sidebar.radio("Choose a feature", ("View Complaints",))

        if option == "View Complaints":
            st.subheader("Complaints Feed")
            complaints = list(db["complaints"].find().sort("timestamp", -1))

            if complaints:
                for c in complaints:
                    st.markdown(f"**{c['username']}** reported:")
                    st.write(f"📌 {c['caption']}")
                    st.write(c["description"])
                    st.caption(c["timestamp"])

                    if "file" in c and "filetype" in c:
                        if c["filetype"].startswith("image"):
                            st.image(c["file"], caption=c.get("filename", "Attached Image"))
                        else:
                            b64 = base64.b64encode(c["file"]).decode()
                            href = f'<a href="data:{c["filetype"]};base64,{b64}" download="{c.get("filename", "file")}">📎 Download {c["filename"]}</a>'
                            st.markdown(href, unsafe_allow_html=True)

                    st.divider()
            else:
                st.info("No complaints found.")

# --- Main ---
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user_role" not in st.session_state:
        st.session_state.user_role = None
    if "username" not in st.session_state:
        st.session_state.username = ""

    if not st.session_state.logged_in:
        option = st.selectbox("Choose an option", ("Login", "Sign Up"))
        if option == "Login":
            login()
        else:
            signup()
    else:
        render_dashboard()

if __name__ == "__main__":
    main()
