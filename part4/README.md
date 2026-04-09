# HBnB — Part 4: Simple Web Client

![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?logo=javascript&logoColor=black)
![Flask API](https://img.shields.io/badge/Flask_API-3.x-lightgrey)
![CORS](https://img.shields.io/badge/CORS-Enabled-green)

---

## 📌 Overview

**HBnB Part 4** is the front-end of the HBnB application.
It interacts with the REST API developed in Part 3 using **AJAX (`fetch`)** and manages authentication via **JWT stored in cookies**.

This project demonstrates how to build a dynamic web interface using **vanilla JavaScript**, without relying on frameworks.

---

## 🌐 Available Pages

| Page | Description |
|------|-------------|
| `index.html` | Home page with hero section, places list, filters, and search |
| `login.html` | User authentication page |
| `place.html` | Displays place details, amenities, and reviews |
| `add_review.html` | Form to submit a review (requires authentication) |
| `add_place.html` | Form to create a new place (requires authentication) |

---

## 📁 Project Structure

```
part4/
├── index.html
├── login.html
├── place.html
├── add_review.html
├── add_place.html
├── styles.css
├── scripts.js
└── images/
    ├── logo.png
    └── icon.png
```

---

## ⚙️ Installation & Setup

### 1. Requirements

- Python 3.10+
- Virtual environment (Part 3)
- `flask-cors`

```bash
pip install -r requirements.txt
```

### 2. Enable CORS (Backend)

In `app/__init__.py`:

```python
from flask_cors import CORS
CORS(app)
```

### 3. Initialize Database (Part 3)

```bash
cd part3/hbnb

rm -f instance/development.db
sqlite3 instance/development.db < schema.sql
sqlite3 instance/development.db < initial_data.sql
```

### 4. Start the API

```bash
cd part3/hbnb
python3 run.py
```

- API: http://127.0.0.1:5000
- Swagger: http://127.0.0.1:5000/api/v1/

### 5. Start the Frontend

```bash
cd part4
python3 -m http.server 8080
```

Open in browser: http://localhost:8080

> ⚠️ Cookies do not work with `file://` — always use a local server.

---

## 🔑 Demo Accounts

All users share the same password: `pass1234`

| Email | Role | Places |
|-------|------|--------|
| admin@hbnb.io | Admin | — |
| sara@test.com | User | place001, place002, place007 |
| marc@test.com | User | place003, place004, place008 |
| lea@test.com | User | place005, place006, place009 |

---

## ⚡ Features

### 🔐 Authentication (`login.html`)

- Sends `POST /api/v1/auth/login`
- Stores JWT in cookies
- Redirects on success
- Displays errors on failure

### 🏠 Home (`index.html`)

- Fetches places from API
- Filters: price, text search
- Updates UI dynamically
- Shows login/logout button

### 📄 Place Details (`place.html`)

- Gets place ID from URL
- Fetches place + reviews
- Displays amenities (emoji) and reviews
- Shows review form if logged in

### ✍️ Add Review (`add_review.html`)

- Requires authentication
- Redirects if not logged in
- Sends `POST /api/v1/reviews/`
- Shows confirmation

### ➕ Add Place (`add_place.html`)

- Requires authentication
- Validates inputs (price, coordinates)
- Sends `POST /api/v1/places/`
- Redirects after creation

---

## 🎨 Design

| Element | Value |
|---------|-------|
| Font | Nunito |
| Primary color | `#F7A92D` |
| Header/Footer | `#1a1a2e` |
| Background | `#f0f0f5` |
| Layout | Cards |
| Images | Unsplash / Picsum |
| Icons | Emoji |

### 🎯 CSS Classes

| Class | Purpose |
|-------|---------|
| `.logo` | Logo |
| `.login-button` | Login button |
| `.place-card` | Place card |
| `.details-button` | Details button |
| `.place-details` | Details section |
| `.place-info` | Info section |
| `.review-card` | Review |
| `#add-review` | Review form |
| `.form` | Form styling |

---

## ⚠️ Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| 401 on login | Bad bcrypt hash | Regenerate |
| CORS error | Missing config | Add `CORS(app)` |
| No data | API not running | Start backend |
| Cookie issue | Using `file://` | Use localhost |
| Token expired | 1h limit | Login again |
| Add Place hidden | Not logged in | Login |

---

## 🧪 Useful Commands

### Reset DB

```bash
cd part3/hbnb

rm -f instance/development.db
sqlite3 instance/development.db < schema.sql
sqlite3 instance/development.db < initial_data.sql

python3 run.py
```

### Inspect DB

```bash
sqlite3 instance/development.db "SELECT email, is_admin FROM users;"
sqlite3 instance/development.db "SELECT title, price FROM places;"
```

### Test API

```bash
curl http://127.0.0.1:5000/api/v1/places/

curl -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"sara@test.com","password":"pass1234"}'
```

---

## 👤 Author

**Sara Rebati** — Holberton School, 2026
