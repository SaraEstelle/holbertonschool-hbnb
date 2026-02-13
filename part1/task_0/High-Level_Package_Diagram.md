# High-Level Package Diagram — HBnB Evolution

## Objective

The objective of this document is to present a high-level overview of the architecture of the HBnB Evolution application.
It illustrates how the application is organized into three main layers and how these layers communicate with each other using the Facade design pattern.

---

## Application Architecture Overview

The HBnB Evolution application follows a layered architecture composed of three main layers:

- Presentation Layer
- Business Logic Layer
- Persistence Layer

Each layer has a specific responsibility and communicates only with the appropriate adjacent layer.

---

## Presentation Layer

The Presentation Layer is responsible for handling interactions between the user and the application.
It contains the APIs and services exposed to clients.

This layer does not contain any business logic.
All requests are delegated to the Business Logic Layer through the Facade.

---

## Business Logic Layer

The Business Logic Layer represents the core of the application.
It contains the business rules and the main domain models such as User, Place, Review, and Amenity.

This layer is responsible for validating data and applying business logic before interacting with the Persistence Layer.

---

## Persistence Layer

The Persistence Layer is responsible for data storage and retrieval.
It manages interactions with the database and provides mechanisms to create, read, update, and delete data.

This layer is isolated from the Presentation Layer.

---

## Facade Pattern

The communication between the Presentation Layer and the Business Logic Layer is handled through the Facade design pattern.

The Facade provides a unified interface that simplifies interactions and hides the internal complexity of the business logic.
This approach reduces coupling between layers and improves maintainability and scalability.

---

## High-Level Package Diagram

The following diagram illustrates the overall architecture of the HBnB Evolution application and the communication pathways between layers.

---

## High-Level Package Diagram (Version 1)

```mermaid
flowchart TB

%% ===== PRESENTATION LAYER =====
subgraph Presentation_Layer["Presentation Layer (API & Services)"]
    API["REST API\n(Endpoints)"]
    Services["Application Services"]
end

%% ===== FACADE =====
Facade["Facade\n(Application Interface)"]

%% ===== BUSINESS LOGIC LAYER =====
subgraph Business_Logic_Layer["Business Logic Layer (Models & Rules)"]
    UserModel["User Model"]
    PlaceModel["Place Model"]
    ReviewModel["Review Model"]
    AmenityModel["Amenity Model"]

    BusinessRules["Business Rules\n(Validation, Permissions)"]
end

%% ===== PERSISTENCE LAYER =====
subgraph Persistence_Layer["Persistence Layer"]
    Repositories["Repositories / DAO"]
    Database["Database"]
end

%% ===== RELATIONSHIPS =====
API --> Services
Services --> Facade

Facade --> UserModel
Facade --> PlaceModel
Facade --> ReviewModel
Facade --> AmenityModel
Facade --> BusinessRules

UserModel --> Repositories
PlaceModel --> Repositories
ReviewModel --> Repositories
AmenityModel --> Repositories

Repositories --> Database
```
---
## High-Level Package Diagram (Version 2)

```mermaid
flowchart TB

subgraph Presentation["Presentation Layer"]
    API["REST API"]
    Services["Application Services"]
end

Facade["Facade\n(Application Interface)"]

subgraph Business["Business Logic Layer"]
    User["User"]
    Place["Place"]
    Review["Review"]
    Amenity["Amenity"]
end

subgraph Persistence["Persistence Layer"]
    Repository["Repositories"]
    Database["Database"]
end

API --> Services
Services --> Facade

Facade --> User
Facade --> Place
Facade --> Review
Facade --> Amenity

User --> Repository
Place --> Repository
Review --> Repository
Amenity --> Repository

Repository --> Database
```

---
