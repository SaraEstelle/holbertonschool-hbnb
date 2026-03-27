#!/usr/bin/env python3
"""
HBnB — Tests API automatises
Teste tous les endpoints HTTP avec requests.
Organises par type : Auth, CRUD, RBAC, Relations

Usage :
    1. Lancer le serveur : python3 run.py
    2. Lancer les tests  : python3 tests/test_api.py
"""

import requests
import sys

# ============================================================
# Configuration
# ============================================================

BASE_URL = "http://127.0.0.1:5000/api/v1"

ADMIN_EMAIL = "admin@hbnb.io"
ADMIN_PASSWORD = "admin1234"

WIFI_ID = "7c9fdf4d-99be-4b1c-8c2e-5aea5db0d0eb"
POOL_ID = "ae5ae8a5-0203-451b-9cb8-6086e5b2f41e"
AIRCO_ID = "97bc1cc5-3dcd-439e-894f-e9986dedd012"

# ============================================================
# Utilitaires
# ============================================================

passed = 0
failed = 0
total = 0

# Stockage des IDs crees pendant les tests
state = {
    "admin_token": None,
    "john_token": None,
    "jane_token": None,
    "john_id": None,
    "jane_id": None,
    "place_id": None,
    "review_id": None,
    "amenity_id": None,
}


def test(name, condition, details=""):
    global passed, failed, total
    total += 1
    if condition:
        passed += 1
        print(f"  [OK]   {name}")
    else:
        failed += 1
        print(f"  [FAIL] {name}")
        if details:
            print(f"         Details : {details}")


def section(title):
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def post(url, data, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return requests.post(f"{BASE_URL}{url}", json=data, headers=headers)


def get(url, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return requests.get(f"{BASE_URL}{url}", headers=headers)


def put(url, data, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return requests.put(f"{BASE_URL}{url}", json=data, headers=headers)


def delete(url, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return requests.delete(f"{BASE_URL}{url}", headers=headers)


# ============================================================
# SECTION 1 — AUTH
# ============================================================

def test_auth():
    section("SECTION 1 — AUTH")

    # TEST 1.1 — Login admin valide
    r = post("/auth/login", {"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    test("1.1 — Login admin valide -> 200 + token",
         r.status_code == 200 and "access_token" in r.json(),
         f"status={r.status_code}")
    if r.status_code == 200:
        state["admin_token"] = r.json()["access_token"]

    # TEST 1.2 — Login mauvais mot de passe
    r = post("/auth/login", {"email": ADMIN_EMAIL, "password": "mauvais"})
    test("1.2 — Login mauvais mot de passe -> 401",
         r.status_code == 401,
         f"status={r.status_code}")

    # TEST 1.3 — Login email inexistant
    r = post("/auth/login", {"email": "inexistant@test.com", "password": "admin1234"})
    test("1.3 — Login email inexistant -> 401",
         r.status_code == 401,
         f"status={r.status_code}")

    # TEST 1.4 — Acces endpoint protege sans token
    r = post("/users/", {
        "first_name": "Test", "last_name": "User",
        "email": "test@test.com", "password": "pass123"
    })
    test("1.4 — POST /users/ sans token -> 401",
         r.status_code == 401,
         f"status={r.status_code}")

    # TEST 1.5 — Acces endpoint protege avec token valide
    r = post("/amenities/", {"name": "TestAuth"},
             token=state["admin_token"])
    test("1.5 — POST /amenities/ avec token admin -> 201",
         r.status_code == 201,
         f"status={r.status_code}")
    # Nettoyer l'amenity creee
    if r.status_code == 201:
        amenity_id = r.json().get("id")
        if amenity_id:
            put(f"/amenities/{amenity_id}",
                {"name": "TestAuthCleaned"},
                token=state["admin_token"])


# ============================================================
# SECTION 2 — CRUD : USERS
# ============================================================

def test_crud_users():
    section("SECTION 2 — CRUD : USERS")

    print("\n  -- CREATE --")

    # TEST 2.1 — Creer John
    r = post("/users/", {
        "first_name": "John", "last_name": "Doe",
        "email": "john@test.com", "password": "password123"
    }, token=state["admin_token"])
    test("2.1 — Creer user valide (John) -> 201",
         r.status_code == 201,
         f"status={r.status_code}, body={r.text[:100]}")
    if r.status_code == 201:
        state["john_id"] = r.json()["id"]

    # TEST 2.2 — Creer Jane
    r = post("/users/", {
        "first_name": "Jane", "last_name": "Smith",
        "email": "jane@test.com", "password": "password123"
    }, token=state["admin_token"])
    test("2.2 — Creer deuxieme user (Jane) -> 201",
         r.status_code == 201,
         f"status={r.status_code}")
    if r.status_code == 201:
        state["jane_id"] = r.json()["id"]

    # TEST 2.3 — Email duplique
    r = post("/users/", {
        "first_name": "Dup", "last_name": "User",
        "email": "john@test.com", "password": "password123"
    }, token=state["admin_token"])
    test("2.3 — Email duplique -> 422",
         r.status_code == 422,
         f"status={r.status_code}")

    # TEST 2.4 — Login John et Jane pour leurs tokens
    r = post("/auth/login", {"email": "john@test.com", "password": "password123"})
    if r.status_code == 200:
        state["john_token"] = r.json()["access_token"]

    r = post("/auth/login", {"email": "jane@test.com", "password": "password123"})
    if r.status_code == 200:
        state["jane_token"] = r.json()["access_token"]

    test("2.4 — Login John et Jane -> tokens obtenus",
         state["john_token"] is not None and state["jane_token"] is not None)

    print("\n  -- READ --")

    # TEST 2.5 — Lire tous les users
    r = get("/users/")
    test("2.5 — GET /users/ -> 200",
         r.status_code == 200,
         f"status={r.status_code}")

    # TEST 2.6 — Lire user par ID
    if state["john_id"]:
        r = get(f"/users/{state['john_id']}")
        test("2.6 — GET /users/<john_id> -> 200 avec donnees",
             r.status_code == 200 and r.json().get("first_name") == "John",
             f"status={r.status_code}")

    # TEST 2.7 — User inexistant
    r = get("/users/00000000-0000-0000-0000-000000000000")
    test("2.7 — GET user inexistant -> 404",
         r.status_code == 404,
         f"status={r.status_code}")

    print("\n  -- UPDATE --")

    # TEST 2.8 — Modifier son propre profil
    if state["john_id"] and state["john_token"]:
        r = put(f"/users/{state['john_id']}",
                {"first_name": "Johnny", "last_name": "Doe"},
                token=state["john_token"])
        test("2.8 — PUT /users/<john_id> par John -> 200",
             r.status_code == 200,
             f"status={r.status_code}")

    # TEST 2.9 — Modifier profil d'un autre user
    if state["jane_id"] and state["john_token"]:
        r = put(f"/users/{state['jane_id']}",
                {"first_name": "Hacked"},
                token=state["john_token"])
        test("2.9 — PUT /users/<jane_id> par John -> 403",
             r.status_code == 403,
             f"status={r.status_code}")

    # TEST 2.10 — Modifier email via PUT /users
    if state["john_id"] and state["john_token"]:
        r = put(f"/users/{state['john_id']}",
                {"email": "newemail@test.com"},
                token=state["john_token"])
        test("2.10 — Modifier email via PUT /users -> 400",
             r.status_code == 400,
             f"status={r.status_code}")


# ============================================================
# SECTION 3 — CRUD : AMENITIES
# ============================================================

def test_crud_amenities():
    section("SECTION 3 — CRUD : AMENITIES")

    print("\n  -- CREATE --")

    # TEST 3.1 — Creer amenity valide
    r = post("/amenities/",
             {"name": "Jacuzzi", "description": "Luxury jacuzzi"},
             token=state["admin_token"])
    test("3.1 — POST /amenities/ admin -> 201",
         r.status_code == 201,
         f"status={r.status_code}")
    if r.status_code == 201:
        state["amenity_id"] = r.json()["id"]

    # TEST 3.2 — Creer amenity sans etre admin
    r = post("/amenities/",
             {"name": "Bain de soleil"},
             token=state["john_token"])
    test("3.2 — POST /amenities/ user normal -> 403",
         r.status_code == 403,
         f"status={r.status_code}")

    # TEST 3.3 — Creer amenity sans token
    r = post("/amenities/", {"name": "NoToken"})
    test("3.3 — POST /amenities/ sans token -> 401",
         r.status_code == 401,
         f"status={r.status_code}")

    print("\n  -- READ --")

    # TEST 3.4 — Lire toutes les amenities
    r = get("/amenities/")
    test("3.4 — GET /amenities/ -> 200",
         r.status_code == 200,
         f"status={r.status_code}")

    # TEST 3.5 — Lire amenity par ID
    if state["amenity_id"]:
        r = get(f"/amenities/{state['amenity_id']}")
        test("3.5 — GET /amenities/<id> -> 200",
             r.status_code == 200 and r.json().get("name") == "Jacuzzi",
             f"status={r.status_code}")

    # TEST 3.6 — Amenity inexistante
    r = get("/amenities/00000000-0000-0000-0000-000000000000")
    test("3.6 — GET amenity inexistante -> 404",
         r.status_code == 404,
         f"status={r.status_code}")

    print("\n  -- UPDATE --")

    # TEST 3.7 — Modifier amenity (admin)
    if state["amenity_id"]:
        r = put(f"/amenities/{state['amenity_id']}",
                {"name": "Jacuzzi VIP", "description": "Luxury private jacuzzi"},
                token=state["admin_token"])
        test("3.7 — PUT /amenities/<id> admin -> 200",
             r.status_code == 200,
             f"status={r.status_code}")

    # TEST 3.8 — Modifier amenity sans etre admin
    if state["amenity_id"]:
        r = put(f"/amenities/{state['amenity_id']}",
                {"name": "Hacked"},
                token=state["john_token"])
        test("3.8 — PUT /amenities/<id> user normal -> 403",
             r.status_code == 403,
             f"status={r.status_code}")


# ============================================================
# SECTION 4 — CRUD : PLACES
# ============================================================

def test_crud_places():
    section("SECTION 4 — CRUD : PLACES")

    print("\n  -- CREATE --")

    # TEST 4.1 — Creer place valide
    r = post("/places/", {
        "title": "Appartement Paris",
        "description": "Beau appartement",
        "price": 120.00,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "amenities": [WIFI_ID]
    }, token=state["john_token"])
    test("4.1 — POST /places/ John -> 201",
         r.status_code == 201,
         f"status={r.status_code}, body={r.text[:150]}")
    if r.status_code == 201:
        state["place_id"] = r.json()["id"]

    # TEST 4.2 — Prix negatif
    r = post("/places/", {
        "title": "Bad Place", "description": "Invalid",
        "price": -50.00, "latitude": 48.8566, "longitude": 2.3522,
        "amenities": []
    }, token=state["john_token"])
    test("4.2 — Prix negatif -> 400",
         r.status_code == 400,
         f"status={r.status_code}")

    # TEST 4.3 — Latitude invalide
    r = post("/places/", {
        "title": "Bad Lat", "description": "Invalid",
        "price": 50.00, "latitude": 999.00, "longitude": 2.3522,
        "amenities": []
    }, token=state["john_token"])
    test("4.3 — Latitude invalide -> 400",
         r.status_code == 400,
         f"status={r.status_code}")

    # TEST 4.4 — Sans token
    r = post("/places/", {
        "title": "No token", "description": "Invalid",
        "price": 50.00, "latitude": 48.00, "longitude": 2.00,
        "amenities": []
    })
    test("4.4 — POST /places/ sans token -> 401",
         r.status_code == 401,
         f"status={r.status_code}")

    print("\n  -- READ --")

    # TEST 4.5 — Lire toutes les places
    r = get("/places/")
    test("4.5 — GET /places/ -> 200",
         r.status_code == 200,
         f"status={r.status_code}")

    # TEST 4.6 — Lire place par ID avec owner et amenities
    if state["place_id"]:
        r = get(f"/places/{state['place_id']}")
        data = r.json()
        test("4.6 — GET /places/<id> retourne owner et amenities",
             r.status_code == 200
             and "owner" in data
             and "amenities" in data,
             f"status={r.status_code}, keys={list(data.keys())}")

    # TEST 4.7 — Place inexistante
    r = get("/places/00000000-0000-0000-0000-000000000000")
    test("4.7 — GET place inexistante -> 404",
         r.status_code == 404,
         f"status={r.status_code}")

    print("\n  -- UPDATE --")

    # TEST 4.8 — Modifier sa propre place
    if state["place_id"] and state["john_token"]:
        r = put(f"/places/{state['place_id']}",
                {"title": "Appartement Paris Renove", "price": 150.00},
                token=state["john_token"])
        test("4.8 — PUT /places/<id> par proprio -> 200",
             r.status_code == 200,
             f"status={r.status_code}")

    # TEST 4.9 — Modifier place d'un autre
    if state["place_id"] and state["jane_token"]:
        r = put(f"/places/{state['place_id']}",
                {"title": "Hacked place"},
                token=state["jane_token"])
        test("4.9 — PUT /places/<id> par autre user -> 403",
             r.status_code == 403,
             f"status={r.status_code}")


# ============================================================
# SECTION 5 — CRUD : REVIEWS
# ============================================================

def test_crud_reviews():
    section("SECTION 5 — CRUD : REVIEWS")

    print("\n  -- CREATE --")

    # TEST 5.1 — Review valide (Jane sur place de John)
    if state["place_id"] and state["jane_token"]:
        r = post("/reviews/", {
            "text": "Super endroit, tres bien situe !",
            "rating": 5,
            "place_id": state["place_id"]
        }, token=state["jane_token"])
        test("5.1 — POST /reviews/ Jane -> 201",
             r.status_code == 201,
             f"status={r.status_code}")
        if r.status_code == 201:
            state["review_id"] = r.json()["id"]

    # TEST 5.2 — Review sur sa propre place
    if state["place_id"] and state["john_token"]:
        r = post("/reviews/", {
            "text": "Ma propre place est top",
            "rating": 5,
            "place_id": state["place_id"]
        }, token=state["john_token"])
        test("5.2 — Review sur sa propre place -> 400",
             r.status_code == 400,
             f"status={r.status_code}")

    # TEST 5.3 — Doublon review
    if state["place_id"] and state["jane_token"]:
        r = post("/reviews/", {
            "text": "Deuxieme review",
            "rating": 3,
            "place_id": state["place_id"]
        }, token=state["jane_token"])
        test("5.3 — Doublon review -> 400",
             r.status_code == 400,
             f"status={r.status_code}")

    # TEST 5.4 — Rating invalide
    if state["place_id"] and state["admin_token"]:
        r = post("/reviews/", {
            "text": "Bad rating",
            "rating": 10,
            "place_id": state["place_id"]
        }, token=state["admin_token"])
        test("5.4 — Rating invalide -> 400",
             r.status_code == 400,
             f"status={r.status_code}")

    # TEST 5.5 — Sans token
    r = post("/reviews/", {
        "text": "No token", "rating": 3,
        "place_id": state["place_id"] or "fake-id"
    })
    test("5.5 — POST /reviews/ sans token -> 401",
         r.status_code == 401,
         f"status={r.status_code}")

    print("\n  -- READ --")

    # TEST 5.6 — Lire toutes les reviews
    r = get("/reviews/")
    test("5.6 — GET /reviews/ -> 200",
         r.status_code == 200,
         f"status={r.status_code}")

    # TEST 5.7 — Lire review par ID
    if state["review_id"]:
        r = get(f"/reviews/{state['review_id']}")
        test("5.7 — GET /reviews/<id> -> 200",
             r.status_code == 200,
             f"status={r.status_code}")

    # TEST 5.8 — Lire reviews d'une place
    if state["place_id"]:
        r = get(f"/places/{state['place_id']}/reviews")
        test("5.8 — GET /places/<id>/reviews -> 200",
             r.status_code == 200,
             f"status={r.status_code}")

    # TEST 5.9 — Reviews place inexistante
    r = get("/places/00000000-0000-0000-0000-000000000000/reviews")
    test("5.9 — GET reviews place inexistante -> 404",
         r.status_code == 404,
         f"status={r.status_code}")

    print("\n  -- UPDATE --")

    # TEST 5.10 — Modifier sa propre review
    if state["review_id"] and state["jane_token"]:
        r = put(f"/reviews/{state['review_id']}",
                {"text": "Encore mieux que prevu !", "rating": 5},
                token=state["jane_token"])
        test("5.10 — PUT /reviews/<id> par auteur -> 200",
             r.status_code == 200,
             f"status={r.status_code}")

    # TEST 5.11 — Modifier review d'un autre
    if state["review_id"] and state["john_token"]:
        r = put(f"/reviews/{state['review_id']}",
                {"text": "Hacked review", "rating": 1},
                token=state["john_token"])
        test("5.11 — PUT /reviews/<id> par autre user -> 403",
             r.status_code == 403,
             f"status={r.status_code}")

    print("\n  -- DELETE --")

    # TEST 5.12 — Supprimer review inexistante
    r = delete("/reviews/00000000-0000-0000-0000-000000000000",
               token=state["admin_token"])
    test("5.12 — DELETE review inexistante -> 404",
         r.status_code == 404,
         f"status={r.status_code}")

    # TEST 5.13 — Supprimer review d'un autre (sans etre admin)
    if state["review_id"] and state["john_token"]:
        r = delete(f"/reviews/{state['review_id']}",
                   token=state["john_token"])
        test("5.13 — DELETE review d'un autre -> 403",
             r.status_code == 403,
             f"status={r.status_code}")

    # TEST 5.14 — Supprimer sa propre review
    if state["review_id"] and state["jane_token"]:
        r = delete(f"/reviews/{state['review_id']}",
                   token=state["jane_token"])
        test("5.14 — DELETE review par auteur -> 200",
             r.status_code == 200,
             f"status={r.status_code}")


# ============================================================
# SECTION 6 — RBAC
# ============================================================

def test_rbac():
    section("SECTION 6 — RBAC (Role Based Access Control)")

    # TEST 6.1 — Admin cree un user
    r = post("/users/", {
        "first_name": "New", "last_name": "User",
        "email": "newuser@test.com", "password": "password123"
    }, token=state["admin_token"])
    test("6.1 — Admin cree un user -> 201",
         r.status_code == 201,
         f"status={r.status_code}")
    new_user_id = r.json().get("id") if r.status_code == 201 else None

    # TEST 6.2 — User normal essaie de creer un user
    r = post("/users/", {
        "first_name": "Hack", "last_name": "Attempt",
        "email": "hack@test.com", "password": "password123"
    }, token=state["john_token"])
    test("6.2 — User normal cree un user -> 403",
         r.status_code == 403,
         f"status={r.status_code}")

    # TEST 6.3 — Admin modifie un user qui ne lui appartient pas
    if state["john_id"]:
        r = put(f"/users/{state['john_id']}",
                {"first_name": "Admin Updated"},
                token=state["admin_token"])
        test("6.3 — Admin modifie user d'un autre -> 200 (bypass)",
             r.status_code == 200,
             f"status={r.status_code}")

    # TEST 6.4 — User normal cree une amenity
    r = post("/amenities/",
             {"name": "Unauthorized Amenity"},
             token=state["john_token"])
    test("6.4 — User normal cree amenity -> 403",
         r.status_code == 403,
         f"status={r.status_code}")

    # TEST 6.5 — Admin cree une amenity
    r = post("/amenities/",
             {"name": "Admin Amenity"},
             token=state["admin_token"])
    test("6.5 — Admin cree une amenity -> 201",
         r.status_code == 201,
         f"status={r.status_code}")
    admin_amenity_id = r.json().get("id") if r.status_code == 201 else None

    # TEST 6.6 — Admin modifie place d'un autre
    if state["place_id"]:
        r = put(f"/places/{state['place_id']}",
                {"title": "Modified by Admin", "price": 200.00},
                token=state["admin_token"])
        test("6.6 — Admin modifie place d'un autre -> 200 (bypass)",
             r.status_code == 200,
             f"status={r.status_code}")

    # TEST 6.7 — Admin modifie amenity
    if state["amenity_id"]:
        r = put(f"/amenities/{state['amenity_id']}",
                {"name": "Admin Modified Amenity"},
                token=state["admin_token"])
        test("6.7 — Admin modifie une amenity -> 200",
             r.status_code == 200,
             f"status={r.status_code}")

    # TEST 6.8 — Admin supprime review d'un autre
    # Creer une review de Jane pour tester
    if state["place_id"] and state["jane_token"]:
        r = post("/reviews/", {
            "text": "Review pour test admin delete",
            "rating": 4,
            "place_id": state["place_id"]
        }, token=state["jane_token"])
        if r.status_code == 201:
            review_id = r.json()["id"]
            r2 = delete(f"/reviews/{review_id}", token=state["admin_token"])
            test("6.8 — Admin supprime review d'un autre -> 200 (bypass)",
                 r2.status_code == 200,
                 f"status={r2.status_code}")
        else:
            test("6.8 — Admin supprime review d'un autre -> 200 (bypass)",
                 False, "Impossible de creer la review de test")


# ============================================================
# SECTION 7 — RELATIONS
# ============================================================

def test_relations():
    section("SECTION 7 — RELATIONS")

    # TEST 7.1 — GET place retourne owner imbrique
    if state["place_id"]:
        r = get(f"/places/{state['place_id']}")
        data = r.json()
        owner = data.get("owner")
        test("7.1 — GET /places/<id> retourne owner imbrique",
             r.status_code == 200
             and owner is not None
             and "first_name" in owner
             and "email" in owner,
             f"owner={owner}")

    # TEST 7.2 — GET place retourne amenities imbriquees
    if state["place_id"]:
        r = get(f"/places/{state['place_id']}")
        data = r.json()
        amenities = data.get("amenities", [])
        test("7.2 — GET /places/<id> retourne amenities",
             r.status_code == 200 and isinstance(amenities, list),
             f"amenities={amenities}")

    # TEST 7.3 — Reviews d'une place retournent user_id et place_id
    if state["place_id"] and state["jane_token"]:
        # Creer une review pour ce test
        r = post("/reviews/", {
            "text": "Review pour test relation",
            "rating": 3,
            "place_id": state["place_id"]
        }, token=state["jane_token"])
        if r.status_code == 201:
            review_id = r.json()["id"]
            r2 = get(f"/places/{state['place_id']}/reviews")
            reviews = r2.json()
            test("7.3 — GET /places/<id>/reviews retourne user_id et place_id",
                 r2.status_code == 200
                 and len(reviews) > 0
                 and "user_id" in reviews[0]
                 and "place_id" in reviews[0],
                 f"reviews[0]={reviews[0] if reviews else 'vide'}")
            # Nettoyer
            delete(f"/reviews/{review_id}", token=state["jane_token"])
        else:
            test("7.3 — GET /places/<id>/reviews retourne user_id et place_id",
                 False, "Impossible de creer review de test")

    # TEST 7.4 — Reviews place inexistante
    r = get("/places/00000000-0000-0000-0000-000000000000/reviews")
    test("7.4 — GET /places/inexistant/reviews -> 404",
         r.status_code == 404,
         f"status={r.status_code}")

    # TEST 7.5 — owner_id de la place = ID du user connecte
    if state["place_id"] and state["john_id"]:
        r = get(f"/places/{state['place_id']}")
        data = r.json()
        owner_id = data.get("owner_id") or (data.get("owner") or {}).get("id")
        test("7.5 — owner_id de la place = ID de John (JWT)",
             owner_id == state["john_id"],
             f"owner_id={owner_id}, john_id={state['john_id']}")


# ============================================================
# MAIN
# ============================================================

def check_server():
    """Verifie que le serveur est disponible."""
    try:
        r = requests.get(f"{BASE_URL}/", timeout=3)
        return True
    except requests.exceptions.ConnectionError:
        return False


def main():
    print("\n" + "=" * 60)
    print("   HBNB — TESTS API AUTOMATISES")
    print("=" * 60)

    if not check_server():
        print(f"\n[ERREUR] Serveur inaccessible sur {BASE_URL}")
        print("Lancez d'abord : python3 run.py")
        sys.exit(1)

    print(f"\n  Serveur detecte sur {BASE_URL}")

    test_auth()
    test_crud_users()
    test_crud_amenities()
    test_crud_places()
    test_crud_reviews()
    test_rbac()
    test_relations()

    print("\n" + "=" * 60)
    print(f"  RESULTATS : {passed}/{total} tests passes")
    if failed == 0:
        print("  TOUS LES TESTS SONT PASSES !")
    else:
        print(f"  {failed} ECHEC(S) — voir les [FAIL] ci-dessus")
    print("=" * 60 + "\n")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
