# Task 2 — Explanatory Notes

Summary of the API flows and the role of each layer in fulfilling the requests described by the sequence diagrams.

---

## 1. User Registration — `POST /api/users/register`

### Purpose of the sequence diagram

This diagram describes the flow for **registering a new user**. It shows how the client sends registration data, how it is validated and stored, and how an authentication token is returned.

### Brief description of the API call

| Step | Layer | Action |
|------|--------|--------|
| 1 | **Presentation (API)** | Receives `POST /api/users/register` with `{first_name, last_name, email, password}`. |
| 2 | **Presentation** | Validates input format (e.g. email format, password strength). Returns `400 Bad Request` if invalid. |
| 3 | **Business Logic (User Model)** | Creates user via `create_user(user_data)`: checks email uniqueness in DB. |
| 4 | **Business Logic** | If email exists → returns error; API responds with `409 Conflict`. |
| 5 | **Business Logic** | Hashes password, generates UUID and `created_at`, then persists user via **Persistence Layer**. |
| 6 | **Presentation** | Generates authentication token and returns `201 Created` with `{user_id, token, message}`. |

### Flow of interactions and layer roles

- **Presentation Layer (API/Services):** Entry point; validates request format, delegates user creation to the User model, generates the token, and shapes HTTP responses (400, 409, 201).
- **Business Logic Layer (User Model):** Encapsulates registration rules: email uniqueness, password hashing, and creation of the user entity before persisting.
- **Persistence Layer (Database):** Stores and queries users (e.g. check email, `INSERT` new user); no business rules, only data access.

The flow is linear: **Client → API → User Model → Database**, with validation and error handling at the API and Business Logic layers.

---

## 2. Place Creation — `POST /api/places`

### Purpose of the sequence diagram

This diagram describes the flow for **creating a new place by an authenticated host**. It shows authentication, input validation, place creation, amenity linking, and the response returned to the client.

### Brief description of the API call

| Step | Layer | Action |
|------|--------|--------|
| 1 | **Presentation (API)** | Receives `POST /api/places` with place data and optional `amenities: [amenity_ids]`. |
| 2 | **Authentication Service** | Validates token; returns `user_id` and `is_host`. If not authenticated or not host → `401` or `403`. |
| 3 | **Presentation** | Validates input (e.g. price > 0, valid coordinates). Returns `400 Bad Request` if invalid. |
| 4 | **Business Logic (Place Model)** | `create_place(place_data, owner_id)`: validates coordinates and price, generates UUID, sets `is_available = true`, `created_at`. |
| 5 | **Persistence** | `INSERT` into `places`; then for each `amenity_id`, verify existence and `INSERT` into `place_amenities`. |
| 6 | **Business Logic** | Loads full place with amenities (e.g. JOIN), returns complete place object to API. |
| 7 | **Presentation** | Returns `201 Created` with place details (e.g. `place_id`, `title`, `amenities`, `message`). |

### Flow of interactions and layer roles

- **Presentation Layer (API/Services):** Receives the request, calls Authentication Service for token validation, validates request body (price, coordinates), calls Place model for creation, and returns the appropriate HTTP status and payload (401/403/400/201).
- **Authentication Service:** Centralizes token validation and role check (`is_host`); protects the endpoint so only authenticated hosts can create places.
- **Business Logic (Place Model):** Implements place creation rules (coordinates, price, defaults), generates IDs and timestamps, and orchestrates amenity linking by delegating existence checks to the Amenity model.
- **Business Logic (Amenity Model):** Verifies that each `amenity_id` exists before the Place model links it; keeps amenity rules in one place.
- **Persistence Layer (Database):** Executes `INSERT` into `places` and `place_amenities`, and `SELECT` (with JOIN) to return the created place with its amenities.

The flow is **Client → API → Auth → API → Place Model → (Amenity Model + DB) → Place Model → DB → API → Client**. Authentication and input validation happen before any write; place and amenity logic are separated in the Business Logic layer.

---

## Summary table

| API | Purpose | Main layers involved | Key validations / checks |
|-----|--------|----------------------|---------------------------|
| **POST /api/users/register** | Create user and get token | API, User Model, DB | Input format, email uniqueness, password hashing |
| **POST /api/places** | Create place (host only) | API, Auth, Place Model, Amenity Model, DB | Token + host role, input (price, coordinates), amenity existence |

These notes align with the sequence diagrams **User_Registration.mmd** and **Place_Creation.mmd** and describe how each layer contributes to fulfilling the API request from the client to the response.
