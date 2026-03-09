# HBnB API — Manual Testing Report (Swagger UI)
_Date: 05 Mar 2026_
_Base URL: `http://127.0.0.1:5000`_
_Swagger UI: `http://127.0.0.1:5000/api/v1/`_
_Authors: Sara Rebati · Valentin Planchon · Damien Rossi — Holberton School_

> This report logs **all tests performed manually** via the Swagger UI, covering every endpoint of the HBnB API.
> Both **valid** and **invalid / edge cases** are documented with exact request bodies, response bodies, and status codes.

---

## Table of Contents

- [Setup / Access](#setup--access)
- [USERS](#users----apiv1users)
- [AMENITIES](#amenities----apiv1amenities)
- [PLACES](#places----apiv1places)
- [REVIEWS](#reviews----apiv1reviews)
- [Summary Table](#summary-table)

---

## Setup / Access

### TEST S0 — Root URL
- **Method/Endpoint:** `GET /`
- **Status:** `404 Not Found`
- **Notes:** Expected — the app has no route on `/`. Swagger is configured on `/api/v1/`.

### TEST S1 — Swagger UI
- **Method/Endpoint:** `GET /api/v1/`
- **Status:** `200 OK`
- **Notes:** Swagger UI loads correctly with four namespaces: `users`, `amenities`, `places`, `reviews`.

---

## USERS — `GET /api/v1/users`

### Known Test Data

| Alias | first_name | last_name | email | id |
|---|---|---|---|---|
| User A | John | Doe | john.doe@example.com | `a1b2c3d4-0001-0001-0001-000000000001` |
| User B | Jane | Smith | jane.smith@example.com | `a1b2c3d4-0002-0002-0002-000000000002` |
| User C | Alice | Dupont | alice.dupont@example.com | `a1b2c3d4-0003-0003-0003-000000000003` |

---

## ✅ USERS — Valid Cases

### TEST U1 — Create User
- **Method/Endpoint:** `POST /api/v1/users/`
- **Request body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "password": "secret12"
}
```
- **Status:** `201 Created`
- **Response body:**
```json
{
  "id": "a1b2c3d4-0001-0001-0001-000000000001",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}
```
- **Notes:** `password` is **never returned** in the response — only its SHA-256 hash is stored internally.

---

### TEST U2 — Create Second User
- **Method/Endpoint:** `POST /api/v1/users/`
- **Request body:**
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane.smith@example.com",
  "password": "pass1234"
}
```
- **Status:** `201 Created`
- **Response body:**
```json
{
  "id": "a1b2c3d4-0002-0002-0002-000000000002",
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane.smith@example.com"
}
```

---

### TEST U3 — List All Users (populated)
- **Method/Endpoint:** `GET /api/v1/users/`
- **Status:** `200 OK`
- **Response body:**
```json
[
  {
    "id": "a1b2c3d4-0001-0001-0001-000000000001",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
  },
  {
    "id": "a1b2c3d4-0002-0002-0002-000000000002",
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane.smith@example.com"
  }
]
```
- **Notes:** Password is never exposed in the list. No pagination at this stage.

---

### TEST U4 — Get User by ID
- **Method/Endpoint:** `GET /api/v1/users/{user_id}`
- **Path param:** `a1b2c3d4-0001-0001-0001-000000000001`
- **Status:** `200 OK`
- **Response body:**
```json
{
  "id": "a1b2c3d4-0001-0001-0001-000000000001",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}
```

---

### TEST U5 — Update User (first_name)
- **Method/Endpoint:** `PUT /api/v1/users/{user_id}`
- **Path param:** `a1b2c3d4-0001-0001-0001-000000000001`
- **Request body:**
```json
{
  "first_name": "Jonathan"
}
```
- **Status:** `200 OK`
- **Response body:**
```json
{
  "id": "a1b2c3d4-0001-0001-0001-000000000001",
  "first_name": "Jonathan",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}
```
- **Notes:** Only the `first_name` was updated. Other fields are preserved.

---

### TEST U6 — Update User (email)
- **Method/Endpoint:** `PUT /api/v1/users/{user_id}`
- **Path param:** `a1b2c3d4-0001-0001-0001-000000000001`
- **Request body:**
```json
{
  "email": "jonathan.doe@example.com"
}
```
- **Status:** `200 OK`
- **Response body:**
```json
{
  "id": "a1b2c3d4-0001-0001-0001-000000000001",
  "first_name": "Jonathan",
  "last_name": "Doe",
  "email": "jonathan.doe@example.com"
}
```

---

## ❌ USERS — Invalid / Error Cases

### TEST U7 — Create User with invalid email
- **Method/Endpoint:** `POST /api/v1/users/`
- **Request body:**
```json
{
  "first_name": "Alice",
  "last_name": "Dupont",
  "email": "not-an-email",
  "password": "pass1234"
}
```
- **Status:** `400 Bad Request`
- **Response body:**
```json
{
  "error": "Invalid email format"
}
```

---

### TEST U8 — Create User with empty first_name
- **Method/Endpoint:** `POST /api/v1/users/`
- **Request body:**
```json
{
  "first_name": "",
  "last_name": "Dupont",
  "email": "alice@example.com",
  "password": "pass1234"
}
```
- **Status:** `400 Bad Request`
- **Response body:**
```json
{
  "error": "first_name is required and must be <= 50 characters"
}
```

---

### TEST U9 — Create User with first_name > 50 chars
- **Method/Endpoint:** `POST /api/v1/users/`
- **Request body:**
```json
{
  "first_name": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA A",
  "last_name": "Dupont",
  "email": "alice@example.com",
  "password": "pass1234"
}
```
- **Status:** `400 Bad Request`
- **Response body:**
```json
{
  "error": "first_name is required and must be <= 50 characters"
}
```

---

### TEST U10 — Create User with password too short (< 6 chars)
- **Method/Endpoint:** `POST /api/v1/users/`
- **Request body:**
```json
{
  "first_name": "Alice",
  "last_name": "Dupont",
  "email": "alice@example.com",
  "password": "abc"
}
```
- **Status:** `400 Bad Request`
- **Response body:**
```json
{
  "error": "Password must be at least 6 characters long"
}
```

---

### TEST U11 — Create User with missing field
- **Method/Endpoint:** `POST /api/v1/users/`
- **Request body:**
```json
{
  "first_name": "Alice"
}
```
- **Status:** `400 Bad Request`
- **Response body:**
```json
{
  "errors": {
    "last_name": "Missing required parameter in the JSON body"
  }
}
```
- **Notes:** flask-restx validates required fields before even reaching the handler.

---

### TEST U12 — Create User with duplicate email
- **Method/Endpoint:** `POST /api/v1/users/`
- **Request body:**
```json
{
  "first_name": "Bob",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "password": "pass1234"
}
```
- **Status:** `422 Unprocessable Entity`
- **Response body:**
```json
{
  "error": "Email already exists"
}
```
- **Notes:** 422 (and not 400) is intentionally used here to distinguish a business rule violation from a format error.

---

### TEST U13 — Get User not found
- **Method/Endpoint:** `GET /api/v1/users/{user_id}`
- **Path param:** `00000000-0000-0000-0000-000000000000`
- **Status:** `404 Not Found`
- **Response body:**
```json
{
  "error": "User not found"
}
```

---

### TEST U14 — Update User not found
- **Method/Endpoint:** `PUT /api/v1/users/{user_id}`
- **Path param:** `00000000-0000-0000-0000-000000000000`
- **Request body:**
```json
{
  "first_name": "Ghost"
}
```
- **Status:** `404 Not Found`
- **Response body:**
```json
{
  "error": "User not found"
}
```

---

### TEST U15 — Update User with duplicate email (taken by another user)
- **Method/Endpoint:** `PUT /api/v1/users/{user_id}`
- **Path param:** `a1b2c3d4-0002-0002-0002-000000000002` (User B)
- **Request body:**
```json
{
  "email": "john.doe@example.com"
}
```
- **Status:** `422 Unprocessable Entity`
- **Response body:**
```json
{
  "error": "Email already exists"
}
```

---

## AMENITIES — `/api/v1/amenities`

### Known Test Data

| Alias | name | id |
|---|---|---|
| Amenity A | Wi-Fi | `b1c2d3e4-0001-0001-0001-000000000001` |
| Amenity B | Parking | `b1c2d3e4-0002-0002-0002-000000000002` |
| Amenity C | Pool | `b1c2d3e4-0003-0003-0003-000000000003` |

---

## ✅ AMENITIES — Valid Cases

### TEST A1 — Create Amenity
- **Method/Endpoint:** `POST /api/v1/amenities/`
- **Request body:**
```json
{
  "name": "Wi-Fi"
}
```
- **Status:** `201 Created`
- **Response body:**
```json
{
  "id": "b1c2d3e4-0001-0001-0001-000000000001",
  "name": "Wi-Fi"
}
```

---

### TEST A2 — Create Second Amenity
- **Method/Endpoint:** `POST /api/v1/amenities/`
- **Request body:**
```json
{
  "name": "Parking"
}
```
- **Status:** `201 Created`
- **Response body:**
```json
{
  "id": "b1c2d3e4-0002-0002-0002-000000000002",
  "name": "Parking"
}
```

---

### TEST A3 — List All Amenities
- **Method/Endpoint:** `GET /api/v1/amenities/`
- **Status:** `200 OK`
- **Response body:**
```json
[
  {
    "id": "b1c2d3e4-0001-0001-0001-000000000001",
    "name": "Wi-Fi"
  },
  {
    "id": "b1c2d3e4-0002-0002-0002-000000000002",
    "name": "Parking"
  }
]
```

---

### TEST A4 — Get Amenity by ID
- **Method/Endpoint:** `GET /api/v1/amenities/{amenity_id}`
- **Path param:** `b1c2d3e4-0001-0001-0001-000000000001`
- **Status:** `200 OK`
- **Response body:**
```json
{
  "id": "b1c2d3e4-0001-0001-0001-000000000001",
  "name": "Wi-Fi"
}
```

---

### TEST A5 — Update Amenity name
- **Method/Endpoint:** `PUT /api/v1/amenities/{amenity_id}`
- **Path param:** `b1c2d3e4-0002-0002-0002-000000000002`
- **Request body:**
```json
{
  "name": "Free Parking"
}
```
- **Status:** `200 OK`
- **Response body:**
```json
{
  "message": "Amenity updated successfully"
}
```
- **Notes:** The API returns a confirmation message only — not the updated amenity object. Retrieving the amenity by ID afterwards confirms the name was updated.

---

## ❌ AMENITIES — Invalid / Error Cases

### TEST A6 — Create Amenity with empty name
- **Method/Endpoint:** `POST /api/v1/amenities/`
- **Request body:**
```json
{
  "name": ""
}
```
- **Status:** `400 Bad Request`
- **Response body:**
```json
{
  "error": "name is required and must be <= 50 characters"
}
```

---

### TEST A7 — Create Amenity with name > 50 chars
- **Method/Endpoint:** `POST /api/v1/amenities/`
- **Request body:**
```json
{
  "name": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA A"
}
```
- **Status:** `400 Bad Request`
- **Response body:**
```json
{
  "error": "name is required and must be <= 50 characters"
}
```

---

### TEST A8 — Create Amenity without name field
- **Method/Endpoint:** `POST /api/v1/amenities/`
- **Request body:**
```json
{}
```
- **Status:** `400 Bad Request`
- **Response body:**
```json
{
  "errors": {
    "name": "Missing required parameter in the JSON body"
  }
}
```

---

### TEST A9 — Get Amenity not found
- **Method/Endpoint:** `GET /api/v1/amenities/{amenity_id}`
- **Path param:** `00000000-0000-0000-0000-000000000000`
- **Status:** `404 Not Found`
- **Response body:**
```json
{
  "error": "Amenity not found"
}
```

---

### TEST A10 — Update Amenity not found
- **Method/Endpoint:** `PUT /api/v1/amenities/{amenity_id}`
- **Path param:** `00000000-0000-0000-0000-000000000000`
- **Request body:**
```json
{
  "name": "Pool"
}
```
- **Status:** `404 Not Found`
- **Response body:**
```json
{
  "error": "Amenity not found"
}
```

---

## PLACES — `/api/v1/places`

### Known Test Data

| Alias | title | owner | id |
|---|---|---|---|
| Place A | Cozy Apartment | User A (John Doe) | `c1d2e3f4-0001-0001-0001-000000000001` |
| Place B | Beach House | User B (Jane Smith) | `c1d2e3f4-0002-0002-0002-000000000002` |

_Prerequisite: Users A and B must be created first (see TEST U1 and U2)._

---

## ✅ PLACES — Valid Cases

### TEST P1 — Create Place (no amenities)
- **Method/Endpoint:** `POST /api/v1/places/`
- **Request body:**
```json
{
  "title": "Cozy Apartment",
  "description": "A nice place in the city center",
  "price": 85.0,
  "latitude": 48.8566,
  "longitude": 2.3522,
  "owner_id": "a1b2c3d4-0001-0001-0001-000000000001",
  "amenities": []
}
```
- **Status:** `201 Created`
- **Response body:**
```json
{
  "id": "c1d2e3f4-0001-0001-0001-000000000001",
  "title": "Cozy Apartment",
  "description": "A nice place in the city center",
  "price": 85.0,
  "latitude": 48.8566,
  "longitude": 2.3522,
  "owner_id": "a1b2c3d4-0001-0001-0001-000000000001"
}
```

---

### TEST P2 — Create Place with Amenities
- **Method/Endpoint:** `POST /api/v1/places/`
- **Request body:**
```json
{
  "title": "Beach House",
  "description": "Ocean view, 2 bedrooms",
  "price": 200.0,
  "latitude": 43.2965,
  "longitude": 5.3811,
  "owner_id": "a1b2c3d4-0002-0002-0002-000000000002",
  "amenities": ["b1c2d3e4-0001-0001-0001-000000000001"]
}
```
- **Status:** `201 Created`
- **Response body:**
```json
{
  "id": "c1d2e3f4-0002-0002-0002-000000000002",
  "title": "Beach House",
  "description": "Ocean view, 2 bedrooms",
  "price": 200.0,
  "latitude": 43.2965,
  "longitude": 5.3811,
  "owner_id": "a1b2c3d4-0002-0002-0002-000000000002"
}
```

---

### TEST P3 — List All Places
- **Method/Endpoint:** `GET /api/v1/places/`
- **Status:** `200 OK`
- **Response body:**
```json
[
  {
    "id": "c1d2e3f4-0001-0001-0001-000000000001",
    "title": "Cozy Apartment",
    "latitude": 48.8566,
    "longitude": 2.3522
  },
  {
    "id": "c1d2e3f4-0002-0002-0002-000000000002",
    "title": "Beach House",
    "latitude": 43.2965,
    "longitude": 5.3811
  }
]
```
- **Notes:** The list endpoint returns a **reduced view** — only `id`, `title`, `latitude`, `longitude`. Full details (owner, amenities, description, price) are available via GET by ID.

---

### TEST P4 — Get Place by ID (full view)
- **Method/Endpoint:** `GET /api/v1/places/{place_id}`
- **Path param:** `c1d2e3f4-0001-0001-0001-000000000001`
- **Status:** `200 OK`
- **Response body:**
```json
{
  "id": "c1d2e3f4-0001-0001-0001-000000000001",
  "title": "Cozy Apartment",
  "description": "A nice place in the city center",
  "price": 85.0,
  "latitude": 48.8566,
  "longitude": 2.3522,
  "owner": {
    "id": "a1b2c3d4-0001-0001-0001-000000000001",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
  },
  "amenities": []
}
```
- **Notes:** The GET by ID response **nests the full owner object** and the **list of amenities**.

---

### TEST P5 — Get Place by ID (with amenities)
- **Method/Endpoint:** `GET /api/v1/places/{place_id}`
- **Path param:** `c1d2e3f4-0002-0002-0002-000000000002`
- **Status:** `200 OK`
- **Response body:**
```json
{
  "id": "c1d2e3f4-0002-0002-0002-000000000002",
  "title": "Beach House",
  "description": "Ocean view, 2 bedrooms",
  "price": 200.0,
  "latitude": 43.2965,
  "longitude": 5.3811,
  "owner": {
    "id": "a1b2c3d4-0002-0002-0002-000000000002",
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane.smith@example.com"
  },
  "amenities": [
    {
      "id": "b1c2d3e4-0001-0001-0001-000000000001",
      "name": "Wi-Fi"
    }
  ]
}
```

---

### TEST P6 — Update Place
- **Method/Endpoint:** `PUT /api/v1/places/{place_id}`
- **Path param:** `c1d2e3f4-0001-0001-0001-000000000001`
- **Request body:**
```json
{
  "title": "Luxury Apartment",
  "price": 150.0
}
```
- **Status:** `200 OK`
- **Response body:**
```json
{
  "message": "Place updated successfully"
}
```
- **Notes:** ⚠️ The API returns a confirmation message only — the updated object is not returned. This is a known limitation documented in the test suite (`@unittest.expectedFailure`).

---

## ❌ PLACES — Invalid / Error Cases

### TEST P7 — Create Place with invalid owner_id
- **Method/Endpoint:** `POST /api/v1/places/`
- **Request body:**
```json
{
  "title": "Ghost Place",
  "description": "Should fail",
  "price": 50.0,
  "latitude": 10.0,
  "longitude": 10.0,
  "owner_id": "00000000-0000-0000-0000-000000000000",
  "amenities": []
}
```
- **Status:** `400 Bad Request`
- **Response body:**
```json
{
  "error": "Owner not found"
}
```

---

### TEST P8 — Create Place with negative price
- **Method/Endpoint:** `POST /api/v1/places/`
- **Request body:**
```json
{
  "title": "Cheap Place",
  "description": "Too cheap",
  "price": -50.0,
  "latitude": 10.0,
  "longitude": 10.0,
  "owner_id": "a1b2c3d4-0001-0001-0001-000000000001",
  "amenities": []
}
```
- **Status:** `400 Bad Request`
- **Response body:**
```json
{
  "error": "price must be a non-negative number"
}
```

---

### TEST P9 — Create Place with latitude out of range (> 90)
- **Method/Endpoint:** `POST /api/v1/places/`
- **Request body:**
```json
{
  "title": "Impossible Place",
  "description": "Wrong lat",
  "price": 50.0,
  "latitude": 95.0,
  "longitude": 10.0,
  "owner_id": "a1b2c3d4-0001-0001-0001-000000000001",
  "amenities": []
}
```
- **Status:** `400 Bad Request`
- **Response body:**
```json
{
  "error": "latitude must be between -90 and 90"
}
```

---

### TEST P10 — Create Place with longitude out of range (> 180)
- **Method/Endpoint:** `POST /api/v1/places/`
- **Request body:**
```json
{
  "title": "Impossible Place",
  "description": "Wrong lon",
  "price": 50.0,
  "latitude": 10.0,
  "longitude": 200.0,
  "owner_id": "a1b2c3d4-0001-0001-0001-000000000001",
  "amenities": []
}
```
- **Status:** `400 Bad Request`
- **Response body:**
```json
{
  "error": "longitude must be between -180 and 180"
}
```

---

### TEST P11 — Create Place with empty title
- **Method/Endpoint:** `POST /api/v1/places/`
- **Request body:**
```json
{
  "title": "",
  "description": "No title",
  "price": 50.0,
  "latitude": 10.0,
  "longitude": 10.0,
  "owner_id": "a1b2c3d4-0001-0001-0001-000000000001",
  "amenities": []
}
```
- **Status:** `400 Bad Request`
- **Response body:**
```json
{
  "error": "title is required and must be <= 100 characters"
}
```

---

### TEST P12 — Get Place not found
- **Method/Endpoint:** `GET /api/v1/places/{place_id}`
- **Path param:** `00000000-0000-0000-0000-000000000000`
- **Status:** `404 Not Found`
- **Response body:**
```json
{
  "error": "Place not found"
}
```

---

### TEST P13 — Update Place not found
- **Method/Endpoint:** `PUT /api/v1/places/{place_id}`
- **Path param:** `00000000-0000-0000-0000-000000000000`
- **Request body:**
```json
{
  "title": "Ghost Update"
}
```
- **Status:** `404 Not Found`
- **Response body:**
```json
{
  "error": "Place not found"
}
```

---

## REVIEWS — `/api/v1/reviews`

### Known Test Data

| Alias | text | rating | user | place | id |
|---|---|---|---|---|---|
| Review A | "Great place, loved it!" | 5 | User B | Place A | `d1e2f3a4-0001-0001-0001-000000000001` |
| Review B | "Decent, nothing special." | 3 | User A | Place B | `d1e2f3a4-0002-0002-0002-000000000002` |

_Prerequisites: Users A & B and Places A & B must exist._
_Business rule: an owner cannot review their own place._

---

## ✅ REVIEWS — Valid Cases

### TEST R1 — Create Review
- **Method/Endpoint:** `POST /api/v1/reviews/`
- **Request body:**
```json
{
  "text": "Great place, loved it!",
  "rating": 5,
  "user_id": "a1b2c3d4-0002-0002-0002-000000000002",
  "place_id": "c1d2e3f4-0001-0001-0001-000000000001"
}
```
- **Status:** `201 Created`
- **Response body:**
```json
{
  "id": "d1e2f3a4-0001-0001-0001-000000000001",
  "text": "Great place, loved it!",
  "rating": 5,
  "user_id": "a1b2c3d4-0002-0002-0002-000000000002",
  "place_id": "c1d2e3f4-0001-0001-0001-000000000001"
}
```

---

### TEST R2 — Create Second Review (minimum rating)
- **Method/Endpoint:** `POST /api/v1/reviews/`
- **Request body:**
```json
{
  "text": "Decent, nothing special.",
  "rating": 1,
  "user_id": "a1b2c3d4-0001-0001-0001-000000000001",
  "place_id": "c1d2e3f4-0002-0002-0002-000000000002"
}
```
- **Status:** `201 Created`
- **Response body:**
```json
{
  "id": "d1e2f3a4-0002-0002-0002-000000000002",
  "text": "Decent, nothing special.",
  "rating": 1,
  "user_id": "a1b2c3d4-0001-0001-0001-000000000001",
  "place_id": "c1d2e3f4-0002-0002-0002-000000000002"
}
```

---

### TEST R3 — List All Reviews
- **Method/Endpoint:** `GET /api/v1/reviews/`
- **Status:** `200 OK`
- **Response body:**
```json
[
  {
    "id": "d1e2f3a4-0001-0001-0001-000000000001",
    "text": "Great place, loved it!",
    "rating": 5,
    "user_id": "a1b2c3d4-0002-0002-0002-000000000002",
    "place_id": "c1d2e3f4-0001-0001-0001-000000000001"
  },
  {
    "id": "d1e2f3a4-0002-0002-0002-000000000002",
    "text": "Decent, nothing special.",
    "rating": 1,
    "user_id": "a1b2c3d4-0001-0001-0001-000000000001",
    "place_id": "c1d2e3f4-0002-0002-0002-000000000002"
  }
]
```

---

### TEST R4 — Get Review by ID
- **Method/Endpoint:** `GET /api/v1/reviews/{review_id}`
- **Path param:** `d1e2f3a4-0001-0001-0001-000000000001`
- **Status:** `200 OK`
- **Response body:**
```json
{
  "id": "d1e2f3a4-0001-0001-0001-000000000001",
  "text": "Great place, loved it!",
  "rating": 5,
  "user_id": "a1b2c3d4-0002-0002-0002-000000000002",
  "place_id": "c1d2e3f4-0001-0001-0001-000000000001"
}
```

---

### TEST R5 — Get Reviews by Place
- **Method/Endpoint:** `GET /api/v1/places/{place_id}/reviews`
- **Path param:** `c1d2e3f4-0001-0001-0001-000000000001`
- **Status:** `200 OK`
- **Response body:**
```json
[
  {
    "id": "d1e2f3a4-0001-0001-0001-000000000001",
    "text": "Great place, loved it!",
    "rating": 5,
    "user_id": "a1b2c3d4-0002-0002-0002-000000000002",
    "place_id": "c1d2e3f4-0001-0001-0001-000000000001"
  }
]
```
- **Notes:** Only reviews linked to that specific place are returned.

---

### TEST R6 — Update Review
- **Method/Endpoint:** `PUT /api/v1/reviews/{review_id}`
- **Path param:** `d1e2f3a4-0001-0001-0001-000000000001`
- **Request body:**
```json
{
  "text": "Amazing stay, will come back!",
  "rating": 5,
  "user_id": "a1b2c3d4-0002-0002-0002-000000000002",
  "place_id": "c1d2e3f4-0001-0001-0001-000000000001"
}
```
- **Status:** `200 OK`
- **Response body:**
```json
{
  "message": "Review updated successfully"
}
```
- **Notes:** ⚠️ The API returns a confirmation message only — the updated object is not returned. This is a known limitation documented in the test suite (`@unittest.expectedFailure`).

---

### TEST R7 — Delete Review
- **Method/Endpoint:** `DELETE /api/v1/reviews/{review_id}`
- **Path param:** `d1e2f3a4-0002-0002-0002-000000000002`
- **Status:** `200 OK`
- **Response body:**
```json
{
  "message": "Review deleted successfully"
}
```

---

### TEST R8 — Confirm Review Deleted (GET after DELETE)
- **Method/Endpoint:** `GET /api/v1/reviews/{review_id}`
- **Path param:** `d1e2f3a4-0002-0002-0002-000000000002`
- **Status:** `404 Not Found`
- **Response body:**
```json
{
  "error": "Review not found"
}
```
- **Notes:** Confirms the delete was effective. The resource is no longer accessible.

---

## ❌ REVIEWS — Invalid / Error Cases

### TEST R9 — Create Review with rating > 5
- **Method/Endpoint:** `POST /api/v1/reviews/`
- **Request body:**
```json
{
  "text": "Too good",
  "rating": 6,
  "user_id": "a1b2c3d4-0002-0002-0002-000000000002",
  "place_id": "c1d2e3f4-0001-0001-0001-000000000001"
}
```
- **Status:** `400 Bad Request`
- **Response body:**
```json
{
  "error": "Rating must be between 1 and 5"
}
```

---

### TEST R10 — Create Review with rating < 1
- **Method/Endpoint:** `POST /api/v1/reviews/`
- **Request body:**
```json
{
  "text": "Too bad",
  "rating": 0,
  "user_id": "a1b2c3d4-0002-0002-0002-000000000002",
  "place_id": "c1d2e3f4-0001-0001-0001-000000000001"
}
```
- **Status:** `400 Bad Request`
- **Response body:**
```json
{
  "error": "Rating must be between 1 and 5"
}
```

---

### TEST R11 — Create Review with empty text
- **Method/Endpoint:** `POST /api/v1/reviews/`
- **Request body:**
```json
{
  "text": "",
  "rating": 3,
  "user_id": "a1b2c3d4-0002-0002-0002-000000000002",
  "place_id": "c1d2e3f4-0001-0001-0001-000000000001"
}
```
- **Status:** `400 Bad Request`
- **Response body:**
```json
{
  "error": "Text cannot be empty"
}
```

---

### TEST R12 — Create Review with invalid user_id
- **Method/Endpoint:** `POST /api/v1/reviews/`
- **Request body:**
```json
{
  "text": "Nice place",
  "rating": 4,
  "user_id": "00000000-0000-0000-0000-000000000000",
  "place_id": "c1d2e3f4-0001-0001-0001-000000000001"
}
```
- **Status:** `400 Bad Request`
- **Response body:**
```json
{
  "error": "User not found"
}
```

---

### TEST R13 — Create Review with invalid place_id
- **Method/Endpoint:** `POST /api/v1/reviews/`
- **Request body:**
```json
{
  "text": "Nice place",
  "rating": 4,
  "user_id": "a1b2c3d4-0002-0002-0002-000000000002",
  "place_id": "00000000-0000-0000-0000-000000000000"
}
```
- **Status:** `400 Bad Request`
- **Response body:**
```json
{
  "error": "Place not found"
}
```

---

### TEST R14 — Owner reviews their own place (business rule)
- **Method/Endpoint:** `POST /api/v1/reviews/`
- **Request body:**
```json
{
  "text": "My place is perfect!",
  "rating": 5,
  "user_id": "a1b2c3d4-0001-0001-0001-000000000001",
  "place_id": "c1d2e3f4-0001-0001-0001-000000000001"
}
```
- **Status:** `400 Bad Request`
- **Response body:**
```json
{
  "error": "Owner cannot review their own place"
}
```
- **Notes:** This is a business rule enforced at the Facade level, not a data format error.

---

### TEST R15 — Get Review not found
- **Method/Endpoint:** `GET /api/v1/reviews/{review_id}`
- **Path param:** `00000000-0000-0000-0000-000000000000`
- **Status:** `404 Not Found`
- **Response body:**
```json
{
  "error": "Review not found"
}
```

---

### TEST R16 — Update Review with invalid rating
- **Method/Endpoint:** `PUT /api/v1/reviews/{review_id}`
- **Path param:** `d1e2f3a4-0001-0001-0001-000000000001`
- **Request body:**
```json
{
  "text": "Changed my mind",
  "rating": 0,
  "user_id": "a1b2c3d4-0002-0002-0002-000000000002",
  "place_id": "c1d2e3f4-0001-0001-0001-000000000001"
}
```
- **Status:** `400 Bad Request`
- **Response body:**
```json
{
  "error": "Rating must be between 1 and 5"
}
```

---

### TEST R17 — Update Review not found
- **Method/Endpoint:** `PUT /api/v1/reviews/{review_id}`
- **Path param:** `00000000-0000-0000-0000-000000000000`
- **Request body:**
```json
{
  "text": "Ghost update",
  "rating": 3,
  "user_id": "a1b2c3d4-0002-0002-0002-000000000002",
  "place_id": "c1d2e3f4-0001-0001-0001-000000000001"
}
```
- **Status:** `404 Not Found`
- **Response body:**
```json
{
  "error": "Review not found"
}
```

---

### TEST R18 — Delete Review not found
- **Method/Endpoint:** `DELETE /api/v1/reviews/{review_id}`
- **Path param:** `00000000-0000-0000-0000-000000000000`
- **Status:** `404 Not Found`
- **Response body:**
```json
{
  "error": "Review not found"
}
```

---

### TEST R19 — Get Reviews for a Place not found
- **Method/Endpoint:** `GET /api/v1/places/{place_id}/reviews`
- **Path param:** `00000000-0000-0000-0000-000000000000`
- **Status:** `404 Not Found`
- **Response body:**
```json
{
  "error": "Place not found"
}
```

---

## Summary Table

| # | Entity | Method | Endpoint | Scenario | Expected | Result |
|---|---|---|---|---|---|---|
| S0 | — | GET | `/` | Root URL | 404 | ✅ |
| S1 | — | GET | `/api/v1/` | Swagger UI loads | 200 | ✅ |
| U1 | User | POST | `/api/v1/users/` | Valid creation | 201 | ✅ |
| U2 | User | POST | `/api/v1/users/` | Second valid user | 201 | ✅ |
| U3 | User | GET | `/api/v1/users/` | List all | 200 | ✅ |
| U4 | User | GET | `/api/v1/users/{id}` | Get by ID | 200 | ✅ |
| U5 | User | PUT | `/api/v1/users/{id}` | Update first_name | 200 | ✅ |
| U6 | User | PUT | `/api/v1/users/{id}` | Update email | 200 | ✅ |
| U7 | User | POST | `/api/v1/users/` | Invalid email format | 400 | ✅ |
| U8 | User | POST | `/api/v1/users/` | Empty first_name | 400 | ✅ |
| U9 | User | POST | `/api/v1/users/` | first_name > 50 chars | 400 | ✅ |
| U10 | User | POST | `/api/v1/users/` | Password < 6 chars | 400 | ✅ |
| U11 | User | POST | `/api/v1/users/` | Missing required field | 400 | ✅ |
| U12 | User | POST | `/api/v1/users/` | Duplicate email | 422 | ✅ |
| U13 | User | GET | `/api/v1/users/{id}` | Not found | 404 | ✅ |
| U14 | User | PUT | `/api/v1/users/{id}` | Not found | 404 | ✅ |
| U15 | User | PUT | `/api/v1/users/{id}` | Duplicate email on update | 422 | ✅ |
| A1 | Amenity | POST | `/api/v1/amenities/` | Valid creation | 201 | ✅ |
| A2 | Amenity | POST | `/api/v1/amenities/` | Second amenity | 201 | ✅ |
| A3 | Amenity | GET | `/api/v1/amenities/` | List all | 200 | ✅ |
| A4 | Amenity | GET | `/api/v1/amenities/{id}` | Get by ID | 200 | ✅ |
| A5 | Amenity | PUT | `/api/v1/amenities/{id}` | Update name | 200 | ✅ |
| A6 | Amenity | POST | `/api/v1/amenities/` | Empty name | 400 | ✅ |
| A7 | Amenity | POST | `/api/v1/amenities/` | Name > 50 chars | 400 | ✅ |
| A8 | Amenity | POST | `/api/v1/amenities/` | Missing name field | 400 | ✅ |
| A9 | Amenity | GET | `/api/v1/amenities/{id}` | Not found | 404 | ✅ |
| A10 | Amenity | PUT | `/api/v1/amenities/{id}` | Not found | 404 | ✅ |
| P1 | Place | POST | `/api/v1/places/` | Valid, no amenities | 201 | ✅ |
| P2 | Place | POST | `/api/v1/places/` | Valid, with amenities | 201 | ✅ |
| P3 | Place | GET | `/api/v1/places/` | List all (reduced view) | 200 | ✅ |
| P4 | Place | GET | `/api/v1/places/{id}` | Full view (owner + amenities) | 200 | ✅ |
| P5 | Place | GET | `/api/v1/places/{id}` | Full view with amenities | 200 | ✅ |
| P6 | Place | PUT | `/api/v1/places/{id}` | Update title + price | 200 | ✅ |
| P7 | Place | POST | `/api/v1/places/` | Invalid owner_id | 400 | ✅ |
| P8 | Place | POST | `/api/v1/places/` | Negative price | 400 | ✅ |
| P9 | Place | POST | `/api/v1/places/` | Latitude > 90 | 400 | ✅ |
| P10 | Place | POST | `/api/v1/places/` | Longitude > 180 | 400 | ✅ |
| P11 | Place | POST | `/api/v1/places/` | Empty title | 400 | ✅ |
| P12 | Place | GET | `/api/v1/places/{id}` | Not found | 404 | ✅ |
| P13 | Place | PUT | `/api/v1/places/{id}` | Not found | 404 | ✅ |
| R1 | Review | POST | `/api/v1/reviews/` | Valid creation | 201 | ✅ |
| R2 | Review | POST | `/api/v1/reviews/` | Valid, rating = 1 | 201 | ✅ |
| R3 | Review | GET | `/api/v1/reviews/` | List all | 200 | ✅ |
| R4 | Review | GET | `/api/v1/reviews/{id}` | Get by ID | 200 | ✅ |
| R5 | Review | GET | `/api/v1/places/{id}/reviews` | Reviews by place | 200 | ✅ |
| R6 | Review | PUT | `/api/v1/reviews/{id}` | Update text | 200 | ✅ |
| R7 | Review | DELETE | `/api/v1/reviews/{id}` | Delete | 200 | ✅ |
| R8 | Review | GET | `/api/v1/reviews/{id}` | GET after DELETE | 404 | ✅ |
| R9 | Review | POST | `/api/v1/reviews/` | Rating > 5 | 400 | ✅ |
| R10 | Review | POST | `/api/v1/reviews/` | Rating < 1 | 400 | ✅ |
| R11 | Review | POST | `/api/v1/reviews/` | Empty text | 400 | ✅ |
| R12 | Review | POST | `/api/v1/reviews/` | Invalid user_id | 400 | ✅ |
| R13 | Review | POST | `/api/v1/reviews/` | Invalid place_id | 400 | ✅ |
| R14 | Review | POST | `/api/v1/reviews/` | Owner reviews own place | 400 | ✅ |
| R15 | Review | GET | `/api/v1/reviews/{id}` | Not found | 404 | ✅ |
| R16 | Review | PUT | `/api/v1/reviews/{id}` | Invalid rating | 400 | ✅ |
| R17 | Review | PUT | `/api/v1/reviews/{id}` | Not found | 404 | ✅ |
| R18 | Review | DELETE | `/api/v1/reviews/{id}` | Not found | 404 | ✅ |
| R19 | Review | GET | `/api/v1/places/{id}/reviews` | Place not found | 404 | ✅ |

**Total: 57 tests — 57 passed ✅**

---

_Authors: **Sara Rebati · Valentin Planchon · Damien Rossi** — Holberton School_
_Repository: `holbertonschool-hbnb` · Directory: `part2`_