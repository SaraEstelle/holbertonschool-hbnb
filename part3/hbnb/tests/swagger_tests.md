# HBnB — Guide de Tests Swagger
## Organises par type : Auth, CRUD, RBAC, Relations

---

## Acces a Swagger

1. Lancer le serveur :
```bash
python3 run.py
```
2. Ouvrir dans le navigateur :
```
http://127.0.0.1:5000/api/v1/
```

---

## Comment utiliser le token JWT dans Swagger

1. Faire `POST /api/v1/auth/login` et copier le `access_token`
2. Cliquer sur **Authorize** en haut a droite
3. Saisir `Bearer <token>` dans le champ Value
4. Cliquer **Authorize** puis **Close**

---

## IDs utiles (donnees initiales)

| Donnee | ID |
|---|---|
| Admin | `36c9050e-ddd3-4c3b-9731-9f487208bbc1` |
| WiFi | `7c9fdf4d-99be-4b1c-8c2e-5aea5db0d0eb` |
| Swimming Pool | `ae5ae8a5-0203-451b-9cb8-6086e5b2f41e` |
| Air Conditioning | `97bc1cc5-3dcd-439e-894f-e9986dedd012` |

---

## ============================================================
## SECTION 1 — AUTH
## ============================================================

### TEST 1.1 — Login admin valide
**Endpoint :** `POST /api/v1/auth/login`
```json
{ "email": "admin@hbnb.io", "password": "admin1234" }
```
**Attendu :** `200` + `access_token`
> Sauvegarder le token et l'utiliser dans Authorize.

---

### TEST 1.2 — Login mauvais mot de passe
**Endpoint :** `POST /api/v1/auth/login`
```json
{ "email": "admin@hbnb.io", "password": "mauvais_mdp" }
```
**Attendu :** `401 Invalid credentials`

---

### TEST 1.3 — Login email inexistant
**Endpoint :** `POST /api/v1/auth/login`
```json
{ "email": "inexistant@test.com", "password": "admin1234" }
```
**Attendu :** `401 Invalid credentials`

---

### TEST 1.4 — Acces endpoint protege sans token
Cliquer Authorize -> Logout (enlever le token)

**Endpoint :** `POST /api/v1/users/`
```json
{ "first_name": "Test", "last_name": "User", "email": "t@t.com", "password": "pass123" }
```
**Attendu :** `401 Missing Authorization Header`

---

### TEST 1.5 — Acces endpoint protege avec token valide
Se reconnecter avec le token admin dans Authorize.

**Endpoint :** `POST /api/v1/amenities/`
```json
{ "name": "Sauna", "description": "Private sauna" }
```
**Attendu :** `201` avec l'id de la nouvelle amenity

---

## ============================================================
## SECTION 2 — CRUD : USERS
## ============================================================

> Token admin requis pour POST.
> Sauvegarder les IDs crees pour les tests suivants.

### TEST 2.1 — Creer un user valide (John)
**Endpoint :** `POST /api/v1/users/` | Token : admin
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@test.com",
  "password": "password123"
}
```
**Attendu :** `201` | **Sauvegarder l'ID de John**

---

### TEST 2.2 — Creer un deuxieme user (Jane)
**Endpoint :** `POST /api/v1/users/` | Token : admin
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane@test.com",
  "password": "password123"
}
```
**Attendu :** `201` | **Sauvegarder l'ID de Jane**

---

### TEST 2.3 — Rejeter email duplique
**Endpoint :** `POST /api/v1/users/` | Token : admin
```json
{
  "first_name": "Dup",
  "last_name": "User",
  "email": "john@test.com",
  "password": "password123"
}
```
**Attendu :** `422 Email already registered`

---

### TEST 2.4 — Lire tous les users
**Endpoint :** `GET /api/v1/users/` | Public
**Attendu :** `200` + liste de 3 users (admin, John, Jane)

---

### TEST 2.5 — Lire un user par ID
**Endpoint :** `GET /api/v1/users/<john_id>` | Public
**Attendu :** `200` avec les details de John

---

### TEST 2.6 — Lire un user inexistant
**Endpoint :** `GET /api/v1/users/00000000-0000-0000-0000-000000000000` | Public
**Attendu :** `404 User not found`

---

### TEST 2.7 — Modifier son propre profil
Faire login avec John (`john@test.com` / `password123`) et utiliser son token.

**Endpoint :** `PUT /api/v1/users/<john_id>` | Token : John
```json
{ "first_name": "Johnny", "last_name": "Doe" }
```
**Attendu :** `200` avec first_name = "Johnny"

---

### TEST 2.8 — Modifier le profil d'un autre user (sans etre admin)
**Endpoint :** `PUT /api/v1/users/<jane_id>` | Token : John
```json
{ "first_name": "Hacked" }
```
**Attendu :** `403 Unauthorized action`

---

### TEST 2.9 — Essayer de modifier email via PUT /users
**Endpoint :** `PUT /api/v1/users/<john_id>` | Token : John
```json
{ "email": "newemail@test.com" }
```
**Attendu :** `400 You cannot modify email or password`

---

## ============================================================
## SECTION 3 — CRUD : AMENITIES
## ============================================================

### TEST 3.1 — Creer une amenity valide (admin)
**Endpoint :** `POST /api/v1/amenities/` | Token : admin
```json
{ "name": "Jacuzzi", "description": "Luxury jacuzzi" }
```
**Attendu :** `201` | **Sauvegarder l'ID**

---

### TEST 3.2 — Creer une amenity sans etre admin
**Endpoint :** `POST /api/v1/amenities/` | Token : John
```json
{ "name": "Bain de soleil", "description": "Terrace" }
```
**Attendu :** `403 Admin privileges required`

---

### TEST 3.3 — Lire toutes les amenities
**Endpoint :** `GET /api/v1/amenities/` | Public
**Attendu :** `200` + liste (WiFi, Swimming Pool, Air Conditioning, Sauna, Jacuzzi)

---

### TEST 3.4 — Lire une amenity par ID
**Endpoint :** `GET /api/v1/amenities/<jacuzzi_id>` | Public
**Attendu :** `200` avec les details du Jacuzzi

---

### TEST 3.5 — Lire une amenity inexistante
**Endpoint :** `GET /api/v1/amenities/00000000-0000-0000-0000-000000000000`
**Attendu :** `404 Amenity not found`

---

### TEST 3.6 — Modifier une amenity (admin)
**Endpoint :** `PUT /api/v1/amenities/<jacuzzi_id>` | Token : admin
```json
{ "name": "Jacuzzi VIP", "description": "Luxury private jacuzzi" }
```
**Attendu :** `200 Amenity updated successfully`

---

### TEST 3.7 — Modifier une amenity sans etre admin
**Endpoint :** `PUT /api/v1/amenities/<jacuzzi_id>` | Token : John
```json
{ "name": "Hacked" }
```
**Attendu :** `403 Admin privileges required`

---

## ============================================================
## SECTION 4 — CRUD : PLACES
## ============================================================

> Le owner_id est pris automatiquement depuis le token JWT.

### TEST 4.1 — Creer une place valide (John)
**Endpoint :** `POST /api/v1/places/` | Token : John
```json
{
  "title": "Appartement Paris",
  "description": "Beau appartement au coeur de Paris",
  "price": 120.00,
  "latitude": 48.8566,
  "longitude": 2.3522,
  "amenities": ["7c9fdf4d-99be-4b1c-8c2e-5aea5db0d0eb"]
}
```
**Attendu :** `201` | **Sauvegarder l'ID de la place**

---

### TEST 4.2 — Creer une place avec prix negatif
**Endpoint :** `POST /api/v1/places/` | Token : John
```json
{
  "title": "Bad Place",
  "description": "Invalid",
  "price": -50.00,
  "latitude": 48.8566,
  "longitude": 2.3522,
  "amenities": []
}
```
**Attendu :** `400 price must be a non-negative number`

---

### TEST 4.3 — Creer une place avec latitude invalide
**Endpoint :** `POST /api/v1/places/` | Token : John
```json
{
  "title": "Bad Lat",
  "description": "Invalid",
  "price": 50.00,
  "latitude": 999.00,
  "longitude": 2.3522,
  "amenities": []
}
```
**Attendu :** `400 latitude must be between -90 and 90`

---

### TEST 4.4 — Lire toutes les places
**Endpoint :** `GET /api/v1/places/` | Public
**Attendu :** `200` + liste des places

---

### TEST 4.5 — Lire une place par ID (avec owner et amenities)
**Endpoint :** `GET /api/v1/places/<place_id>` | Public
**Attendu :** `200` avec owner, amenities, reviews imbriques

---

### TEST 4.6 — Lire une place inexistante
**Endpoint :** `GET /api/v1/places/00000000-0000-0000-0000-000000000000`
**Attendu :** `404 Place not found`

---

### TEST 4.7 — Modifier sa propre place
**Endpoint :** `PUT /api/v1/places/<place_id>` | Token : John
```json
{ "title": "Appartement Paris - Renove", "price": 150.00 }
```
**Attendu :** `200 Place updated successfully`

---

### TEST 4.8 — Modifier la place d'un autre user (sans etre admin)
**Endpoint :** `PUT /api/v1/places/<place_id>` | Token : Jane
```json
{ "title": "Hacked place" }
```
**Attendu :** `403 Unauthorized action`

---

## ============================================================
## SECTION 5 — CRUD : REVIEWS
## ============================================================

### TEST 5.1 — Creer une review valide (Jane sur la place de John)
**Endpoint :** `POST /api/v1/reviews/` | Token : Jane
```json
{
  "text": "Super endroit, tres bien situe !",
  "rating": 5,
  "place_id": "<place_id>"
}
```
**Attendu :** `201` | **Sauvegarder l'ID de la review**

---

### TEST 5.2 — Creer une review sur sa propre place
**Endpoint :** `POST /api/v1/reviews/` | Token : John
```json
{
  "text": "Ma propre place",
  "rating": 5,
  "place_id": "<place_id>"
}
```
**Attendu :** `400 You cannot review your own place`

---

### TEST 5.3 — Creer un doublon de review (meme user / meme place)
**Endpoint :** `POST /api/v1/reviews/` | Token : Jane
```json
{
  "text": "Deuxieme review",
  "rating": 3,
  "place_id": "<place_id>"
}
```
**Attendu :** `400 You have already reviewed this place`

---

### TEST 5.4 — Creer une review avec rating invalide
**Endpoint :** `POST /api/v1/reviews/` | Token : Jane
```json
{
  "text": "Bad rating",
  "rating": 10,
  "place_id": "<place_id>"
}
```
**Attendu :** `400 Rating must be between 1 and 5`

---

### TEST 5.5 — Lire toutes les reviews
**Endpoint :** `GET /api/v1/reviews/` | Public
**Attendu :** `200` + liste

---

### TEST 5.6 — Lire une review par ID
**Endpoint :** `GET /api/v1/reviews/<review_id>` | Public
**Attendu :** `200` avec details

---

### TEST 5.7 — Lire les reviews d'une place
**Endpoint :** `GET /api/v1/places/<place_id>/reviews` | Public
**Attendu :** `200` + liste des reviews de cette place

---

### TEST 5.8 — Modifier sa propre review
**Endpoint :** `PUT /api/v1/reviews/<review_id>` | Token : Jane
```json
{ "text": "Encore mieux que prevu !", "rating": 5 }
```
**Attendu :** `200 Review updated successfully`

---

### TEST 5.9 — Modifier la review d'un autre user (sans etre admin)
**Endpoint :** `PUT /api/v1/reviews/<review_id>` | Token : John
```json
{ "text": "Hacked review", "rating": 1 }
```
**Attendu :** `403 Unauthorized action`

---

### TEST 5.10 — Supprimer sa propre review
**Endpoint :** `DELETE /api/v1/reviews/<review_id>` | Token : Jane
**Attendu :** `200 Review deleted successfully`

---

### TEST 5.11 — Supprimer une review inexistante
**Endpoint :** `DELETE /api/v1/reviews/00000000-0000-0000-0000-000000000000` | Token : admin
**Attendu :** `404 Review not found`

---

## ============================================================
## SECTION 6 — RBAC (Role Based Access Control)
## ============================================================

### TEST 6.1 — Admin cree un user
**Endpoint :** `POST /api/v1/users/` | Token : admin
```json
{
  "first_name": "New",
  "last_name": "User",
  "email": "new@test.com",
  "password": "password123"
}
```
**Attendu :** `201`

---

### TEST 6.2 — User normal essaie de creer un user
**Endpoint :** `POST /api/v1/users/` | Token : John
```json
{
  "first_name": "Hack",
  "last_name": "User",
  "email": "hack@test.com",
  "password": "password123"
}
```
**Attendu :** `403 Admin privileges required`

---

### TEST 6.3 — Admin modifie un user qui ne lui appartient pas
**Endpoint :** `PUT /api/v1/users/<john_id>` | Token : admin
```json
{ "first_name": "Admin Updated" }
```
**Attendu :** `200` (admin bypasse ownership)

---

### TEST 6.4 — Admin cree une amenity
**Endpoint :** `POST /api/v1/amenities/` | Token : admin
```json
{ "name": "Terrasse", "description": "Private terrace" }
```
**Attendu :** `201`

---

### TEST 6.5 — User normal essaie de creer une amenity
**Endpoint :** `POST /api/v1/amenities/` | Token : John
```json
{ "name": "Terrasse2", "description": "Private terrace" }
```
**Attendu :** `403 Admin privileges required`

---

### TEST 6.6 — Admin modifie une place qui ne lui appartient pas
Recreer la review de Jane si necessaire.

**Endpoint :** `PUT /api/v1/places/<place_id>` | Token : admin
```json
{ "title": "Place modifiee par admin", "price": 200.00 }
```
**Attendu :** `200` (admin bypasse ownership)

---

### TEST 6.7 — Admin supprime la review d'un autre user
Recreer une review de Jane d'abord si necessaire.

**Endpoint :** `DELETE /api/v1/reviews/<review_id>` | Token : admin
**Attendu :** `200` (admin bypasse ownership)

---

### TEST 6.8 — Admin modifie une amenity
**Endpoint :** `PUT /api/v1/amenities/<amenity_id>` | Token : admin
```json
{ "name": "Terrasse VIP" }
```
**Attendu :** `200 Amenity updated successfully`

---

## ============================================================
## SECTION 7 — RELATIONS
## ============================================================

### TEST 7.1 — Place retourne son owner dans GET
**Endpoint :** `GET /api/v1/places/<place_id>` | Public

Verifier que la reponse contient :
```json
{
  "owner": {
    "id": "...",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@test.com"
  }
}
```
**Attendu :** `200` avec owner imbrique

---

### TEST 7.2 — Place retourne ses amenities dans GET
**Endpoint :** `GET /api/v1/places/<place_id>` | Public

Verifier que la reponse contient :
```json
{
  "amenities": [
    { "id": "7c9fdf4d...", "name": "WiFi" }
  ]
}
```
**Attendu :** `200` avec amenities imbriquees

---

### TEST 7.3 — Reviews d'une place retournent user_id et place_id
**Endpoint :** `GET /api/v1/places/<place_id>/reviews` | Public

Verifier que chaque review contient `user_id` et `place_id`.
**Attendu :** `200` avec reviews imbriquees

---

### TEST 7.4 — Place inexistante dans reviews
**Endpoint :** `GET /api/v1/places/00000000-0000-0000-0000-000000000000/reviews`
**Attendu :** `404 Place not found`

---

## Recapitulatif

| Section | Nb tests | Valides | Invalides |
|---|---|---|---|
| Auth | 5 | 2 | 3 |
| CRUD Users | 9 | 6 | 3 |
| CRUD Amenities | 7 | 4 | 3 |
| CRUD Places | 8 | 4 | 4 |
| CRUD Reviews | 11 | 5 | 6 |
| RBAC | 8 | 5 | 3 |
| Relations | 4 | 4 | 0 |
| **Total** | **52** | **30** | **22** |
