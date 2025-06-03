# RCM Analytics

RCM Analytics is a Django-based web application designed to manage and analyze revenue cycle management (RCM) tasks. It includes features for task tracking, report generation, file uploads, and user management.

---

## 🔧 Features

- 📊 Dashboard with key RCM metrics
- ✅ Task management system
- 📁 Upload and parse Excel reports
- 🔐 User authentication and role management
- 📄 Custom reports and analytics
- 🌐 Web-based interface using Django templates

---

## 📂 Project Structure

rcm_analytics/
├── db.sqlite3
├── manage.py
├── myvenv/ # Virtual environment
├── rcm_analytics/ # Django project settings
├── rcm_app/ # Main application logic
├── staticfiles/ # Static assets
├── templates/ # HTML templates
├── .gitignore
└── README.md


---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/rcm_analytics.git
cd rcm_analytics-main

source myvenv/bin/activate   # macOS/Linux
myvenv\Scripts\activate      # Windows

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver

http://127.0.0.1:8000/
