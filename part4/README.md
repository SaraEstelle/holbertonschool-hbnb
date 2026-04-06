# HBnB — Part 4 : Simple Web Client

![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?logo=javascript&logoColor=black)
![Flask](https://img.shields.io/badge/Flask_API-3.x-lightgrey)
![CORS](https://img.shields.io/badge/CORS-Enabled-green)

## Présentation

La Part 4 est l'interface web (front-end) de l'application HBnB.
Elle interagit avec l'API REST de la Part 3 via `fetch()` (AJAX) et gère l'authentification JWT côté client via des cookies.

### Ce que fait l'application

| Page | Description |
|---|---|
| `index.html` | Section héro commerciale + liste des places + filtre prix + recherche textuelle |
| `login.html` | Formulaire de connexion → stocke le JWT en cookie |
| `place.html` | Détails d'une place avec photo, amenities, reviews + formulaire d'avis |
| `add_review.html` | Formulaire de review standalone (accès auth uniquement) |

---

## Architecture

```
part4/
├── index.html          ← Page d'accueil : héro + liste places + filtres
├── login.html          ← Formulaire de connexion JWT
├── place.html          ← Détails place + reviews + ajouter review
├── add_review.html     ← Formulaire review standalone
├── styles.css          ← Design complet (palette orange/dark, Nunito)
├── scripts.js          ← Toute la logique JS (Tasks 1-4)
├── seed_demo.sql       ← 6 places + 3 users + reviews pour la démo
├── requirements.txt    ← Dépendances Python (avec flask-cors)
└── images/
    ├── logo.png        ← Logo HBnB
    └── icon.png        ← Favicon
```

---

## Installation et démarrage

### 1. Prérequis

- Python 3.10+ avec l'environnement virtuel de la Part 3 actif
- `flask-cors` installé : `pip install flask-cors`

```bash
pip install -r requirements.txt
```

### 2. Vérifier que CORS est activé dans l'API

Le fichier `app/__init__.py` doit contenir :

```python
from flask_cors import CORS
# ...
CORS(app)
```

> ✅ CORS est déjà intégré dans la version finale fournie.

### 3. Initialiser la base de données

```bash
cd hbnb

# Créer la structure
sqlite3 instance/development.db < schema.sql

# Insérer l'admin et les 3 amenities de base
sqlite3 instance/development.db < initial_data.sql

# (Optionnel) Données de démonstration : 6 places + users + reviews
sqlite3 instance/development.db < seed_demo.sql
```

### 4. Démarrer l'API Flask (Part 3)

```bash
cd hbnb
python3 run.py
```

L'API tourne sur : `http://127.0.0.1:5000`
Swagger UI : `http://127.0.0.1:5000/api/v1/`

### 5. Ouvrir l'interface web

Ouvrir les fichiers HTML directement dans le navigateur **ou** via un serveur HTTP local :

```bash
# Option A — Python simple server
cd part4
python3 -m http.server 8080
# → http://localhost:8080/index.html

# Option B — Node.js live-server (si installé)
npx live-server --port=8080

# Option C — Ouvrir directement dans le navigateur
# Glisser-déposer index.html dans Firefox / Chrome
# ⚠️ Certains navigateurs bloquent les cookies sur file:// → utiliser un serveur
```

---

## Comptes de démo (après seed_demo.sql)

| Email | Mot de passe | Rôle |
|---|---|---|
| `admin@hbnb.io` | `admin1234` | Admin |
| `sara@test.com` | `pass1234` | Propriétaire place001, place002 |
| `marc@test.com` | `pass1234` | Propriétaire place003, place004 |
| `lea@test.com` | `pass1234` | Propriétaire place005, place006 |

---

## Fonctionnalités JavaScript (Tasks)

### Task 1 — Login (`login.html`)

- Écoute la soumission du formulaire `#login-form`
- `POST /api/v1/auth/login` avec `{ email, password }`
- Succès : stocke le token JWT en cookie (`token=...; path=/`)
- Succès : redirige vers `index.html`
- Échec : affiche `#login-error`

### Task 2 — Index (`index.html`)

- Charge les places via `GET /api/v1/places/`
- Filtre par prix côté client (sans re-fetch) : `All / $10 / $50 / $100`
- Filtre par texte sur le titre (recherche instantanée)
- Affiche `Login` ou `Logout` selon la présence du cookie
- Chaque carte affiche une photo (picsum.photos ou Unsplash)

### Task 3 — Place Details (`place.html`)

- Extrait `?id=<uuid>` de l'URL
- Deux fetches en parallèle : détails place + reviews
- Affiche photo, host, prix, description, amenities avec icônes emoji
- Affiche les reviews ou "Be the first!"
- Montre/cache `#add-review` selon l'authentification

### Task 4 — Add Review (`add_review.html` + inline dans `place.html`)

- Redirige vers `index.html` si non authentifié
- `POST /api/v1/reviews/` avec `{ text, rating, place_id }`
- Toast de confirmation + redirection après soumission

---

## Design

| Élément | Valeur |
|---|---|
| Police | Nunito (Google Fonts) |
| Couleur principale | `#F7A92D` (orange) |
| Couleur fond | `#1a1a2e` (dark) pour header/footer |
| Couleur page | `#f0f0f5` (gris clair) |
| Cartes | border: 1px solid #ddd, border-radius: 10px, margin: 20px, padding: 10px |
| Bouton | Gradient orange → orange-dark |
| Photos places | Unsplash (6 places seed) + picsum.photos (fallback) |
| Icônes amenities | Emoji mappés par nom |

### Classes CSS obligatoires (conformité task 0)

| Classe | Élément |
|---|---|
| `.logo` | Image du logo dans le header |
| `.login-button` | Bouton Login dans le header |
| `.place-card` | Carte de place dans la liste |
| `.details-button` | Bouton "View Details" sur la carte |
| `.place-details` | Section details de la page place |
| `.place-info` | Div des infos détaillées (host, prix...) |
| `.review-card` | Carte de review |
| `.add-review` | Section du formulaire d'avis |
| `.form` | Formulaire de review dans `#add-review` |

---

## Tests

### Vérifier le CORS (depuis le front-end)

Ouvrir la console du navigateur et tester :

```javascript
fetch('http://127.0.0.1:5000/api/v1/places/')
  .then(r => r.json())
  .then(d => console.log('Places:', d.length))
  .catch(e => console.error('CORS error:', e));
```

### Tester le login

```bash
curl -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"sara@test.com","password":"pass1234"}'
```

### Tester les places

```bash
curl http://127.0.0.1:5000/api/v1/places/
```

---

## Résolution des problèmes courants

| Problème | Solution |
|---|---|
| `CORS error` dans la console | Vérifier que `CORS(app)` est dans `app/__init__.py` |
| Places ne chargent pas | Lancer l'API avec `python3 run.py` |
| `401 Unauthorized` | Se connecter via `login.html` |
| Cookie non stocké | Utiliser `http://localhost:8080` (pas `file://`) |
| Token expiré (401) | Se reconnecter : le token dure 1h en dev |
| Base de données vide | Exécuter `seed_demo.sql` |
| Images ne s'affichent pas | Connexion Internet requise (Unsplash/picsum) |

---

## Auteurs

- **Sara Rebati**

Holberton School — 2026