# SHEroic 💪💖

SHEroic is a women-centric safety and empowerment platform built with Streamlit. It includes tools for menstrual health tracking, safe route planning, gynecologist finding, job recommendations, complaint submission, and organizational support.

## 🔥 Features

👩 For Women:
- 🩸 **Period Tracker**: Track menstrual cycle and get phase-specific health guidance.
- 🚶‍♀️ **Safe Routes**: Plan safe walking routes with Google Maps & POI data (hospitals, police stations).
- 🧑‍⚕️ **Gynecologist Finder**: Locate nearby gynecologists using Google Places API.
- 📣 **Complaint Upload**: Submit complaints with optional file/photo attachment.
- 💼 **Job Recommendations** *(in progress)*: Personalized suggestions based on skills, degree, and location.

🏢 For Organizations:
- 🧾 **View Complaints**: Access and respond to public complaints submitted by users.
- 💬 **Respond to Users** : Have a 1-1 chat with them about the complaints

---

## 🛠️ Tech Stack

- **Frontend & Logic**: [Streamlit](https://streamlit.io/)
- **Database**: MongoDB (via `pymongo`)
- **Geolocation/Maps**: Google Maps JavaScript API & Google Places API
- **Authentication**: Custom login/signup
- **File Uploads**: Handled via MongoDB GridFS *(optional)*

---

## 📦 Setup Instructions

1. Clone the repo
```bash
git clone https://github.com/AmulyaCswamy23/SHEroic.git
cd SHEroic
2.Install the dependencies
pip install -r requirements.txt
3.Run the app
streamlit run app.py
Note:
I have just given the templates, incase you want to use them and build a website.
They have no use in this project but i have used them as reference to build streamlit app.

