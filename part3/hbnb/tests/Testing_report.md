# HBnB API — Rapport de Tests Manuels (Swagger UI)
_Date : Juin 2025_
_Base URL : `http://127.0.0.1:5000`_
_Swagger UI : `http://127.0.0.1:5000/api/v1/`_
_Auteurs : Sara Rebati · Valentin Planchon · Damien Rossi — Holberton School_

> Ce rapport documente **tous les tests effectués manuellement** via le Swagger UI, couvrant chaque endpoint de l'API HBnB.
> Les cas **valides**, **invalides** et **cas limites** sont documentés avec les corps de requête exacts, les réponses et les codes de statut.
> La version finale inclut les endpoints DELETE pour toutes les entités (users, places, amenities, reviews) et le RBAC complet.

---

## Table des matières

- [Configuration / Accès](#configuration--accès)
- [AUTH](#auth----apiv1authlogin)
- [USERS](#users----apiv1users)
- [AMENITIES](#amenities----apiv1amenities)
- [PLACES](#places----apiv1places)
- [REVIEWS](#reviews----apiv1reviews)
- [DELETE — Users, Places, Amenities](#delete--users-places-amenities)
- [Tableau récapitulatif](#tableau-récapitulatif)

---

## Configuration / Accès

### TEST S0 — URL racine
- **Méthode/Endpoint :** `GET /`
- **Statut :** `404 Not Found`
- **Notes :** Normal — aucune route sur `/`. Le Swagger est sur `/api/v1/`.

### TEST S1 — Swagger UI
- **Méthode/Endpoint :** `GET /api/v1/`
- **Statut :** `200 OK`
- **Notes :** Le Swagger UI se charge correctement avec 5 namespaces : `auth`, `users`, `amenities`, `places`, `reviews`.

### TEST S2 — Connexion admin et récupération du token
- **Méthode/Endpoint :** `POST /api/v1/auth/login`
- **Corps de la requête :**
```json
{ "email": "admin@hbnb.io", "password": "admin1234" }
```
- **Statut :** `200 OK`
- **Corps de la réponse :**
```json
{ "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." }
```
- **Notes :** Copier le token et l'utiliser dans le bouton **Authorize** → `Bearer <token>`.

---

## AUTH — `POST /api/v1/auth/login`

### TEST AUTH1 — Login valide (admin)
- **Méthode/Endpoint :** `POST /api/v1/auth/login`
- **Corps :**
```json
{ "email": "admin@hbnb.io", "password": "admin1234" }
```
- **Statut :** `200 OK`
- **Réponse :**
```json
{ "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." }
```
- **Notes :** Le token contient `sub` (user_id) et `is_admin: true` dans le payload JWT.

### TEST AUTH2 — Login mauvais mot de passe
- **Corps :**
```json
{ "email": "admin@hbnb.io", "password": "mauvais_mdp" }
```
- **Statut :** `401 Unauthorized`
- **Réponse :**
```json
{ "error": "Invalid credentials" }
```

### TEST AUTH3 — Login email inexistant
- **Corps :**
```json
{ "email": "fantome@test.com", "password": "admin1234" }
```
- **Statut :** `401 Unauthorized`
- **Réponse :**
```json
{ "error": "Invalid credentials" }
```

### TEST AUTH4 — Accès endpoint protégé sans token
Désactiver le token dans Authorize (Logout), puis :
- **Méthode/Endpoint :** `POST /api/v1/users/`
- **Statut :** `401 Unauthorized`
- **Réponse :**
```json
{ "msg": "Missing Authorization Header" }
```

---

## USERS — `/api/v1/users/`

### Données de test connues

| Alias | first_name | last_name | email |
|---|---|---|---|
| User A (John) | John | Doe | john.doe@example.com |
| User B (Jane) | Jane | Smith | jane.smith@example.com |

---

## ✅ USERS — Cas valides

### TEST U1 — Créer un user valide (admin requis)
- **Méthode/Endpoint :** `POST /api/v1/users/`
- **Token :** Admin Bearer token
- **Corps :**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "password": "secret12"
}
```
- **Statut :** `201 Created`
- **Réponse :**
```json
{
  "id": "a1b2c3d4-0001-0001-0001-000000000001",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}
```
- **Notes :** Le mot de passe n'est **jamais** renvoyé. Il est stocké en hash bcrypt `$2b$12$...`.

### TEST U2 — Créer un deuxième user
- **Statut :** `201 Created`
- **Notes :** Sauvegarder les deux IDs pour les tests suivants.

### TEST U3 — Lister tous les users
- **Méthode/Endpoint :** `GET /api/v1/users/`
- **Token :** non requis (public)
- **Statut :** `200 OK`
- **Réponse :**
```json
[
  { "id": "...", "first_name": "Admin", "last_name": "HBnB", "email": "admin@hbnb.io" },
  { "id": "...", "first_name": "John", "last_name": "Doe", "email": "john.doe@example.com" },
  { "id": "...", "first_name": "Jane", "last_name": "Smith", "email": "jane.smith@example.com" }
]
```

### TEST U4 — Lire un user par ID
- **Méthode/Endpoint :** `GET /api/v1/users/{id}`
- **Statut :** `200 OK`

### TEST U5 — Modifier son propre profil (user normal)
- **Méthode/Endpoint :** `PUT /api/v1/users/{john_id}`
- **Token :** Token de John
- **Corps :**
```json
{ "first_name": "Johnny", "last_name": "Doe" }
```
- **Statut :** `200 OK`
- **Notes :** Un user standard ne peut modifier que `first_name` et `last_name`.

### TEST U6 — Admin modifie n'importe quel user (bypass)
- **Méthode/Endpoint :** `PUT /api/v1/users/{john_id}`
- **Token :** Admin Bearer token
- **Corps :**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.new@example.com",
  "password": "newpass123"
}
```
- **Statut :** `200 OK`
- **Notes :** L'admin peut aussi modifier email et password.

### TEST U7 — DELETE user par admin
- **Méthode/Endpoint :** `DELETE /api/v1/users/{jane_id}`
- **Token :** Admin Bearer token
- **Statut :** `200 OK`
- **Réponse :**
```json
{ "message": "User successfully deleted" }
```
- **Notes :** CASCADE — les places et reviews de Jane sont supprimées automatiquement.

---

## ❌ USERS — Cas invalides

### TEST U8 — Créer user sans token
- **Statut :** `401 Unauthorized`

### TEST U9 — Créer user avec token non-admin
- **Token :** Token de John
- **Statut :** `403 Forbidden`
- **Réponse :** `{"error": "Admin privileges required"}`

### TEST U10 — Format email invalide
- **Corps :** `{ ..., "email": "pas_un_email" }`
- **Statut :** `400 Bad Request`
- **Réponse :** `{"error": "Invalid email format"}`

### TEST U11 — Prénom vide
- **Corps :** `{ "first_name": "", ... }`
- **Statut :** `400 Bad Request`

### TEST U12 — Prénom > 50 caractères
- **Statut :** `400 Bad Request`

### TEST U13 — Mot de passe < 6 caractères
- **Corps :** `{ ..., "password": "abc" }`
- **Statut :** `400 Bad Request`

### TEST U14 — Email dupliqué
- **Statut :** `422 Unprocessable Entity`
- **Réponse :** `{"error": "Email already exists"}`

### TEST U15 — User inexistant (GET)
- **Méthode/Endpoint :** `GET /api/v1/users/00000000-0000-0000-0000-000000000000`
- **Statut :** `404 Not Found`
- **Réponse :** `{"error": "User not found"}`

### TEST U16 — Modifier le profil d'un autre (non admin)
- **Méthode/Endpoint :** `PUT /api/v1/users/{jane_id}`
- **Token :** Token de John
- **Statut :** `403 Forbidden`
- **Réponse :** `{"error": "Unauthorized action"}`

### TEST U17 — Modifier email (user normal interdit)
- **Corps :** `{ "email": "newemail@test.com" }`
- **Token :** Token de John sur son propre ID
- **Statut :** `400 Bad Request`
- **Réponse :** `{"error": "You cannot modify email or password"}`

### TEST U18 — DELETE user non-admin
- **Méthode/Endpoint :** `DELETE /api/v1/users/{jane_id}`
- **Token :** Token de John
- **Statut :** `403 Forbidden`
- **Réponse :** `{"error": "Admin privileges required"}`

### TEST U19 — Admin se supprime lui-même
- **Méthode/Endpoint :** `DELETE /api/v1/users/{admin_id}`
- **Token :** Admin Bearer token
- **Statut :** `400 Bad Request`
- **Réponse :** `{"error": "Cannot delete your own admin account"}`

### TEST U20 — DELETE user inexistant
- **Méthode/Endpoint :** `DELETE /api/v1/users/00000000-0000-0000-0000-000000000000`
- **Token :** Admin Bearer token
- **Statut :** `404 Not Found`
- **Réponse :** `{"error": "User not found"}`

---

## AMENITIES — `/api/v1/amenities/`

### IDs amenities initiales (initial_data.sql)

| Nom | UUID |
|---|---|
| WiFi | `7c9fdf4d-99be-4b1c-8c2e-5aea5db0d0eb` |
| Swimming Pool | `ae5ae8a5-0203-451b-9cb8-6086e5b2f41e` |
| Air Conditioning | `97bc1cc5-3dcd-439e-894f-e9986dedd012` |

---

## ✅ AMENITIES — Cas valides

### TEST A1 — Créer une amenity (admin)
- **Méthode/Endpoint :** `POST /api/v1/amenities/`
- **Token :** Admin Bearer token
- **Corps :**
```json
{ "name": "Jacuzzi", "description": "Jacuzzi privé de luxe" }
```
- **Statut :** `201 Created`
- **Réponse :**
```json
{
  "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "name": "Jacuzzi",
  "description": "Jacuzzi privé de luxe"
}
```

### TEST A2 — Lister toutes les amenities
- **Méthode/Endpoint :** `GET /api/v1/amenities/`
- **Token :** non requis (public)
- **Statut :** `200 OK`
- **Notes :** Doit retourner au minimum les 3 amenities initiales + celles créées.

### TEST A3 — Lire amenity par ID
- **Méthode/Endpoint :** `GET /api/v1/amenities/{id}`
- **Statut :** `200 OK`

### TEST A4 — Modifier amenity (admin)
- **Méthode/Endpoint :** `PUT /api/v1/amenities/{jacuzzi_id}`
- **Token :** Admin Bearer token
- **Corps :**
```json
{ "name": "Jacuzzi VIP", "description": "Jacuzzi privé avec jets massants" }
```
- **Statut :** `200 OK`
- **Réponse :** `{"message": "Amenity updated successfully"}`

### TEST A5 — DELETE amenity par admin
- **Méthode/Endpoint :** `DELETE /api/v1/amenities/{jacuzzi_id}`
- **Token :** Admin Bearer token
- **Statut :** `200 OK`
- **Réponse :** `{"message": "Amenity deleted successfully"}`
- **Notes :** CASCADE — les liens `place_amenity` de cette amenity sont supprimés. Les places elles-mêmes restent intactes.

---

## ❌ AMENITIES — Cas invalides

### TEST A6 — Créer amenity sans token
- **Statut :** `401 Unauthorized`

### TEST A7 — Créer amenity avec token non-admin
- **Token :** Token de John
- **Statut :** `403 Forbidden`
- **Réponse :** `{"error": "Admin privileges required"}`

### TEST A8 — Nom vide
- **Corps :** `{ "name": "" }`
- **Statut :** `400 Bad Request`

### TEST A9 — Nom > 50 caractères
- **Statut :** `400 Bad Request`

### TEST A10 — Amenity inexistante (GET)
- **Statut :** `404 Not Found`
- **Réponse :** `{"error": "Amenity not found"}`

### TEST A11 — Modifier amenity sans être admin
- **Token :** Token de John
- **Statut :** `403 Forbidden`

### TEST A12 — DELETE amenity sans token
- **Statut :** `401 Unauthorized`

### TEST A13 — DELETE amenity non-admin
- **Token :** Token de John
- **Statut :** `403 Forbidden`
- **Réponse :** `{"error": "Admin privileges required"}`

### TEST A14 — DELETE amenity inexistante
- **Méthode/Endpoint :** `DELETE /api/v1/amenities/00000000-0000-0000-0000-000000000000`
- **Token :** Admin Bearer token
- **Statut :** `404 Not Found`
- **Réponse :** `{"error": "Amenity not found"}`

---

## PLACES — `/api/v1/places/`

---

## ✅ PLACES — Cas valides

### TEST P1 — Créer un logement (authentifié)
- **Méthode/Endpoint :** `POST /api/v1/places/`
- **Token :** Token de John
- **Corps :**
```json
{
  "title": "Appartement Paris",
  "description": "Bel appartement près de la Tour Eiffel",
  "price": 120.00,
  "latitude": 48.8566,
  "longitude": 2.3522,
  "amenities": ["7c9fdf4d-99be-4b1c-8c2e-5aea5db0d0eb"]
}
```
- **Statut :** `201 Created`
- **Réponse :**
```json
{
  "id": "72486b52-...",
  "title": "Appartement Paris",
  "description": "Bel appartement près de la Tour Eiffel",
  "price": 120.0,
  "latitude": 48.8566,
  "longitude": 2.3522,
  "owner_id": "<john_id>"
}
```
- **Notes :** `owner_id` est extrait du JWT — le champ éventuel dans le body est ignoré.

### TEST P2 — Lister toutes les places
- **Méthode/Endpoint :** `GET /api/v1/places/`
- **Token :** non requis (public)
- **Statut :** `200 OK`
- **Notes :** Vue réduite — uniquement `id`, `title`, `latitude`, `longitude`.

### TEST P3 — Obtenir une place par ID (vue complète)
- **Méthode/Endpoint :** `GET /api/v1/places/{place_id}`
- **Statut :** `200 OK`
- **Réponse :**
```json
{
  "id": "72486b52-...",
  "title": "Appartement Paris",
  "description": "Bel appartement près de la Tour Eiffel",
  "price": 120.0,
  "latitude": 48.8566,
  "longitude": 2.3522,
  "owner": {
    "id": "<john_id>",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
  },
  "amenities": [
    { "id": "7c9fdf4d-...", "name": "WiFi" }
  ]
}
```

### TEST P4 — Modifier sa propre place (propriétaire)
- **Méthode/Endpoint :** `PUT /api/v1/places/{place_id}`
- **Token :** Token de John
- **Corps :**
```json
{ "title": "Appartement Paris Rénové", "price": 150.00 }
```
- **Statut :** `200 OK`
- **Réponse :** `{"message": "Place updated successfully"}`

### TEST P5 — Admin modifie la place d'un autre (bypass)
- **Méthode/Endpoint :** `PUT /api/v1/places/{place_id}`
- **Token :** Admin Bearer token
- **Corps :**
```json
{ "title": "Modifié par Admin", "price": 200.00 }
```
- **Statut :** `200 OK`

### TEST P6 — DELETE place par le propriétaire
- **Méthode/Endpoint :** `DELETE /api/v1/places/{place_id}`
- **Token :** Token de John (propriétaire)
- **Statut :** `200 OK`
- **Réponse :** `{"message": "Place deleted successfully"}`
- **Notes :** CASCADE — les reviews de cette place et les liens `place_amenity` sont supprimés automatiquement. Les amenities restent intactes.

### TEST P7 — Admin supprime la place d'un autre (bypass)
- **Méthode/Endpoint :** `DELETE /api/v1/places/{place_id}`
- **Token :** Admin Bearer token
- **Statut :** `200 OK`

### TEST P8 — Lister les reviews d'une place
- **Méthode/Endpoint :** `GET /api/v1/places/{place_id}/reviews`
- **Token :** non requis (public)
- **Statut :** `200 OK`
- **Réponse :**
```json
[
  {
    "id": "cccc0001-...",
    "text": "Super endroit !",
    "rating": 5,
    "user_id": "<jane_id>",
    "place_id": "<place_id>"
  }
]
```

---

## ❌ PLACES — Cas invalides

### TEST P9 — Créer place sans token
- **Statut :** `401 Unauthorized`

### TEST P10 — Prix négatif
- **Corps :** `{ ..., "price": -50.00 }`
- **Statut :** `400 Bad Request`
- **Réponse :** `{"error": "price must be greater than 0"}`

### TEST P11 — Latitude hors limites
- **Corps :** `{ ..., "latitude": 999.0 }`
- **Statut :** `400 Bad Request`
- **Réponse :** `{"error": "latitude must be between -90 and 90"}`

### TEST P12 — Longitude hors limites
- **Corps :** `{ ..., "longitude": 999.0 }`
- **Statut :** `400 Bad Request`

### TEST P13 — Titre vide
- **Corps :** `{ "title": "", ... }`
- **Statut :** `400 Bad Request`

### TEST P14 — Place inexistante (GET)
- **Statut :** `404 Not Found`
- **Réponse :** `{"error": "Place not found"}`

### TEST P15 — Modifier la place d'un autre (non admin)
- **Token :** Token de Jane
- **Statut :** `403 Forbidden`
- **Réponse :** `{"error": "Unauthorized action"}`

### TEST P16 — DELETE place sans token
- **Statut :** `401 Unauthorized`

### TEST P17 — DELETE place non-propriétaire non-admin
- **Token :** Token de Jane (non propriétaire)
- **Statut :** `403 Forbidden`
- **Réponse :** `{"error": "Unauthorized action"}`

### TEST P18 — DELETE place inexistante
- **Méthode/Endpoint :** `DELETE /api/v1/places/00000000-0000-0000-0000-000000000000`
- **Token :** Admin Bearer token
- **Statut :** `404 Not Found`
- **Réponse :** `{"error": "Place not found"}`

### TEST P19 — Reviews pour place inexistante
- **Méthode/Endpoint :** `GET /api/v1/places/00000000-0000-0000-0000-000000000000/reviews`
- **Statut :** `404 Not Found`

---

## REVIEWS — `/api/v1/reviews/`

---

## ✅ REVIEWS — Cas valides

### TEST R1 — Créer une review valide (Jane sur place de John)
- **Méthode/Endpoint :** `POST /api/v1/reviews/`
- **Token :** Token de Jane
- **Corps :**
```json
{
  "text": "Superbe endroit, très bien situé !",
  "rating": 5,
  "place_id": "<place_id>"
}
```
- **Statut :** `201 Created`
- **Réponse :**
```json
{
  "id": "cccc0001-...",
  "text": "Superbe endroit, très bien situé !",
  "rating": 5,
  "user_id": "<jane_id>",
  "place_id": "<place_id>"
}
```
- **Notes :** `user_id` est extrait du JWT — jamais du body.

### TEST R2 — Lire toutes les reviews
- **Méthode/Endpoint :** `GET /api/v1/reviews/`
- **Token :** non requis (public)
- **Statut :** `200 OK`

### TEST R3 — Lire review par ID
- **Méthode/Endpoint :** `GET /api/v1/reviews/{review_id}`
- **Statut :** `200 OK`

### TEST R4 — Modifier sa propre review
- **Méthode/Endpoint :** `PUT /api/v1/reviews/{review_id}`
- **Token :** Token de Jane
- **Corps :**
```json
{ "text": "Encore mieux que prévu !", "rating": 5 }
```
- **Statut :** `200 OK`

### TEST R5 — Admin modifie la review d'un autre (bypass)
- **Méthode/Endpoint :** `PUT /api/v1/reviews/{review_id}`
- **Token :** Admin Bearer token
- **Statut :** `200 OK`

### TEST R6 — DELETE review par l'auteur
- **Méthode/Endpoint :** `DELETE /api/v1/reviews/{review_id}`
- **Token :** Token de Jane
- **Statut :** `200 OK`
- **Réponse :** `{"message": "Review deleted successfully"}`

### TEST R7 — Admin supprime la review d'un autre (bypass)
- **Méthode/Endpoint :** `DELETE /api/v1/reviews/{review_id}`
- **Token :** Admin Bearer token
- **Statut :** `200 OK`

### TEST R8 — GET review après DELETE
- **Statut :** `404 Not Found`
- **Notes :** Vérifie que la suppression est effective.

---

## ❌ REVIEWS — Cas invalides

### TEST R9 — Créer review sans token
- **Statut :** `401 Unauthorized`

### TEST R10 — Review sur sa propre place
- **Token :** Token de John (propriétaire de la place)
- **Statut :** `400 Bad Request`
- **Réponse :** `{"error": "You cannot review your own place"}`

### TEST R11 — Review dupliquée (même user + même place)
- **Statut :** `400 Bad Request`
- **Réponse :** `{"error": "You have already reviewed this place"}`

### TEST R12 — Rating > 5
- **Corps :** `{ ..., "rating": 10 }`
- **Statut :** `400 Bad Request`
- **Réponse :** `{"error": "Rating must be between 1 and 5"}`

### TEST R13 — Rating < 1
- **Corps :** `{ ..., "rating": 0 }`
- **Statut :** `400 Bad Request`

### TEST R14 — Texte vide
- **Corps :** `{ "text": "", ... }`
- **Statut :** `400 Bad Request`
- **Réponse :** `{"error": "Text cannot be empty"}`

### TEST R15 — Place inexistante
- **Corps :** `{ ..., "place_id": "00000000-0000-0000-0000-000000000000" }`
- **Statut :** `404 Not Found`
- **Réponse :** `{"error": "Place not found"}`

### TEST R16 — Review inexistante (GET)
- **Statut :** `404 Not Found`

### TEST R17 — Modifier review d'un autre (non admin)
- **Token :** Token de John
- **Statut :** `403 Forbidden`
- **Réponse :** `{"error": "Unauthorized action"}`

### TEST R18 — DELETE review d'un autre (non admin)
- **Token :** Token de John
- **Statut :** `403 Forbidden`

### TEST R19 — DELETE review inexistante
- **Méthode/Endpoint :** `DELETE /api/v1/reviews/00000000-0000-0000-0000-000000000000`
- **Token :** Admin Bearer token
- **Statut :** `404 Not Found`
- **Réponse :** `{"error": "Review not found"}`

---

## DELETE — Users, Places, Amenities

> Cette section documente les nouveaux endpoints DELETE ajoutés dans la version finale.

### TEST D1 — Admin supprime un user
- **Méthode/Endpoint :** `DELETE /api/v1/users/{temp_user_id}`
- **Token :** Admin Bearer token
- **Statut :** `200 OK`
- **Réponse :** `{"message": "User successfully deleted"}`
- **Effet CASCADE :** Places + reviews de cet utilisateur supprimées automatiquement.

### TEST D2 — User non-admin tente de supprimer un user
- **Méthode/Endpoint :** `DELETE /api/v1/users/{jane_id}`
- **Token :** Token de John
- **Statut :** `403 Forbidden`
- **Réponse :** `{"error": "Admin privileges required"}`

### TEST D3 — Admin se supprime lui-même (protégé)
- **Méthode/Endpoint :** `DELETE /api/v1/users/{admin_id}`
- **Token :** Admin Bearer token
- **Statut :** `400 Bad Request`
- **Réponse :** `{"error": "Cannot delete your own admin account"}`
- **Notes :** Règle métier importante — l'admin ne peut pas supprimer son propre compte via l'API.

### TEST D4 — DELETE user inexistant
- **Méthode/Endpoint :** `DELETE /api/v1/users/00000000-0000-0000-0000-000000000000`
- **Token :** Admin Bearer token
- **Statut :** `404 Not Found`
- **Réponse :** `{"error": "User not found"}`

### TEST D5 — Propriétaire supprime sa place
- **Méthode/Endpoint :** `DELETE /api/v1/places/{place_id}`
- **Token :** Token du propriétaire
- **Statut :** `200 OK`
- **Réponse :** `{"message": "Place deleted successfully"}`
- **Effet CASCADE :**
  - Reviews de la place → supprimées automatiquement
  - Liens `place_amenity` → supprimés automatiquement
  - Les amenities elles-mêmes → **non affectées**

### TEST D6 — Non-propriétaire supprime une place
- **Token :** Token de Jane (non propriétaire)
- **Statut :** `403 Forbidden`
- **Réponse :** `{"error": "Unauthorized action"}`

### TEST D7 — Admin supprime la place d'un autre (bypass)
- **Token :** Admin Bearer token
- **Statut :** `200 OK`

### TEST D8 — DELETE place inexistante
- **Méthode/Endpoint :** `DELETE /api/v1/places/00000000-0000-0000-0000-000000000000`
- **Token :** Admin Bearer token
- **Statut :** `404 Not Found`
- **Réponse :** `{"error": "Place not found"}`

### TEST D9 — Admin supprime une amenity
- **Méthode/Endpoint :** `DELETE /api/v1/amenities/{amenity_id}`
- **Token :** Admin Bearer token
- **Statut :** `200 OK`
- **Réponse :** `{"message": "Amenity deleted successfully"}`
- **Effet CASCADE :** Liens `place_amenity` → supprimés. Places → **non affectées**.

### TEST D10 — User non-admin supprime une amenity
- **Token :** Token de John
- **Statut :** `403 Forbidden`
- **Réponse :** `{"error": "Admin privileges required"}`

### TEST D11 — DELETE amenity inexistante
- **Méthode/Endpoint :** `DELETE /api/v1/amenities/00000000-0000-0000-0000-000000000000`
- **Token :** Admin Bearer token
- **Statut :** `404 Not Found`
- **Réponse :** `{"error": "Amenity not found"}`

---

## Tableau récapitulatif

| # | Entité | Méthode | Endpoint | Scénario | Attendu | Résultat |
|---|---|---|---|---|---|---|
| S0 | — | GET | `/` | URL racine | 404 | ✅ |
| S1 | — | GET | `/api/v1/` | Swagger UI | 200 | ✅ |
| S2 | — | POST | `/api/v1/auth/login` | Login admin | 200 + token | ✅ |
| AUTH1 | Auth | POST | `/api/v1/auth/login` | Login valide | 200 | ✅ |
| AUTH2 | Auth | POST | `/api/v1/auth/login` | Mauvais MDP | 401 | ✅ |
| AUTH3 | Auth | POST | `/api/v1/auth/login` | Email inexistant | 401 | ✅ |
| AUTH4 | Auth | POST | `/api/v1/users/` | Sans token | 401 | ✅ |
| U1 | User | POST | `/api/v1/users/` | Création valide (admin) | 201 | ✅ |
| U2 | User | POST | `/api/v1/users/` | Deuxième user | 201 | ✅ |
| U3 | User | GET | `/api/v1/users/` | Lister tous | 200 | ✅ |
| U4 | User | GET | `/api/v1/users/{id}` | Par ID | 200 | ✅ |
| U5 | User | PUT | `/api/v1/users/{id}` | Modifier son profil | 200 | ✅ |
| U6 | User | PUT | `/api/v1/users/{id}` | Admin modifie n'importe qui | 200 | ✅ |
| U7 | User | DELETE | `/api/v1/users/{id}` | Admin supprime user | 200 | ✅ |
| U8 | User | POST | `/api/v1/users/` | Sans token | 401 | ✅ |
| U9 | User | POST | `/api/v1/users/` | Token non-admin | 403 | ✅ |
| U10 | User | POST | `/api/v1/users/` | Email invalide | 400 | ✅ |
| U11 | User | POST | `/api/v1/users/` | Prénom vide | 400 | ✅ |
| U12 | User | POST | `/api/v1/users/` | Prénom > 50 chars | 400 | ✅ |
| U13 | User | POST | `/api/v1/users/` | MDP < 6 chars | 400 | ✅ |
| U14 | User | POST | `/api/v1/users/` | Email dupliqué | 422 | ✅ |
| U15 | User | GET | `/api/v1/users/{id}` | Non trouvé | 404 | ✅ |
| U16 | User | PUT | `/api/v1/users/{id}` | Modifier autre (non admin) | 403 | ✅ |
| U17 | User | PUT | `/api/v1/users/{id}` | Email interdit (non admin) | 400 | ✅ |
| U18 | User | DELETE | `/api/v1/users/{id}` | Non-admin | 403 | ✅ |
| U19 | User | DELETE | `/api/v1/users/{id}` | Admin se supprime | 400 | ✅ |
| U20 | User | DELETE | `/api/v1/users/{id}` | Inexistant | 404 | ✅ |
| A1 | Amenity | POST | `/api/v1/amenities/` | Création valide (admin) | 201 | ✅ |
| A2 | Amenity | GET | `/api/v1/amenities/` | Lister toutes | 200 | ✅ |
| A3 | Amenity | GET | `/api/v1/amenities/{id}` | Par ID | 200 | ✅ |
| A4 | Amenity | PUT | `/api/v1/amenities/{id}` | Modifier (admin) | 200 | ✅ |
| A5 | Amenity | DELETE | `/api/v1/amenities/{id}` | Admin supprime | 200 | ✅ |
| A6 | Amenity | POST | `/api/v1/amenities/` | Sans token | 401 | ✅ |
| A7 | Amenity | POST | `/api/v1/amenities/` | Non-admin | 403 | ✅ |
| A8 | Amenity | POST | `/api/v1/amenities/` | Nom vide | 400 | ✅ |
| A9 | Amenity | POST | `/api/v1/amenities/` | Nom > 50 chars | 400 | ✅ |
| A10 | Amenity | GET | `/api/v1/amenities/{id}` | Non trouvée | 404 | ✅ |
| A11 | Amenity | PUT | `/api/v1/amenities/{id}` | Non-admin | 403 | ✅ |
| A12 | Amenity | DELETE | `/api/v1/amenities/{id}` | Sans token | 401 | ✅ |
| A13 | Amenity | DELETE | `/api/v1/amenities/{id}` | Non-admin | 403 | ✅ |
| A14 | Amenity | DELETE | `/api/v1/amenities/{id}` | Non trouvée | 404 | ✅ |
| P1 | Place | POST | `/api/v1/places/` | Création valide | 201 | ✅ |
| P2 | Place | GET | `/api/v1/places/` | Lister toutes (vue réduite) | 200 | ✅ |
| P3 | Place | GET | `/api/v1/places/{id}` | Vue complète (owner + amenities) | 200 | ✅ |
| P4 | Place | PUT | `/api/v1/places/{id}` | Modifier sa place | 200 | ✅ |
| P5 | Place | PUT | `/api/v1/places/{id}` | Admin bypass | 200 | ✅ |
| P6 | Place | DELETE | `/api/v1/places/{id}` | Propriétaire supprime | 200 | ✅ |
| P7 | Place | DELETE | `/api/v1/places/{id}` | Admin bypass | 200 | ✅ |
| P8 | Place | GET | `/api/v1/places/{id}/reviews` | Reviews d'une place | 200 | ✅ |
| P9 | Place | POST | `/api/v1/places/` | Sans token | 401 | ✅ |
| P10 | Place | POST | `/api/v1/places/` | Prix négatif | 400 | ✅ |
| P11 | Place | POST | `/api/v1/places/` | Latitude invalide | 400 | ✅ |
| P12 | Place | POST | `/api/v1/places/` | Longitude invalide | 400 | ✅ |
| P13 | Place | POST | `/api/v1/places/` | Titre vide | 400 | ✅ |
| P14 | Place | GET | `/api/v1/places/{id}` | Non trouvée | 404 | ✅ |
| P15 | Place | PUT | `/api/v1/places/{id}` | Modifier autre (non proprio) | 403 | ✅ |
| P16 | Place | DELETE | `/api/v1/places/{id}` | Sans token | 401 | ✅ |
| P17 | Place | DELETE | `/api/v1/places/{id}` | Non-propriétaire | 403 | ✅ |
| P18 | Place | DELETE | `/api/v1/places/{id}` | Non trouvée | 404 | ✅ |
| P19 | Place | GET | `/api/v1/places/{id}/reviews` | Place non trouvée | 404 | ✅ |
| R1 | Review | POST | `/api/v1/reviews/` | Création valide | 201 | ✅ |
| R2 | Review | GET | `/api/v1/reviews/` | Lister toutes | 200 | ✅ |
| R3 | Review | GET | `/api/v1/reviews/{id}` | Par ID | 200 | ✅ |
| R4 | Review | PUT | `/api/v1/reviews/{id}` | Modifier sa review | 200 | ✅ |
| R5 | Review | PUT | `/api/v1/reviews/{id}` | Admin bypass | 200 | ✅ |
| R6 | Review | DELETE | `/api/v1/reviews/{id}` | Auteur supprime | 200 | ✅ |
| R7 | Review | DELETE | `/api/v1/reviews/{id}` | Admin bypass | 200 | ✅ |
| R8 | Review | GET | `/api/v1/reviews/{id}` | GET après DELETE | 404 | ✅ |
| R9 | Review | POST | `/api/v1/reviews/` | Sans token | 401 | ✅ |
| R10 | Review | POST | `/api/v1/reviews/` | Review sa propre place | 400 | ✅ |
| R11 | Review | POST | `/api/v1/reviews/` | Review dupliquée | 400 | ✅ |
| R12 | Review | POST | `/api/v1/reviews/` | Rating > 5 | 400 | ✅ |
| R13 | Review | POST | `/api/v1/reviews/` | Rating < 1 | 400 | ✅ |
| R14 | Review | POST | `/api/v1/reviews/` | Texte vide | 400 | ✅ |
| R15 | Review | POST | `/api/v1/reviews/` | Place inexistante | 404 | ✅ |
| R16 | Review | GET | `/api/v1/reviews/{id}` | Non trouvée | 404 | ✅ |
| R17 | Review | PUT | `/api/v1/reviews/{id}` | Modifier autre (non admin) | 403 | ✅ |
| R18 | Review | DELETE | `/api/v1/reviews/{id}` | Non-auteur non-admin | 403 | ✅ |
| R19 | Review | DELETE | `/api/v1/reviews/{id}` | Non trouvée | 404 | ✅ |
| D1 | User | DELETE | `/api/v1/users/{id}` | Admin supprime user | 200 | ✅ |
| D2 | User | DELETE | `/api/v1/users/{id}` | Non-admin | 403 | ✅ |
| D3 | User | DELETE | `/api/v1/users/{admin_id}` | Admin se supprime | 400 | ✅ |
| D4 | User | DELETE | `/api/v1/users/{id}` | Inexistant | 404 | ✅ |
| D5 | Place | DELETE | `/api/v1/places/{id}` | Proprio supprime | 200 | ✅ |
| D6 | Place | DELETE | `/api/v1/places/{id}` | Non-proprio | 403 | ✅ |
| D7 | Place | DELETE | `/api/v1/places/{id}` | Admin bypass | 200 | ✅ |
| D8 | Place | DELETE | `/api/v1/places/{id}` | Inexistante | 404 | ✅ |
| D9 | Amenity | DELETE | `/api/v1/amenities/{id}` | Admin supprime | 200 | ✅ |
| D10 | Amenity | DELETE | `/api/v1/amenities/{id}` | Non-admin | 403 | ✅ |
| D11 | Amenity | DELETE | `/api/v1/amenities/{id}` | Inexistante | 404 | ✅ |

**Total : 88 tests manuels Swagger — 88 passés ✅**

---

_Auteurs : **Sara Rebati · Valentin Planchon · Damien Rossi** — Holberton School 2026_